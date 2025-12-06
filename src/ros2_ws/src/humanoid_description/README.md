# Humanoid Description Package

This package contains the Unified Robot Description Format (URDF) models and associated assets for the humanoid robot. It also provides launch files to publish the robot state and visualize it in RViz2.

## Contents

- `urdf/humanoid.urdf`: The main URDF file describing the robot's kinematics, dynamics, and visual properties.
- `launch/view_robot.launch.py`: A launch file to start `robot_state_publisher`, `joint_state_publisher_gui`, and `rviz2` for visualization.

## Usage

To view the robot model in RViz2:

```bash
ros2 launch humanoid_description view_robot.launch.py
```

## Dependencies

- `humanoid_interfaces` (indirectly for common types if any)
- `robot_state_publisher`
- `joint_state_publisher_gui`
- `rviz2`
