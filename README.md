# Robotic Wall Builder

This project implements an automated system to build a wall using a robotic arm. The system uses Arduino to control the arm's motors and Python with OpenCV for color-based cube detection.

## Features
- **Layer Building**: Builds layers of the wall using color-coded cubes (red, blue, green).
- **Camera-Based Detection**: Detects cubes using a camera and HSV color filtering.
- **Arduino Control**: Moves the robotic arm for cube manipulation.

## Repository Structure
robotic-wall-builder/ ├── arduino/ │ ├── wall_builder.ino # Arduino code controlling motors ├── python/ │ ├── build_red_layer.py # Code to build the red layer │ ├── build_blue_layer.py # Code to build the blue layer │ ├── build_green_layer.py # Code to build the green layer ├── README.md # Project description and instructions

## Requirements
- Python 3.x
- OpenCV
- Arduino IDE

## Usage

1. Arduino Setup:
- Upload arduino/wall_builder.ino to your Arduino.
2. Run Python Scripts:
- Use python/python_red_layer.py to build the red layer.
- Similarly for other layers.
