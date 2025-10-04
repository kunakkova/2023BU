# Quick Start Guide - Asteroid 2023 BU Orbit Calculation

## 🚀 Быстрый старт

### Windows:
```cmd
run_project.bat
```

### Linux/Mac:
```bash
chmod +x run_project.sh
./run_project.sh
```

## 📁 Структура проекта

```
Orbit_Calculating_2023BU/
├── src/                           # Исходный код
│   ├── main.cpp                   # Главная программа
│   ├── Ephemeris.h               # Работа с эфемеридами
│   ├── observationProcessor.h    # Обработка наблюдений
│   └── orbitCalculator.h         # Расчет орбиты
├── Data/                         # Входные данные
│   └── 2023BU_observations.txt   # Наблюдения в формате MPC
├── results/                      # Результаты
│   ├── processed_observations.txt
│   ├── orbital_elements.txt
│   ├── ephemeris.txt
│   └── residuals.txt
├── download_data.py              # Скрипт загрузки данных
├── Makefile                      # Сборка проекта
├── README.md                     # Подробная документация
└── QUICK_START.md               # Этот файл
```

## 🔗 Ссылки на данные

### Основные источники данных:

1. **Minor Planet Center (MPC)**
   - 🔗 https://www.minorplanetcenter.net/db_search/show_object?object_id=2023+BU
   - 📊 Наблюдательные данные в формате MPC

2. **JPL Small-Body Database**
   - 🔗 https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2023BU
   - 🛰️ Орбитальные элементы и эфемериды

3. **NASA Horizons System**
   - 🔗 https://ssd-api.jpl.nasa.gov/doc/horizons.html
   - 📈 Генерация эфемерид

## ⚙️ Требования

- **C++ компилятор** (GCC 4.8+ или совместимый)
- **SOFA библиотека** для астрономических вычислений
  - Ubuntu/Debian: `sudo apt-get install libsofa1-dev`
  - Или скачать с: http://www.iausofa.org/

## 🛠️ Ручная сборка

```bash
# Создать папки
make setup

# Собрать проект
make

# Запустить расчет
make run
```

## 📊 Результаты

После выполнения программа создаст файлы в папке `results/`:

- **`orbital_elements.txt`** - Рассчитанные элементы орбиты
- **`ephemeris.txt`** - Сгенерированная эфемерида
- **`residuals.txt`** - Остатки (наблюдения vs расчеты)
- **`processed_observations.txt`** - Обработанные наблюдения

## 🔍 Ключевые особенности

✅ **Расчет орбиты** по реальным наблюдениям  
✅ **Без гравитационного ускорения** (как требовалось)  
✅ **Формат MPC** для наблюдений  
✅ **Анализ остатков** для оценки точности  
✅ **Генерация эфемерид** для сравнения  

## 🆚 Отличия от проекта Oumuamua

- ❌ **Нет гравитационного ускорения** от планет
- ✅ **Упрощенная модель** - только Солнце
- ✅ **Формат MPC** вместо кастомного
- ✅ **Астероид 2023 BU** вместо Oumuamua

## 🐛 Устранение неполадок

### Ошибка компиляции:
```bash
# Установить SOFA библиотеку
sudo apt-get install libsofa1-dev

# Или скачать и скомпилировать вручную
wget http://www.iausofa.org/2021_05_12_C/sofa_c-20210512.tar.gz
tar -xzf sofa_c-20210512.tar.gz
cd sofa/20210512/c
make
```

### Нет данных наблюдений:
1. Запустить: `python3 download_data.py`
2. Или скачать вручную с MPC
3. Сохранить как `Data/2023BU_observations.txt`

## 📞 Поддержка

При возникновении проблем:
1. Проверьте установку SOFA библиотеки
2. Убедитесь в наличии данных наблюдений
3. Проверьте формат файла наблюдений
4. Обратитесь к подробной документации в `README.md`

---
**Удачных расчетов орбиты! 🛰️**
