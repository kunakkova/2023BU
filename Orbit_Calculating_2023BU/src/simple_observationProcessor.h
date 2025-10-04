#pragma once
#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <iomanip>
#include <sstream>
#include "Ephemeris.h"

#define EARTH_RADIUS 6378.140 // km
#define SEC_DAY 86400.0 
#define MINSEC_DAY 86400000.0

// Simple Julian date calculation without SOFA
double simple_julian_date(int year, int month, int day, int hour, int minute, double second)
{
    if (month <= 2) {
        year -= 1;
        month += 12;
    }
    
    int a = year / 100;
    int b = 2 - a + a / 4;
    
    double jd = (int)(365.25 * (year + 4716)) + (int)(30.6001 * (month + 1)) + day + b - 1524.5;
    jd += (hour + minute / 60.0 + second / 3600.0) / 24.0;
    
    return jd;
}

class SimpleObservationProcessor
{
public:
    struct Observation
    {
        double time;        // Julian date
        double ra;          // Right Ascension (radians)
        double dec;         // Declination (radians)
        double observer_x;  // Observer position X (km)
        double observer_y;  // Observer position Y (km)
        double observer_z;  // Observer position Z (km)
    };

    std::vector<Observation> observations;

    // Process observations from MPC format file
    void processMPCObservations(const std::string& filename)
    {
        std::ifstream input(filename);
        if (!input.is_open())
        {
            std::cout << "Cannot open observations file: " << filename << std::endl;
            return;
        }

        std::string line;
        while (std::getline(input, line))
        {
            if (line.empty() || line[0] == '#') continue;
            
            Observation obs;
            if (parseMPCLine(line, obs))
            {
                observations.push_back(obs);
            }
        }
        
        input.close();
        std::cout << "Processed " << observations.size() << " observations" << std::endl;
    }

    // Save processed observations to file
    void saveProcessedObservations(const std::string& filename)
    {
        std::ofstream output(filename);
        output.setf(std::ios::scientific);
        
        for (const auto& obs : observations)
        {
            output << std::setprecision(15) 
                   << obs.time << ' ' 
                   << obs.ra << ' ' 
                   << obs.dec << ' '
                   << obs.observer_x << ' '
                   << obs.observer_y << ' '
                   << obs.observer_z << std::endl;
        }
        
        output.close();
    }

private:
    bool parseMPCLine(const std::string& line, Observation& obs)
    {
        // MPC format parser
        // Format: YYYY MM DD.dddddd HH MM SS.sss HH MM SS.sss
        std::istringstream iss(line);
        
        int year, month;
        double day_frac;
        int ra_h, ra_m;
        double ra_s;
        int dec_d, dec_m;
        double dec_s;
        
        if (!(iss >> year >> month >> day_frac >> ra_h >> ra_m >> ra_s >> dec_d >> dec_m >> dec_s))
        {
            return false;
        }
        
        // Convert to Julian date using simple calculation
        int day = (int)day_frac;
        double day_fraction = day_frac - day;
        
        // Convert day fraction to hours, minutes, seconds
        double total_hours = day_fraction * 24.0;
        int hours = (int)total_hours;
        double remaining_minutes = (total_hours - hours) * 60.0;
        int minutes = (int)remaining_minutes;
        double seconds = (remaining_minutes - minutes) * 60.0;
        
        obs.time = simple_julian_date(year, month, day, hours, minutes, seconds);
        
        // Convert coordinates to radians
        obs.ra = (ra_h + ra_m/60.0 + ra_s/3600.0) * M_PI / 180.0;
        obs.dec = (abs(dec_d) + dec_m/60.0 + dec_s/3600.0) * M_PI / 180.0;
        if (dec_d < 0) obs.dec = -obs.dec;
        
        // For now, set observer position to Earth center
        // In real implementation, this should be calculated from observatory coordinates
        obs.observer_x = obs.observer_y = obs.observer_z = 0.0;
        
        return true;
    }
};
