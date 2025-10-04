#!/usr/bin/env python3
"""
Script to download real observational data for asteroid 2023 BU
from the Minor Planet Center (MPC) database.
"""

import requests
import re
import sys
from datetime import datetime

def download_mpc_data():
    """
    Download observational data for 2023 BU from MPC
    """
    print("Downloading 2023 BU observational data from MPC...")
    
    # Direct URL to the observation data file
    url = "https://www.minorplanetcenter.net/tmp2/2023_BU.txt"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        content = response.text
        lines = content.split('\n')
        
        # Use the same parsing logic as simple_mpc_parser.py
        observations = []
        for line in lines:
            obs_line = parse_mpc_line_simple(line)
            if obs_line:
                observations.append(obs_line)
        
        if observations:
            print(f"Found {len(observations)} observations")
            
            # Save to file
            with open('Data/2023BU_observations.txt', 'w') as f:
                f.write("# Asteroid 2023 BU Observations from MPC\n")
                f.write("# Downloaded on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                f.write("# Format: YYYY MM DD.dddddd HH MM SS.sss HH MM SS.sss\n")
                f.write("# Source: https://www.minorplanetcenter.net/tmp2/2023_BU.txt\n\n")
                
                for obs in observations:
                    f.write(obs + '\n')
            
            print("Data saved to Data/2023BU_observations.txt")
            return True
        else:
            print("No observations found in MPC response")
            print("Please manually download data from:")
            print("https://www.minorplanetcenter.net/tmp2/2023_BU.txt")
            return False
            
    except requests.RequestException as e:
        print(f"Error downloading data: {e}")
        print("Please manually download data from:")
        print("https://www.minorplanetcenter.net/tmp2/2023_BU.txt")
        return False

def parse_mpc_line_simple(line):
    """
    Simple MPC line parser (same as in simple_mpc_parser.py)
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    
    # Try different patterns to match various MPC formats
    patterns = [
        # Pattern 1: C2023 01 21.34299109 50 04.192+43 47 13.29
        r'C2023\s+(\d{1,2})\s+(\d{1,2}\.\d+)\s+(\d{1,2})\s+(\d{1,2})\s+([\d.]+)([+-]\d{1,2})\s+(\d{1,2})\s+([\d.]+)',
        # Pattern 2: C2023 01 21.99514 09 48 47.36 +43 41 03.0
        r'C2023\s+(\d{1,2})\s+(\d{1,2}\.\d+)\s+(\d{1,2})\s+(\d{1,2})\s+([\d.]+)\s+([+-]\d{1,2})\s+(\d{1,2})\s+([\d.]+)',
        # Pattern 3: C2023 01 22.03881109 49 06.64 +43 40 38.7
        r'C2023\s+(\d{1,2})\s+(\d{1,2}\.\d+)(\d{1,2})\s+(\d{1,2})\s+([\d.]+)\s+([+-]\d{1,2})\s+(\d{1,2})\s+([\d.]+)',
        # Pattern 4: C2023 01 22.08618109 48 43.678+43 38 19.86
        r'C2023\s+(\d{1,2})\s+(\d{1,2}\.\d+)(\d{1,2})\s+(\d{1,2})\s+([\d.]+)([+-]\d{1,2})\s+(\d{1,2})\s+([\d.]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            try:
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
                
                # Format: YYYY MM DD.dddddd HH MM SS.sss HH MM SS.sss
                obs_line = f"{year} {month:02d} {day_frac:.6f} {ra_h:02d} {ra_m:02d} {ra_s:06.3f} {dec_d:+03d} {dec_m:02d} {dec_s:05.2f}"
                return obs_line
                
            except (ValueError, IndexError):
                continue
    
    return None

def download_jpl_data():
    """
    Download orbital elements from JPL Small-Body Database
    """
    print("Downloading 2023 BU orbital elements from JPL...")
    
    url = "https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2023BU"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'orbital_data' in data:
            orbital_data = data['orbital_data']
            
            # Save orbital elements
            with open('Data/2023BU_jpl_elements.txt', 'w') as f:
                f.write("# Asteroid 2023 BU Orbital Elements from JPL\n")
                f.write("# Downloaded on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                f.write("# Source: https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2023BU\n\n")
                
                if 'elements' in orbital_data:
                    elements = orbital_data['elements']
                    for key, value in elements.items():
                        if isinstance(value, dict) and 'value' in value:
                            f.write(f"# {key}: {value['value']} {value.get('unit', '')}\n")
            
            print("JPL orbital elements saved to Data/2023BU_jpl_elements.txt")
            return True
        else:
            print("No orbital data found in JPL response")
            return False
            
    except requests.RequestException as e:
        print(f"Error downloading JPL data: {e}")
        return False

def main():
    print("=== 2023 BU Data Downloader ===")
    print()
    
    # Download MPC observations
    mpc_success = download_mpc_data()
    print()
    
    # Download JPL orbital elements
    jpl_success = download_jpl_data()
    print()
    
    if mpc_success or jpl_success:
        print("Data download completed!")
        print()
        print("Next steps:")
        print("1. Review the downloaded data files")
        print("2. Run: make setup")
        print("3. Run: make")
        print("4. Run: make run")
    else:
        print("Data download failed!")
        print()
        print("Please manually download data from:")
        print("- MPC: https://www.minorplanetcenter.net/db_search/show_object?object_id=2023+BU")
        print("- JPL: https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2023BU")
        print()
        print("Save the data in the appropriate format in the Data/ directory")

if __name__ == "__main__":
    main()
