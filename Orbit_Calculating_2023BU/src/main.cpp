#include "Ephemeris.h"
#include "observationProcessor.h"
#include "orbitCalculator.h"
#include <iostream>
#include <fstream>
#include <vector>

int main()
{
    std::cout << "=== Asteroid 2023 BU Orbit Calculation ===" << std::endl;
    std::cout << "Calculating orbit from real observations" << std::endl;
    std::cout << std::endl;

    // Initialize observation processor
    ObservationProcessor processor;
    
    // Process observations from MPC format
    std::cout << "Processing observations..." << std::endl;
    processor.processMPCObservations("Data/2023BU_observations.txt");
    
    if (processor.observations.empty())
    {
        std::cout << "No observations found. Please check the data file." << std::endl;
        std::cout << "Expected format: YYYY MM DD.dddddd HH MM SS.sss HH MM SS.sss" << std::endl;
        return 1;
    }
    
    // Save processed observations
    processor.saveProcessedObservations("results/processed_observations.txt");
    std::cout << "Processed observations saved to results/processed_observations.txt" << std::endl;
    
    // Initialize orbit calculator
    OrbitCalculator calculator;
    
    // Determine orbital elements from observations
    std::cout << "Determining orbital elements..." << std::endl;
    OrbitCalculator::OrbitalElements elements = calculator.determineOrbit(processor.observations);
    
    // Display orbital elements
    std::cout << std::endl;
    std::cout << "=== Orbital Elements ===" << std::endl;
    std::cout << "Semi-major axis: " << elements.a << " AU" << std::endl;
    std::cout << "Eccentricity: " << elements.e << std::endl;
    std::cout << "Inclination: " << elements.i * 180.0 / M_PI << " degrees" << std::endl;
    std::cout << "Longitude of ascending node: " << elements.Omega * 180.0 / M_PI << " degrees" << std::endl;
    std::cout << "Argument of perihelion: " << elements.omega * 180.0 / M_PI << " degrees" << std::endl;
    std::cout << "Mean anomaly: " << elements.M * 180.0 / M_PI << " degrees" << std::endl;
    std::cout << "Period: " << elements.T << " days" << std::endl;
    
    // Save orbital elements
    calculator.saveOrbitalElements(elements, "results/orbital_elements.txt");
    std::cout << "Orbital elements saved to results/orbital_elements.txt" << std::endl;
    
    // Generate ephemeris for comparison
    std::cout << std::endl;
    std::cout << "Generating ephemeris..." << std::endl;
    
    std::ofstream ephemeris("results/ephemeris.txt");
    ephemeris.setf(std::ios::scientific);
    ephemeris << "# Time(JD) X(km) Y(km) Z(km) VX(km/s) VY(km/s) VZ(km/s)" << std::endl;
    
    // Generate ephemeris for the observation period
    double start_time = processor.observations[0].time;
    double end_time = processor.observations[processor.observations.size()-1].time;
    double step = 0.1; // 0.1 day steps
    
    for (double t = start_time; t <= end_time; t += step)
    {
        OrbitCalculator::StateVector state = calculator.elementsToStateVector(elements, t);
        
        ephemeris << std::setprecision(15) 
                  << t << ' '
                  << state.x << ' ' << state.y << ' ' << state.z << ' '
                  << state.vx << ' ' << state.vy << ' ' << state.vz << std::endl;
    }
    
    ephemeris.close();
    std::cout << "Ephemeris saved to results/ephemeris.txt" << std::endl;
    
    // Calculate residuals (difference between observed and calculated positions)
    std::cout << std::endl;
    std::cout << "Calculating residuals..." << std::endl;
    
    std::ofstream residuals("results/residuals.txt");
    residuals.setf(std::ios::scientific);
    residuals << "# Time(JD) Obs_RA(rad) Obs_Dec(rad) Calc_RA(rad) Calc_Dec(rad) RA_Res(rad) Dec_Res(rad)" << std::endl;
    
    double total_ra_residual = 0.0;
    double total_dec_residual = 0.0;
    int count = 0;
    
    for (const auto& obs : processor.observations)
    {
        OrbitCalculator::StateVector state = calculator.elementsToStateVector(elements, obs.time);
        
        // Convert state vector to RA/Dec (simplified)
        double calc_ra = atan2(state.y, state.x);
        double calc_dec = atan2(state.z, sqrt(state.x*state.x + state.y*state.y));
        
        double ra_residual = obs.ra - calc_ra;
        double dec_residual = obs.dec - calc_dec;
        
        // Normalize residuals to [-π, π]
        while (ra_residual > M_PI) ra_residual -= 2*M_PI;
        while (ra_residual < -M_PI) ra_residual += 2*M_PI;
        while (dec_residual > M_PI) dec_residual -= 2*M_PI;
        while (dec_residual < -M_PI) dec_residual += 2*M_PI;
        
        residuals << std::setprecision(15) 
                  << obs.time << ' '
                  << obs.ra << ' ' << obs.dec << ' '
                  << calc_ra << ' ' << calc_dec << ' '
                  << ra_residual << ' ' << dec_residual << std::endl;
        
        total_ra_residual += fabs(ra_residual);
        total_dec_residual += fabs(dec_residual);
        count++;
    }
    
    residuals.close();
    
    double mean_ra_residual = total_ra_residual / count;
    double mean_dec_residual = total_dec_residual / count;
    
    std::cout << "Mean RA residual: " << mean_ra_residual * 180.0 / M_PI * 3600.0 << " arcseconds" << std::endl;
    std::cout << "Mean Dec residual: " << mean_dec_residual * 180.0 / M_PI * 3600.0 << " arcseconds" << std::endl;
    std::cout << "Residuals saved to results/residuals.txt" << std::endl;
    
    std::cout << std::endl;
    std::cout << "=== Calculation Complete ===" << std::endl;
    std::cout << "Results saved in the 'results' directory" << std::endl;
    
    return 0;
}
