# Makefile for Asteroid 2023 BU Orbit Calculation
# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++11 -Wall -O2
INCLUDES = -I./src
LIBS = -lsofa_c

# Directories
SRC_DIR = src
DATA_DIR = Data
RESULTS_DIR = results

# Source files
SOURCES = $(SRC_DIR)/main.cpp
OBJECTS = $(SOURCES:.cpp=.o)
TARGET = orbit_calculator

# Default target
all: $(TARGET)

# Build the main executable
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $(TARGET) $(OBJECTS) $(LIBS)

# Compile source files
$(SRC_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Create necessary directories
setup:
	mkdir -p $(DATA_DIR)
	mkdir -p $(RESULTS_DIR)

# Clean build files
clean:
	rm -f $(OBJECTS) $(TARGET)

# Clean all generated files
distclean: clean
	rm -rf $(RESULTS_DIR)/*

# Install SOFA library (if needed)
install-sofa:
	@echo "Please download and install SOFA library from:"
	@echo "http://www.iausofa.org/"
	@echo "Or use: sudo apt-get install libsofa1-dev (Ubuntu/Debian)"

# Run the program
run: $(TARGET)
	./$(TARGET)

# Help
help:
	@echo "Available targets:"
	@echo "  all          - Build the program (default)"
	@echo "  setup        - Create necessary directories"
	@echo "  clean        - Remove object files and executable"
	@echo "  distclean    - Remove all generated files"
	@echo "  install-sofa - Show SOFA library installation instructions"
	@echo "  run          - Build and run the program"
	@echo "  help         - Show this help message"

.PHONY: all setup clean distclean install-sofa run help
