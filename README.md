# Drone Simulator

A 3D drone flight simulator built with Python and the Ursina Engine.

## Features

- Realistic drone physics simulation
- Intuitive controls
- 3D environment with obstacles
- Real-time flight data display
- Battery simulation
- Collision detection

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required packages:
```bash
pip install ursina
```

## Controls

- W/S: Pitch forward/backward
- A/D: Roll left/right
- Q: Increase thrust
- E: Decrease thrust
- Shift + Q/E: Yaw left/right

## Running the Simulator

Simply run the main.py file:
```bash
python main.py
```

## Project Structure

- `main.py`: Main application entry point
- `drone.py`: Drone physics and properties
- `controls.py`: User input handling
- `environment.py`: 3D environment setup
- `assets/`: Directory for models, textures, and audio files

## Development

The simulator is built using the Ursina Engine, which provides:
- 3D rendering capabilities
- Physics simulation
- Input handling
- Collision detection
- Lighting and shadows

## License

MIT License 