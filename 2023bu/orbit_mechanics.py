import numpy as np
from scipy.integrate import solve_ivp

def kepler_equations(t, y, mu):
    """
    Уравнения движения для задачи двух тел (Кеплеровское движение).
    Эта функция описывает, как гравитация Солнца изменяет скорость тела.

    Args:
        t: время (не используется в этой простой модели, но требуется для solve_ivp).
        y (list): Вектор состояния [x, y, z, vx, vy, vz].
        mu (float): Гравитационный параметр центрального тела (Солнца).

    Returns:
        list: Производные вектора состояния [vx, vy, vz, ax, ay, az].
    """
    r_vec = y[:3]
    r_norm = np.linalg.norm(r_vec)
    
    # Ускорение a = -mu * r / |r|^3
    accel_vec = -mu * r_vec / r_norm**3
    
    return [y[3], y[4], y[5], accel_vec[0], accel_vec[1], accel_vec[2]]

def propagate_orbit(state_vector, t0, t_target, mu):
    """
    Пропагирует (прогнозирует) орбиту тела с начального времени t0 до целевого t_target.
    Использует численный интегратор для решения уравнений Кеплера.

    Args:
        state_vector (list/np.array): Начальный вектор состояния [x, y, z, vx, vy, vz] в AU и AU/день.
        t0 (float): Начальное время в Юлианских днях.
        t_target (float): Целевое время в Юлианских днях.
        mu (float): Гравитационный параметр Солнца (в AU^3/day^2).

    Returns:
        np.array: Новый вектор состояния в момент времени t_target.
    """
    # Решаем систему дифференциальных уравнений
    solution = solve_ivp(
        fun=kepler_equations,      # Уравнения движения
        t_span=[t0, t_target],     # Интервал времени
        y0=state_vector,           # Начальные условия
        args=(mu,),                # Дополнительные аргументы для fun (mu)
        rtol=1e-12,                # Относительная точность
        atol=1e-12                 # Абсолютная точность
    )
    
    # Возвращаем последнее вычисленное состояние
    final_state = solution.y[:, -1]
    return final_state

def state_to_ra_dec(asteroid_state, earth_state):
    """
    Преобразует гелиоцентрические векторы состояния астероида и Земли
    в наблюдаемые координаты прямого восхождения (RA) и склонения (DEC).

    Args:
        asteroid_state (list/np.array): Вектор состояния астероида [x, y, z, ...].
        earth_state (list/np.array): Вектор состояния Земли [x, y, z, ...].

    Returns:
        tuple: (RA, DEC) в радианах.
    """
    # 1. Находим вектор от Земли до астероида (геоцентрический вектор)
    geo_vector = asteroid_state[:3] - earth_state[:3]
    x, y, z = geo_vector
    
    # 2. Преобразуем декартовы координаты в сферические
    # Прямое восхождение (RA) - угол в плоскости XY
    ra = np.arctan2(y, x)
    # Склонение (DEC) - угол с плоскостью XY
    dec = np.arcsin(z / np.linalg.norm(geo_vector))
    
    # Убедимся, что RA находится в диапазоне [0, 2*pi]
    if ra < 0:
        ra += 2 * np.pi
        
    return (ra, dec)

