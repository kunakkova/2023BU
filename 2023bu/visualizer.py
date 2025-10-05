import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Импортируем наш модуль с механикой
import orbit_mechanics

# Гравитационный параметр Солнца
MU_SUN = 0.00029591220828559104

def plot_orbit_3d(final_state, epoch, duration_days=400):
    """
    Строит 3D-график орбиты астероида и Земли с корректным масштабом.
    """
    t_span = [epoch, epoch + duration_days]
    t_eval = np.linspace(t_span[0], t_span[1], 1000)

    asteroid_trajectory = np.array([
        orbit_mechanics.propagate_orbit(final_state, epoch, t, MU_SUN) for t in t_eval
    ])

    theta = np.linspace(0, 2 * np.pi, 200)
    earth_x = np.cos(theta)
    earth_y = np.sin(theta)
    earth_z = np.zeros_like(theta)

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter([0], [0], [0], color='yellow', s=250, label='Солнце')
    ax.plot(earth_x, earth_y, earth_z, 'b--', label='Орбита Земли')
    ax.plot(asteroid_trajectory[:, 0], asteroid_trajectory[:, 1], asteroid_trajectory[:, 2], 'r-', label='Орбита 2023 BU')

    ax.set_xlabel('X (а.е.)')
    ax.set_ylabel('Y (а.е.)')
    ax.set_zlabel('Z (а.е.)')
    ax.set_title('Орбита астероида 2023 BU относительно Солнца')
    ax.legend()

    # --- НОВЫЙ БЛОК КОДА ДЛЯ УСТАНОВКИ МАСШТАБА ---
    # Находим максимальный диапазон данных по всем осям, включая орбиту Земли (радиус 1)
    all_points = np.vstack([asteroid_trajectory[:, :3], np.array([1, 1, 1])])
    x_min, x_max = all_points[:,0].min(), all_points[:,0].max()
    y_min, y_max = all_points[:,1].min(), all_points[:,1].max()
    z_min, z_max = all_points[:,2].min(), all_points[:,2].max()

    max_range = np.array([x_max-x_min, y_max-y_min, z_max-z_min]).max()
    
    mid_x = (x_max+x_min) * 0.5
    mid_y = (y_max+y_min) * 0.5
    mid_z = (z_max+z_min) * 0.5
    
    ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
    ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
    ax.set_zlim(mid_z - max_range/2, mid_z + max_range/2)
    # --- КОНЕЦ НОВОГО БЛОКА ---
    
    plt.show()

def plot_residuals(initial_residuals, final_residuals):
    """
    Строит гистограммы распределения ошибок до и после подгонки.
    
    Args:
        initial_residuals (np.array): Массив невязок до оптимизации.
        final_residuals (np.array): Массив невязок после оптимизации.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Гистограмма начальных ошибок
    ax1.hist(np.rad2deg(initial_residuals) * 3600, bins=30, color='red', alpha=0.75)
    ax1.set_title('Распределение ошибок ДО оптимизации')
    ax1.set_xlabel('Ошибка (в угловых секундах)')
    ax1.set_ylabel('Количество наблюдений')
    ax1.grid(True)

    # Гистограмма конечных ошибок
    ax2.hist(np.rad2deg(final_residuals) * 3600, bins=30, color='green', alpha=0.75)
    ax2.set_title('Распределение ошибок ПОСЛЕ оптимизации')
    ax2.set_xlabel('Ошибка (в угловых секундах)')
    ax2.grid(True)
    
    fig.suptitle('Сравнение точности модели до и после подгонки орбиты', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

