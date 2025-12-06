# Quickstart Guide: Physical AI & Humanoid Robotics Textbook Project

This guide provides quick validation steps to ensure your development environment and core project components are set up correctly. Each step corresponds to a key independent test from the feature specification.

## 1. Validate ROS 2 Setup and Basic Robot Control

**Objective**: Verify the ROS 2 installation and the ability to control a simulated robot's joints and read sensor data.

**Scenario**:
1.  **Environment Setup**: Ensure ROS 2 Humble (or specified version) is installed and sourced in your environment.
2.  **Package Build**: Navigate to a sample ROS 2 package directory (e.g., `resources/code/module1-ros2/my_ros2_pkg`) and build it using `colcon build`.
3.  **Simulation Launch**: Launch a simple simulated robot (e.g., using a provided launch file in `resources/simulations/spawn_humanoid_world.launch.py`).
4.  **Control and Data Readout**: Run a test script or node that commands the robot's joints and logs data from its virtual sensors.
5.  **Expected Outcome**: The simulated robot's joints should move as commanded, and sensor data should be printed to the console without errors.

## 2. Validate Gazebo & Unity Digital Twin Simulation

**Objective**: Confirm the ability to run a Gazebo simulation with a humanoid robot and visualize it in Unity.

**Scenario**:
1.  **Gazebo Launch**: Launch the Gazebo simulation with a humanoid robot model (e.g., `resources/simulations/humanoid_world.world`).
2.  **Unity Visualization**: Open the Unity project (`resources/code/module2-unity/HumanoidViz`) and ensure it's configured to connect to the Gazebo simulation.
3.  **Basic Motion**: Trigger a basic motion in Gazebo (e.g., through a ROS 2 command or a simple script).
4.  **Expected Outcome**: The humanoid robot model should appear in Gazebo with physics enabled, and its motion should be accurately reflected in the Unity visualization. Simulated sensor data should be verifiable via ROS 2 topics.

## 3. Validate NVIDIA Isaac AI Brain Setup

**Objective**: Ensure NVIDIA Isaac Sim is correctly configured for basic AI perception and navigation tasks.

**Scenario**:
1.  **Isaac Sim Launch**: Launch NVIDIA Isaac Sim with a simulated environment containing objects and obstacles.
2.  **Perception Test**: Run a sample Isaac ROS perception project that identifies and locates objects within the simulated scene.
3.  **Navigation Test**: Use the Nav2 stack (or equivalent) within Isaac Sim to command the robot to navigate from a starting point to a goal, avoiding obstacles.
4.  **Expected Outcome**: The robot should successfully identify objects and autonomously navigate to the goal without collisions in Isaac Sim.

## 4. Validate Vision-Language-Action (VLA) Integration

**Objective**: Confirm the basic integration of voice commands, LLM planning, and robotic actions.

**Scenario**:
1.  **Microphone Setup**: Ensure your microphone is correctly configured and accessible by the system.
2.  **Whisper Integration**: Use a test script to capture a short voice command and process it via the OpenAI Whisper API, verifying accurate transcription.
3.  **LLM Planning**: Pass the transcribed text to the integrated LLM (e.g., GPT model) and verify that it returns a valid JSON array of robotic actions.
4.  **Action Execution**: Simulate the execution of one of the generated robotic actions (e.g., by logging the action command).
5.  **Expected Outcome**: Voice command is accurately transcribed, the LLM generates a sensible sequence of robot actions, and the system logs demonstrate the intended robotic action.

---

**Note**: This quickstart provides a high-level overview. Refer to individual module tutorials for detailed setup and verification procedures.