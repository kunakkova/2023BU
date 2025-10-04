#!/usr/bin/env python3
"""
Simple script to parse MPC observation data for asteroid 2023 BU
and convert it to our format.
"""

import re
from datetime import datetime

def parse_mpc_line(line):
    """
    Parse a single MPC observation line
    Format: K23B00U  C2023 01 21.34299109 50 04.192+43 47 13.29         21.19RU~6CJqI41
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    
    # Look for the pattern: C2023 MM DD.dddddd HH MM SS.sss±DD MM SS.ss
    # More flexible pattern to handle various formats
    pattern = r'C2023\s+(\d{1,2})\s+(\d{1,2}\.\d+)\s+(\d{1,2})\s+(\d{1,2})\s+([\d.]+)([+-]\d{1,2})\s+(\d{1,2})\s+([\d.]+)'
    
    # Alternative pattern for lines without spaces between RA components
    pattern2 = r'C2023\s+(\d{1,2})\s+(\d{1,2}\.\d+)(\d{1,2})\s+(\d{1,2})\s+([\d.]+)([+-]\d{1,2})\s+(\d{1,2})\s+([\d.]+)'
    match = re.search(pattern, line)
    
    if not match:
        # Try alternative pattern
        match = re.search(pattern2, line)
        if not match:
            return None
    
    month = int(match.group(1))
    day_frac = float(match.group(2))
    ra_h = int(match.group(3))
    ra_m = int(match.group(4))
    ra_s = float(match.group(5))
    dec_d = int(match.group(6))  # includes sign
    dec_m = int(match.group(7))
    dec_s = float(match.group(8))
    
    # Convert to our format
    year = 2023
    day = int(day_frac)
    day_fraction = day_frac - day
    
    # Format: YYYY MM DD.dddddd HH MM SS.sss HH MM SS.sss
    obs_line = f"{year} {month:02d} {day_frac:.6f} {ra_h:02d} {ra_m:02d} {ra_s:06.3f} {dec_d:+03d} {dec_m:02d} {dec_s:05.2f}"
    
    return obs_line

def main():
    print("=== MPC Data Parser for 2023 BU ===")
    print("Parsing observation data...")
    
    # Sample data from the provided URL
    sample_data = """K23B00U  C2023 01 21.34299109 50 04.192+43 47 13.29         21.19RU~6CJqI41
K23B00U  C2023 01 21.44005909 49 14.025+43 47 08.78         20.15RU~6CJqI41
K23B00U*KC2023 01 21.99514 09 48 47.36 +43 41 03.0          19.5 GX~6CJqL51
K23B00U KC2023 01 21.99661 09 48 46.67 +43 41 02.0          19.5 GX~6CJqL51
K23B00U KC2023 01 21.99806 09 48 45.90 +43 41 00.8          19.6 GX~6CJqL51
K23B00U KC2023 01 22.03881109 49 06.64 +43 40 38.7 X~6CJqI93
K23B00U KC2023 01 22.04159209 49 05.13 +43 40 40.4 19.2 GX~6CJqI93
K23B00U KC2023 01 22.04418409 49 03.81 +43 40 40.8 19.5 GX~6CJqI93
K23B00U KC2023 01 22.08105 09 48 04.79 +43 38 43.2 19.6 GX~6CJqL51
K23B00U KC2023 01 22.08270 09 48 04.02 +43 38 39.0 19.2 GX~6CJqL51
K23B00U KC2023 01 22.08435 09 48 03.29 +43 38 34.8 19.4 GX~6CJqL51
K23B00U KC2023 01 22.08618109 48 43.678+43 38 19.86 19.7 GV~6CJqJ95
K23B00U KC2023 01 22.09241009 48 40.759+43 38 16.26 19.9 GV~6CJqJ95
K23B00U KC2023 01 22.09552709 48 39.218+43 38 13.70 19.9 GV~6CJqJ95
K23B00U KC2023 01 22.15423709 50 02.66 +43 35 01.8 20.0 GX~6CJq858
K23B00U KC2023 01 22.16243309 50 00.98 +43 35 28.7 19.9 GX~6CJq858
K23B00U KC2023 01 22.17257309 49 58.69 +43 36 02.4 20.2 GX~6CJq858
K23B00U KB2023 01 22.20101409 49 49.826+43 37 32.39 19.3 GX~6CJqV28
K23B00U C2023 01 22.39571309 48 12.380+43 42 22.39 19.78GV~6CJqV00
K23B00U C2023 01 22.40069709 48 09.094+43 42 17.89 19.83GV~6CJqV00
K23B00U C2023 01 22.40566109 48 05.789+43 42 12.92 20.04GV~6CJqV00
K23B00U C2023 01 22.41062509 48 02.506+43 42 07.09 19.83GV~6CJqV00
K23B00U C2023 01 22.44478909 47 40.250+43 41 09.38 20.01GV~6CJqV00
K23B00U C2023 01 22.44977609 47 37.090+43 40 58.30 20.14GV~6CJqV00
K23B00U C2023 01 22.45474109 47 33.940+43 40 46.49 20.18GV~6CJqV00
K23B00U C2023 01 22.45970509 47 30.872+43 40 34.28 20.29GV~6CJqV00
K23B00U KC2023 01 23.05401509 47 07.84 +43 31 54.8 19.3 GX~6CJqC95
K23B00U KC2023 01 23.07198609 46 55.43 +43 31 37.2 19.5 GX~6CJqC95
K23B00U 1C2023 01 23.35629109 46 39.695+43 32 38.87 20.09GV~6CJq703
K23B00U 1C2023 01 23.36633609 46 31.138+43 32 35.34 V~6CJq703
K23B00U 1C2023 01 23.37135709 46 26.900+43 32 31.52 19.52GV~6CJq703
K23B00U KC2023 01 23.37635 09 46 43.166+43 28 25.64 17.7 GV~6CJqU52
K23B00U KC2023 01 23.37938 09 46 40.831+43 28 25.82 19.6 GV~6CJqU52
K23B00U KC2023 01 23.39612 09 46 27.931+43 28 23.23 19.2 GV~6CJqU52
K23B00U KC2023 01 23.40215 09 46 23.328+43 28 17.15 19.2 GV~6CJqU52
K23B00U C2023 01 23.40817909 47 27.761+43 34 06.46 18.77oV~8AkQT05
K23B00U C2023 01 23.40998509 47 26.345+43 34 11.32 19.02oV~8AkQT05
K23B00U C2023 01 23.41315009 47 23.878+43 34 18.52 19.09oV~8AkQT05
K23B00U C2023 01 23.41904409 47 18.986+43 34 32.20 19.07oV~8AkQT05
K23B00U C2023 01 23.48214509 46 22.433+43 35 41.62 19.02GV~6CJqF52
K23B00U KC2023 01 23.99034009 45 19.997+43 11 44.77 18.8 GV~6CJqJ95
K23B00U KC2023 01 23.99271309 45 18.269+43 11 45.96 18.8 GV~6CJqJ95
K23B00U KC2023 01 23.99504109 45 16.507+43 11 48.05 19.0 GV~6CJqJ95
K23B00U KC2023 01 23.99738609 45 14.743+43 11 49.49 19.4 GV~6CJqJ95"""
    
    observations = []
    lines = sample_data.split('\n')
    
    for line in lines:
        obs_line = parse_mpc_line(line)
        if obs_line:
            observations.append(obs_line)
    
    if observations:
        print(f"Successfully parsed {len(observations)} observations")
        
        # Save to file
        with open('Data/2023BU_observations.txt', 'w') as f:
            f.write("# Asteroid 2023 BU Observations from MPC\n")
            f.write("# Parsed on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.write("# Format: YYYY MM DD.dddddd HH MM SS.sss HH MM SS.sss\n")
            f.write("# Source: https://www.minorplanetcenter.net/tmp2/2023_BU.txt\n\n")
            
            for obs in observations:
                f.write(obs + '\n')
        
        print("Data saved to Data/2023BU_observations.txt")
        print("\nFirst few observations:")
        for i, obs in enumerate(observations[:5]):
            print(f"  {i+1}: {obs}")
        
        return True
    else:
        print("No observations found!")
        return False

if __name__ == "__main__":
    main()
