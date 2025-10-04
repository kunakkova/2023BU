#pragma once
#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <vector>
#include <iomanip>

class PlanetEphemeris 
{
public:
    struct format
    {
        double t; // in Julian format
        double x;
        double y;
        double z;
        double vx;
        double vy;
        double vz;
    };

    double GM;
    double step;
    std::vector<struct format> data;

    void init(std::string filename, double s)
    {
        step = s;
        std::ifstream input(filename);
        if (!input.is_open())
        {
            std::cout << "File cannot be opened: " << filename << std::endl;
            return;
        }

        struct format tmp;

        while (!input.eof())
        {
            input >> tmp.t >> tmp.x >> tmp.y >> tmp.z;
            if (filename == "Data/Earth.txt" || filename == "Data/RealOrbit.txt" || filename == "Data/2023BU_observations.txt")
                input >> tmp.vx >> tmp.vy >> tmp.vz;
            data.push_back(tmp);
        }

        input.close();
    }

    // getting coors for any moment as linear interpolation with two closest points
    void get_coors(double time, double &x, double &y, double &z)
    {
        int i = (int)((time - 2459960.0) / step) + 1; // Adjusted for 2023 BU timeframe
        if (i <= 0 || i >= data.size())
        {
            if (i <= 0) {
                x = data[0].x;
                y = data[0].y;
                z = data[0].z;
            } else {
                x = data[data.size()-1].x;
                y = data[data.size()-1].y;
                z = data[data.size()-1].z;
            }
            return;
        }

        x = (time - data[i - 1].t) * (data[i].x - data[i - 1].x) / (data[i].t - data[i - 1].t) + data[i - 1].x;
        y = (time - data[i - 1].t) * (data[i].y - data[i - 1].y) / (data[i].t - data[i - 1].t) + data[i - 1].y;
        z = (time - data[i - 1].t) * (data[i].z - data[i - 1].z) / (data[i].t - data[i - 1].t) + data[i - 1].z;
    }

    void get_speed (double time, double &vx, double &vy, double &vz)
    {
        int i = (int)((time - 2459960.0) / step) + 1;
        if (i <= 0 || i >= data.size())
        {
            if (i <= 0) {
                vx = data[0].vx;
                vy = data[0].vy;
                vz = data[0].vz;
            } else {
                vx = data[data.size()-1].vx;
                vy = data[data.size()-1].vy;
                vz = data[data.size()-1].vz;
            }
            return;
        }

        vx = (time - data[i - 1].t) * (data[i].vx - data[i - 1].vx) / (data[i].t - data[i - 1].t) + data[i - 1].vx;
        vy = (time - data[i - 1].t) * (data[i].vy - data[i - 1].vy) / (data[i].t - data[i - 1].t) + data[i - 1].vy;
        vz = (time - data[i - 1].t) * (data[i].vz - data[i - 1].vz) / (data[i].t - data[i - 1].t) + data[i - 1].vz;
    }
};

class TimeEphemeris 
{
public:
    struct format
    {
        double t; // in Julian format
        double dt;
    };

    std::vector<struct format> data;

    void init(std::string filename)
    {
        std::ifstream input(filename);
        if (!input.is_open())
        {
            std::cout << "File cannot be opened: " << filename << std::endl;
            return;
        }

        struct format tmp;

        while (!input.eof())
        {
            input >> tmp.t >> tmp.dt;
            data.push_back(tmp);
        }

        input.close();
    }

    // getting dt for any moment as linear interpolation with two closest points
    double get_dt(double time)
    {
        int i = (int)(time - 2459960.0) + 1;
        if (i <= 0)
        {
            return data[0].dt;
        }
        if (i >= data.size())
        {
            return data[data.size()-1].dt;
        }

        return (time - data[i - 1].t) * (data[i].dt - data[i - 1].dt) / (data[i].t - data[i - 1].t) + data[i - 1].dt;
    }
};
