# AI-Based Autonomous Navigation System

A Python-based 2D robotics simulation demonstrating autonomous path planning, obstacle avoidance, and navigation performance evaluation using the A* search algorithm.

## Project Overview

This project simulates a virtual robot navigating a grid-based environment. The robot calculates a route from a starting position to a destination while avoiding obstacles.

The simulation provides visual feedback and performance metrics to help evaluate navigation behavior.

## Features

- Interactive 2D grid-world simulation
- A* path planning with eight-direction movement
- Obstacle-aware route calculation
- Diagonal corner-cutting prevention
- Interactive destination selection
- Dynamic obstacle placement and removal
- Automatic path replanning
- Navigation status and performance metrics
- Automated tests using pytest

## Technology Stack

- Python
- Pygame
- pytest
- Matplotlib (for future performance analysis)

## Project Structure

```text
AI-Based-Autonomous-Navigation-System/
├── main.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   └── navigation.py
└── tests/
    ├── test_navigation.py
    └── test_scenarios.py
```

## Installation

### Prerequisites

- Python 3.12 or a compatible Python version
- Git (optional, for cloning the repository)

### Setup

1. Clone the repository or download the project files.
2. Open a terminal inside the project directory.
3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate it.

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

5. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Simulation

```bash
python main.py
```

## Controls

| Control | Action |
|---|---|
| Left mouse click | Select a new destination |
| Right mouse click | Add or remove an obstacle |
| Spacebar | Pause or resume navigation |
| R | Recalculate the route |
| M | Reset the default map |
| Escape | Exit the simulation |

## Run Automated Tests

```bash
python -m pytest -v
```

The tests cover route finding, diagonal movement, obstacle avoidance, unreachable destinations, invalid coordinates, and scenario-based navigation.

Record the actual test result from your local environment before publishing this README.

## Performance Metrics

The simulator displays:

- Number of movement steps
- Calculated path cost
- Number of expanded search nodes
- Path planning time

Planning time depends on the computer, map, and obstacles. Measurements are indicative and should not be treated as universal performance guarantees.

## Current Limitations

- The environment is a 2D grid rather than a physically realistic 3D world.
- The robot does not use real sensors or camera-based perception.
- Navigation uses a classical search algorithm rather than a trained machine-learning model.
- Replanning currently begins at the original start position after map edits.
- The simulator does not model physical robot dynamics, wheel slip, or localization errors.

## Future Improvements

- Add performance graphs and CSV result exports.
- Implement robot localization and simulated range sensors.
- Add more advanced path-planning algorithms for comparison.
- Introduce ROS 2 and Gazebo integration as a future extension.
- Evaluate navigation performance across larger maps.

## Project Purpose

This project is intended for educational and portfolio purposes. It demonstrates fundamental concepts in robotics simulation, graph search, path planning, software testing, and engineering evaluation.
