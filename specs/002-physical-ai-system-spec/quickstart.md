# Quickstart: Physical AI System Development Environment

This guide provides the steps to set up a local development environment for the Physical AI System project.

## Prerequisites

- Ubuntu 22.04 LTS
- NVIDIA GPU with at least 8GB VRAM (RTX 3070 or higher recommended)
- NVIDIA Driver version 525.60.11 or later
- At least 32GB RAM
- At least 100GB free disk space

## 1. Install ROS 2 Humble

Follow the official ROS 2 Humble installation guide:
[https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)

Make sure to source the setup file in your `.bashrc`:
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## 2. Install NVIDIA Isaac Sim

1.  Download and install the NVIDIA Omniverse Launcher:
    [https://www.nvidia.com/en-us/omniverse/download/](https://www.nvidia.com/en-us/omniverse/download/)
2.  From the Omniverse Launcher, install "Isaac Sim" (use version 2023.1.1 or later).
3.  Inside Isaac Sim, go to `Window -> Extensions` and ensure the `omni.isaac.ros2_bridge` extension is enabled.

## 3. Set up the ROS 2 Workspace

1.  Clone this repository.
2.  Create and build the ROS 2 workspace:
    ```bash
    cd /path/to/this/repository/src/ros2_ws
    colcon build
    ```
3.  Source the new workspace in your `.bashrc` **after** the main ROS 2 setup:
    ```bash
    echo "source /path/to/this/repository/src/ros2_ws/install/setup.bash" >> ~/.bashrc
    source ~/.bashrc
    ```

## 4. Running the Simulation

1.  Launch Isaac Sim from the Omniverse Launcher.
2.  Open the main simulation world file (path to be determined).
3.  In a terminal, launch the ROS 2 control nodes:
    ```bash
    # Example launch command
    ros2 launch humanoid_control main.launch.py
    ```

You should now have a running simulation with the humanoid robot connected to the ROS 2 control system.
