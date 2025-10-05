import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel
import visualizer

# --- Импортируем наши модули ---
import data_parser
import orbit_mechanics

# --- Константы ---
# Гравитационный параметр Солнца в AU^3/день^2
MU_SUN = 0.00029591220828559104

def calculate_residuals(initial_state_guess, epoch, observations_df):
    """
    Целевая функция для оптимизатора least_squares.
    Вычисляет "невязки" - разницу между предсказанными и реальными наблюдениями.
    """
    residuals = []
    
    # Получаем временные метки наблюдений
    time_objects = Time(observations_df['JD'].values, format='jd', scale='tdb')
    
    # Получаем точные положения Земли для всех моментов наблюдений ОДНИМ вызовом
    earth_positions, _ = get_body_barycentric_posvel('earth', time_objects)
    earth_states = earth_positions.xyz.to('au').value.T # Транспонируем для удобного итерирования

    for i, row in observations_df.iterrows():
        t_obs = row['JD']
        ra_obs = row['RA_rad']
        dec_obs = row['DEC_rad']

        # 1. Предсказываем положение астероида
        predicted_state = orbit_mechanics.propagate_orbit(initial_state_guess, epoch, t_obs, MU_SUN)
        
        # 2. Берем соответствующее положение Земли
        earth_state = earth_states[i]
        
        # 3. Вычисляем предсказанные RA и DEC
        ra_pred, dec_pred = orbit_mechanics.state_to_ra_dec(predicted_state, earth_state)

        # 4. Вычисляем невязку (разницу)
        # Особая обработка для RA, т.к. это угол (2pi и 0 - это одно и то же)
        delta_ra = ra_pred - ra_obs
        delta_ra = (delta_ra + np.pi) % (2 * np.pi) - np.pi
        
        delta_dec = dec_pred - dec_obs
        
        residuals.extend([delta_ra, delta_dec])
        
    return np.array(residuals)

def main():
    """
    Основная функция для запуска процесса определения орбиты.
    """
    # 1. Загружаем данные наблюдений из файла
    observations = data_parser.parse_observations('horizons_results.txt')
    print(f"Загружено {len(observations)} наблюдений.")

    # 2. Задаем начальное приближение из вашего файла horizons_results.txt
    # Это "Equivalent ICRF heliocentric cartesian coordinates (au, au/d)"
    initial_state_guess = np.array([
        -0.5585807334111443,  # X (au)
         0.746685604159777,   # Y (au)
         0.3255044783346349,  # Z (au)
        -0.01351305344133843, # VX (au/day)
        -0.009562138901216793,# VY (au/day)
        -0.004996700278555643 # VZ (au/day)
    ])
    
    # Эпоха (момент времени) для начального приближения, также из файла
    epoch_jd = 2459969.5  # 2023-Jan-25.00 (TDB)

    print("\n--- Начальное приближение (вектор состояния): ---")
    print(initial_state_guess)
    
    print("\n--- Запуск итерационного процесса уточнения орбиты... ---")
    # 3. Вызываем оптимизатор
    result = least_squares(
        fun=calculate_residuals,    # Функция, минимизирующая невязки
        x0=initial_state_guess,     # Начальное приближение
        args=(epoch_jd, observations), # Дополнительные аргументы для fun
        method='lm',                # Метод Левенберга-Марквардта, хорошо подходит для таких задач
        verbose=2,                  # Показывает детальный лог процесса оптимизации
        xtol=1e-12,                 # Условие остановки по изменению вектора состояния
        ftol=1e-12                  # Условие остановки по изменению суммы квадратов невязок
    )

    # 4. Выводим результат
    final_state = result.x
    print("\n--- Процесс завершен! ---")
    print("\n--- Уточненный вектор состояния (X, Y, Z, VX, VY, VZ): ---")
    print(final_state)

    # --- Шаг 5: Визуализация ---
    print("\n--- Построение графиков... ---")

    # 5.1 Вычисляем начальные невязки для сравнения
    initial_residuals = calculate_residuals(initial_state_guess, epoch_jd, observations)
    
    # 5.2 Финальные невязки у нас уже есть в объекте result
    final_residuals = result.fun

    # 5.3 Строим график орбит
    visualizer.plot_orbit_3d(final_state, epoch_jd)
    
    # 5.4 Строим гистограммы ошибок
    visualizer.plot_residuals(initial_residuals, final_residuals)

if __name__ == '__main__':
    main()

