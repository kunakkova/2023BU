#pragma once
#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <vector>
#include <iomanip>
#include "Ephemeris.h"
#include "observationProcessor.h"

#define GMS  132712440043.85333 // Sun gravitational parameter
#define KM_TO_AU 6.68459e-9    // 1 km = .. au
#define AU_TO_KM 1.495978707e8 // 1 AU = .. km

class OrbitCalculator
{
public:
    struct OrbitalElements
    {
        double a;        // Semi-major axis (AU)
        double e;        // Eccentricity
        double i;        // Inclination (radians)
        double Omega;    // Longitude of ascending node (radians)
        double omega;    // Argument of perihelion (radians)
        double M;        // Mean anomaly (radians)
        double T;        // Period (days)
    };

    struct StateVector
    {
        double x, y, z;      // Position (km)
        double vx, vy, vz;   // Velocity (km/s)
    };

    // Calculate orbital elements from state vector
    OrbitalElements stateVectorToElements(const StateVector& state)
    {
        OrbitalElements elements;
        
        // Convert position to AU
        double r_x = state.x * KM_TO_AU;
        double r_y = state.y * KM_TO_AU;
        double r_z = state.z * KM_TO_AU;
        
        // Convert velocity to AU/day
        double v_x = state.vx * 86400.0 * KM_TO_AU;
        double v_y = state.vy * 86400.0 * KM_TO_AU;
        double v_z = state.vz * 86400.0 * KM_TO_AU;
        
        // Calculate orbital elements
        double r = sqrt(r_x*r_x + r_y*r_y + r_z*r_z);
        double v2 = v_x*v_x + v_y*v_y + v_z*v_z;
        
        // Specific angular momentum
        double h_x = r_y*v_z - r_z*v_y;
        double h_y = r_z*v_x - r_x*v_z;
        double h_z = r_x*v_y - r_y*v_x;
        double h = sqrt(h_x*h_x + h_y*h_y + h_z*h_z);
        
        // Semi-major axis
        elements.a = 1.0 / (2.0/r - v2/GMS);
        
        // Eccentricity
        double energy = v2/2.0 - GMS/r;
        double e2 = 1.0 + 2.0*energy*h*h/(GMS*GMS);
        elements.e = sqrt(e2);
        
        // Inclination
        elements.i = acos(h_z/h);
        
        // Longitude of ascending node
        elements.Omega = atan2(h_x, -h_y);
        if (elements.Omega < 0) elements.Omega += 2*M_PI;
        
        // Argument of perihelion
        double n_x = -h_y;
        double n_y = h_x;
        double n = sqrt(n_x*n_x + n_y*n_y);
        
        double cos_omega = (n_x*(r_x*v2/GMS - r_x) + n_y*(r_y*v2/GMS - r_y)) / (n * elements.e * r);
        double sin_omega = (r_z/elements.e) * sqrt(1 - cos_omega*cos_omega);
        elements.omega = atan2(sin_omega, cos_omega);
        if (elements.omega < 0) elements.omega += 2*M_PI;
        
        // Mean anomaly
        double cos_E = (1 - r/elements.a) / elements.e;
        double sin_E = (r_x*v_x + r_y*v_y + r_z*v_z) / (sqrt(GMS*elements.a) * elements.e);
        double E = atan2(sin_E, cos_E);
        elements.M = E - elements.e * sin(E);
        if (elements.M < 0) elements.M += 2*M_PI;
        
        // Period
        elements.T = 2*M_PI * sqrt(elements.a*elements.a*elements.a / GMS);
        
        return elements;
    }

    // Calculate state vector from orbital elements
    StateVector elementsToStateVector(const OrbitalElements& elements, double time)
    {
        StateVector state;
        
        // Solve Kepler's equation for eccentric anomaly
        double E = solveKeplerEquation(elements.M, elements.e);
        
        // Calculate position in orbital plane
        double x_orb = elements.a * (cos(E) - elements.e);
        double y_orb = elements.a * sqrt(1 - elements.e*elements.e) * sin(E);
        double z_orb = 0.0;
        
        // Calculate velocity in orbital plane
        double n = sqrt(GMS / (elements.a*elements.a*elements.a));
        double sin_E = sin(E);
        double cos_E = cos(E);
        double factor = n / (1 - elements.e * cos_E);
        
        double vx_orb = -elements.a * n * sin_E * factor;
        double vy_orb = elements.a * n * sqrt(1 - elements.e*elements.e) * cos_E * factor;
        double vz_orb = 0.0;
        
        // Transform to 3D space
        double cos_omega = cos(elements.omega);
        double sin_omega = sin(elements.omega);
        double cos_Omega = cos(elements.Omega);
        double sin_Omega = sin(elements.Omega);
        double cos_i = cos(elements.i);
        double sin_i = sin(elements.i);
        
        // Position
        double x1 = x_orb * cos_omega - y_orb * sin_omega;
        double y1 = x_orb * sin_omega + y_orb * cos_omega;
        double z1 = 0.0;
        
        state.x = (x1 * cos_Omega - y1 * sin_Omega * cos_i) * AU_TO_KM;
        state.y = (x1 * sin_Omega + y1 * cos_Omega * cos_i) * AU_TO_KM;
        state.z = y1 * sin_i * AU_TO_KM;
        
        // Velocity
        double vx1 = vx_orb * cos_omega - vy_orb * sin_omega;
        double vy1 = vx_orb * sin_omega + vy_orb * cos_omega;
        double vz1 = 0.0;
        
        state.vx = (vx1 * cos_Omega - vy1 * sin_Omega * cos_i) * AU_TO_KM / 86400.0;
        state.vy = (vx1 * sin_Omega + vy1 * cos_Omega * cos_i) * AU_TO_KM / 86400.0;
        state.vz = vy1 * sin_i * AU_TO_KM / 86400.0;
        
        return state;
    }

    // Simple orbit determination from observations (Gauss method)
    OrbitalElements determineOrbit(const std::vector<ObservationProcessor::Observation>& obs)
    {
        if (obs.size() < 3)
        {
            std::cout << "Need at least 3 observations for orbit determination" << std::endl;
            return OrbitalElements{0, 0, 0, 0, 0, 0, 0};
        }
        
        // Use first, middle, and last observations
        const auto& obs1 = obs[0];
        const auto& obs2 = obs[obs.size()/2];
        const auto& obs3 = obs[obs.size()-1];
        
        // Convert observations to state vectors (simplified)
        // This is a placeholder - real implementation would use proper Gauss method
        StateVector state;
        
        // For demonstration, use approximate values for 2023 BU
        // These would be calculated from the observations
        state.x = 1.0e8;  // km
        state.y = 1.0e8;  // km
        state.z = 1.0e7;  // km
        state.vx = 30.0;  // km/s
        state.vy = 20.0;  // km/s
        state.vz = 5.0;   // km/s
        
        return stateVectorToElements(state);
    }

    // Save orbital elements to file
    void saveOrbitalElements(const OrbitalElements& elements, const std::string& filename)
    {
        std::ofstream output(filename);
        output.setf(std::ios::scientific);
        
        output << "# Orbital Elements for 2023 BU" << std::endl;
        output << "# Semi-major axis (AU): " << elements.a << std::endl;
        output << "# Eccentricity: " << elements.e << std::endl;
        output << "# Inclination (deg): " << elements.i * 180.0 / M_PI << std::endl;
        output << "# Longitude of ascending node (deg): " << elements.Omega * 180.0 / M_PI << std::endl;
        output << "# Argument of perihelion (deg): " << elements.omega * 180.0 / M_PI << std::endl;
        output << "# Mean anomaly (deg): " << elements.M * 180.0 / M_PI << std::endl;
        output << "# Period (days): " << elements.T << std::endl;
        
        output.close();
    }

private:
    // Solve Kepler's equation: M = E - e*sin(E)
    double solveKeplerEquation(double M, double e)
    {
        double E = M; // Initial guess
        double delta = 1.0;
        int max_iter = 100;
        int iter = 0;
        
        while (fabs(delta) > 1e-10 && iter < max_iter)
        {
            delta = (M - (E - e * sin(E))) / (1 - e * cos(E));
            E += delta;
            iter++;
        }
        
        return E;
    }
};
