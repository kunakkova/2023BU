# Asteroid 2023 BU Orbit Calculation

This project calculates the orbital elements of asteroid 2023 BU from real observational data, similar to the Oumuamua project but **without gravitational acceleration** from other celestial bodies.

## Project Overview

Asteroid 2023 BU was discovered on January 21, 2023, by Russian amateur astronomer Gennadiy Borisov. It made a very close approach to Earth on January 26, 2023, passing at a distance of only 3,600 km from the surface - one of the closest recorded approaches of near-Earth objects.

## Key Features

- **Orbit determination** from real observational data
- **No gravitational acceleration** from planets (as requested)
- **MPC format** observation processing
- **Orbital elements** calculation and visualization
- **Residual analysis** for accuracy assessment
- **Ephemeris generation** for comparison

## Project Structure

```
Orbit_Calculating_2023BU/
├── src/                    # Source code
│   ├── main.cpp           # Main program
│   ├── Ephemeris.h        # Ephemeris data handling
│   ├── observationProcessor.h  # Observation data processing
│   └── orbitCalculator.h  # Orbital calculations
├── Data/                  # Input data files
│   └── 2023BU_observations.txt  # MPC format observations
├── results/               # Output files
│   ├── processed_observations.txt
│   ├── orbital_elements.txt
│   ├── ephemeris.txt
│   └── residuals.txt
├── Makefile              # Build configuration
└── README.md             # This file
```

## Data Sources

### Primary Data Sources

1. **Minor Planet Center (MPC) - Real Observation Data**
   - **Direct data URL**: https://www.minorplanetcenter.net/tmp2/2023_BU.txt
   - **Search page**: https://www.minorplanetcenter.net/db_search/show_object?object_id=2023+BU
   - **Format**: MPC observation format with 1783+ real observations
   - **Coverage**: January 21-31, 2023 (close approach period)

2. **JPL Small-Body Database**
   - URL: https://ssd-api.jpl.nasa.gov/doc/sbdb.html
   - API endpoint: https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2023BU

3. **NASA Horizons System**
   - URL: https://ssd-api.jpl.nasa.gov/doc/horizons.html
   - For generating ephemeris data

### Data Format

The program expects observations in MPC format:
```
YYYY MM DD.dddddd HH MM SS.sss HH MM SS.sss
```

Example:
```
2023 01 21.123456 12 34 56.789 -12 34 56.789
```

## Installation and Usage

### Prerequisites

1. **C++ Compiler** (GCC 4.8+ or compatible)
2. **SOFA Library** for astronomical calculations
   - Download from: http://www.iausofa.org/
   - Ubuntu/Debian: `sudo apt-get install libsofa1-dev`
   - Or compile from source

### Build Instructions

1. **Setup directories:**
   ```bash
   make setup
   ```

2. **Download observation data:**
   - Visit the MPC website and search for "2023 BU"
   - Download the observation data in MPC format
   - Save as `Data/2023BU_observations.txt`

3. **Build the program:**
   ```bash
   make
   ```

4. **Run the calculation:**
   ```bash
   make run
   ```

### Manual Build

```bash
g++ -std=c++11 -Wall -O2 -I./src -c src/main.cpp -o src/main.o
g++ -std=c++11 -Wall -O2 -I./src -o orbit_calculator src/main.o -lsofa_c
```

## Output Files

The program generates several output files in the `results/` directory:

1. **`processed_observations.txt`** - Processed observation data
2. **`orbital_elements.txt`** - Calculated orbital elements
3. **`ephemeris.txt`** - Generated ephemeris for the observation period
4. **`residuals.txt`** - Residuals (observed vs calculated positions)

## Orbital Elements

The program calculates the following orbital elements:

- **Semi-major axis (a)** - Size of the orbit
- **Eccentricity (e)** - Shape of the orbit
- **Inclination (i)** - Tilt of the orbit plane
- **Longitude of ascending node (Ω)** - Orientation of the orbit
- **Argument of perihelion (ω)** - Orientation of the orbit's closest point
- **Mean anomaly (M)** - Position in the orbit
- **Period (T)** - Time to complete one orbit

## Key Differences from Oumuamua Project

1. **No gravitational acceleration** - Only considers the Sun's gravity
2. **Simplified force model** - Focuses on orbital mechanics
3. **MPC format** - Uses standard astronomical observation format
4. **2023 BU specific** - Tailored for this particular asteroid

## Accuracy and Limitations

- **Simplified model** - Does not account for planetary perturbations
- **Two-body problem** - Only considers Sun-asteroid interaction
- **No relativistic effects** - Uses Newtonian mechanics
- **Limited observations** - Accuracy depends on observation quality

## References

1. [Minor Planet Center](https://www.minorplanetcenter.net/)
2. [JPL Small-Body Database](https://ssd-api.jpl.nasa.gov/)
3. [SOFA Library](http://www.iausofa.org/)
4. [Asteroid 2023 BU Discovery](https://www.jpl.nasa.gov/news/asteroid-2023-bu-to-pass-very-close-to-earth)

## License

This project is for educational and research purposes. Please cite the original Oumuamua project if using this code as a reference.

## Contact

For questions about this project, please refer to the original Oumuamua orbit calculation project documentation.
