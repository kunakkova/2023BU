import pandas as pd
import numpy as np
import re
from datetime import datetime

def hms_to_decimal(h, m, s):
    """Преобразует часы, минуты, секунды в десятичные часы."""
    return h + m / 60 + s / 3600

def dms_to_decimal(d, m, s):
    """Преобразует градусы, минуты, секунды в десятичные градусы."""
    sign = 1 if float(d) >= 0 else -1
    return float(d) + sign * (float(m) / 60) + sign * (float(s) / 3600)

def parse_observations(file_path):
    """
    Парсит файл наблюдений JPL HORIZONS и извлекает временные метки,
    прямое восхождение (RA) и склонение (DEC).

    Args:
        file_path (str): Путь к файлу horizons_results.txt.

    Returns:
        pandas.DataFrame: DataFrame со столбцами [JD, RA_rad, DEC_rad].
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_index = None
    for i, line in enumerate(lines):
        if '$$SOE' in line:
            start_index = i + 1
            break

    if start_index is None:
        raise ValueError("Блок с наблюдениями ('$$SOE') не найден в файле.")

    end_index = None
    for i in range(start_index, len(lines)):
        if '$$EOE' in lines[i]:
            end_index = i
            break
    if end_index is None:
        end_index = len(lines)

    obs_lines = lines[start_index:end_index]

    dates = []
    ra_rad = []
    dec_rad = []

    for line in obs_lines:
        # **ИСПРАВЛЕНИЕ ЗДЕСЬ:** r'\s+' вместо r'\\s+'
        parts = re.split(r'\s+', line.strip())
        
        # Строка может быть пустой, пропускаем ее
        if not parts or len(parts) < 8:
            continue
            
        # Некоторые строки могут начинаться с пробела, что дает пустой элемент в начале
        if parts[0] == '':
            parts = parts[1:]

        try:
            # 1. Парсинг и преобразование времени в Юлианскую Дату (JD)
            date_str = parts[0] + ' ' + parts[1]
            dt = datetime.strptime(date_str, '%Y-%b-%d %H:%M')
            jd = 367*dt.year - int(7*(dt.year + int((dt.month+9)/12))/4) + int(275*dt.month/9) + dt.day + 1721013.5 + (dt.hour + dt.minute/60)/24
            dates.append(jd)

            # 2. Парсинг и преобразование прямого восхождения (RA)
            ra_h, ra_m, ra_s = parts[2], parts[3], parts[4]
            ra_deg = hms_to_decimal(float(ra_h), float(ra_m), float(ra_s)) * 15
            ra_rad.append(np.deg2rad(ra_deg))

            # 3. Парсинг и преобразование склонения (DEC)
            dec_d, dec_m, dec_s = parts[5], parts[6], parts[7]
            dec_deg = dms_to_decimal(dec_d, dec_m, dec_s)
            dec_rad.append(np.deg2rad(dec_deg))
        except (ValueError, IndexError):
            # Пропускаем строки, которые не удалось распарсить, если такие встретятся
            print(f"Пропущена строка с неверным форматом: {line.strip()}")
            continue

    df = pd.DataFrame({'JD': dates, 'RA_rad': ra_rad, 'DEC_rad': dec_rad})
    return df

