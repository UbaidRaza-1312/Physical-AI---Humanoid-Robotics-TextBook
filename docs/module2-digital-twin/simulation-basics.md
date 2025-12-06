---
id: simulation-basics
title: Robot Simulation with Gazebo & Unity
---

Welcome to Module 2, where you will explore the fascinating world of **robot simulation** using a powerful combination of **Gazebo** for realistic physics and sensor emulation, and **Unity** for high-fidelity visualization. This module will guide you through creating a "digital twin" of a humanoid robot, allowing you to test complex behaviors in a safe, controlled, and reproducible environment.

## The Importance of Digital Twins

A digital twin is a virtual replica of a physical system. In robotics, this concept is invaluable for:
-   **Safe Testing**: Experimenting with robot behaviors without risk to physical hardware or humans.
-   **Cost Reduction**: Developing and iterating on designs without needing expensive physical prototypes.
-   **Accelerated Development**: Running simulations much faster than real-time or in parallel.
-   **Reproducibility**: Ensuring experiments can be run identically multiple times.
-   **Synthetic Data Generation**: Creating vast amounts of labeled data for training AI models, especially useful for perception tasks where real-world data collection is difficult or dangerous.

## Gazebo: The Physics Engine

**Gazebo** is a robust 3D robotics simulator widely used in research and industry. It provides:
-   **Accurate Physics**: Simulates gravity, collisions, friction, and rigid body dynamics.
-   **Extensive Sensor Emulation**: Supports a wide range of virtual sensors, including LiDAR, depth cameras, IMUs, force/torque sensors, and more. This is crucial for developing perception and navigation algorithms.
-   **Robot Model Integration**: Seamlessly integrates with URDF (Unified Robot Description Format) and SDF (Simulation Description Format) for defining robot and world models.
-   **ROS 2 Integration**: Designed to work hand-in-hand with ROS 2, allowing you to use the same ROS 2 nodes in simulation as you would on a physical robot.

### Setting up a Gazebo Environment

You will learn how to:
-   Launch Gazebo with pre-built worlds.
-   Import and spawn your humanoid robot model (defined using URDF/SDF).
-   Configure virtual sensors and visualize their data through ROS 2 topics.
-   Interact with the simulation, applying forces or moving objects.

## Unity: High-Fidelity Visualization

While Gazebo excels at physics, **Unity** is a powerful real-time 3D development platform renowned for its stunning graphics and visualization capabilities. By synchronizing Unity with Gazebo, we achieve:
-   **Photorealistic Rendering**: Create visually rich and immersive simulation environments.
-   **Advanced Lighting and Materials**: Enhance the aesthetic quality of your digital twin.
-   **Custom User Interfaces**: Develop interactive tools and dashboards for monitoring and controlling your robot.
-   **Synthetic Data Generation**: Unity's advanced rendering pipeline can be used to generate highly realistic synthetic datasets for training deep learning models, particularly for computer vision tasks.

### Synchronizing Gazebo and Unity

This section will cover methods for connecting Gazebo (running physics and ROS 2) with Unity (for visualization). Common approaches involve using:
-   **ROS 2 Unity Bridge**: A package that facilitates communication between ROS 2 and Unity, allowing real-time data exchange.
-   **Shared Memory/Network Protocols**: Custom solutions for high-bandwidth, low-latency data transfer between the two simulators.

## Sample Project: Simulating Humanoid Walking and Object Manipulation

In this module's sample project, you will apply the concepts learned to:
1.  Set up a Gazebo world with a simple humanoid robot and some objects.
2.  Implement a basic walking gait for the humanoid within Gazebo, either through direct joint commands or a simple controller.
3.  Synchronize this Gazebo simulation with a Unity project to visualize the walking motion in a high-fidelity environment.
4.  Develop a simple script to make the humanoid robot interact with and manipulate (e.g., push, pick up) an object in the Gazebo simulation, observing the results in Unity.

This project will demonstrate the power of combining Gazebo's robust physics with Unity's visual fidelity for realistic robot development and testing.

## Bringing It All Together: Your First Digital Twin

Let's integrate the concepts we've learned by launching our sample Gazebo world.

### 1. The Gazebo World File

**`humanoid_world.world`**
```xml
<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="humanoid_simple_world">
    <include>
      <uri>model://sun</uri>
    </include>
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Simple Humanoid Robot -->
    <model name="simple_humanoid">
      <pose>0 0 0.5 0 0 0</pose> <!-- Initial pose of the robot -->
      <static>false</static> <!-- Robot can move -->
      <link name="base_link">
        <visual>
          <geometry><box><size>0.1 0.1 0.1</size></box></geometry>
          <material><script><uri>file://media/materials/scripts/gazebo.material</uri><name>Gazebo/Orange</name></script></material>
        </visual>
        <collision>
          <geometry><box><size>0.1 0.1 0.1</size></box></geometry>
        </collision>
        <inertial>
          <mass>1.0</mass>
          <inertia><ixx>0.01</ixx><ixy>0</ixy><ixz>0</ixz><iyy>0.01</iyy><iyz>0</iyz><izz>0.01</izz></inertia>
        </inertial>
      </link>

      <!-- Torso -->
      <link name="torso">
        <visual>
          <geometry><box><size>0.2 0.3 0.5</size></box></geometry>
          <material><script><uri>file://media/materials/scripts/gazebo.material</uri><name>Gazebo/Grey</name></script></material>
        </visual>
        <collision>
          <geometry><box><size>0.2 0.3 0.5</size></box></geometry>
        </collision>
        <inertial>
          <mass>5.0</mass>
          <inertia><ixx>0.5</ixx><ixy>0</ixy><ixz>0</ixz><iyy>0.5</iyy><iyz>0</iyz><izz>0.5</izz></inertia>
        </inertial>
      </link>
      <joint name="base_to_torso" type="fixed">
        <parent>base_link</parent>
        <child>torso</child>
        <pose>0 0 0.25 0 0 0</pose>
      </joint>

      <!-- Head -->
      <link name="head">
        <visual>
          <geometry><sphere><radius>0.1</radius></sphere></geometry>
          <material><script><uri>file://media/materials/scripts/gazebo.material</uri><name>Gazebo/White</name></script></material>
        </visual>
        <collision>
          <geometry><sphere><radius>0.1</radius></sphere></geometry>
        </collision>
        <inertial>
          <mass>1.0</mass>
          <inertia><ixx>0.01</ixx><ixy>0</ixy><ixz>0</ixz><iyy>0.01</iyy><iyz>0</iyz><izz>0.01</izz></inertia>
        </inertial>
      </link>
      <joint name="torso_to_head" type="revolute">
        <parent>torso</parent>
        <child>head</child>
        <pose>0 0 0.3 0 0 0</pose>
        <axis><xyz>0 0 1</xyz></axis>
        <limit lower="-1.57" upper="1.57" velocity="100" effort="100"/></joint>

      <!-- Placeholder for right arm - expand as needed -->
      <link name="right_upper_arm">
        <visual>
          <geometry><cylinder><radius>0.04</radius><length>0.3</length></cylinder></geometry>
          <material><script><uri>file://media/materials/scripts/gazebo.material</uri><name>Gazebo/Grey</name></script></material>
        </visual>
        <collision>
          <geometry><cylinder><radius>0.04</radius><length>0.3</length></cylinder></geometry>
        </collision>
        <inertial>
          <mass>0.5</mass>
          <inertia><ixx>0.005</ixx><ixy>0</ixy><ixz>0</ixz><iyy>0.005</iyy><iyz>0</iyz><izz>0.005</izz></inertia>
        </inertial>
      </link>
      <joint name="torso_to_right_upper_arm" type="revolute">
        <parent>torso</parent>
        <child>right_upper_arm</child>
        <pose>0 -0.2 0.2 0 0 0</pose>
        <axis><xyz>0 1 0</xyz></axis>
        <limit lower="-1.57" upper="1.57" velocity="100" effort="100"/>
      </joint>

      <!-- Placeholder for left arm - expand as needed -->
      <link name="left_upper_arm">
        <visual>
          <geometry><cylinder><radius>0.04</radius><length>0.3</length></cylinder></geometry>
          <material><script><uri>file://media/materials/scripts/gazebo.material</uri><name>Gazebo/Grey</name></script></material>
        </visual>
        <collision>
          <geometry><cylinder><radius>0.04</radius><length>0.3</length></cylinder></geometry>
        </collision>
        <inertial>
          <mass>0.5</mass>
          <inertia><ixx>0.005</ixx><ixy>0</ixy><ixz>0</ixz><iyy>0.005</iyy><iyz>0</iyz><izz>0.005</izz></inertia>
        </inertial>
      </link>
      <joint name="torso_to_left_upper_arm" type="revolute">
        <parent>torso</parent>
        <child>left_upper_arm</child>
        <pose>0 0.2 0.2 0 0 0</pose>
        <axis><xyz>0 1 0</xyz></axis>
        <limit lower="-1.57" upper="1.57" effort="100" velocity="100"/>
      </joint>
    </model>
  </world>
</sdf>
```

### 2. Launching in Gazebo

1.  Ensure your ROS 2 environment is sourced.
2.  Navigate to the `resources/simulations/` directory.
3.  Launch the world:
    ```bash
    ros2 launch spawn_humanoid_world.launch.py
    ```
    This command will open Gazebo with the `simple_humanoid` robot spawned in the world.

### 3. Unity Visualization (Placeholder)

The Unity project for high-fidelity visualization would reside in `resources/code/module2-unity/HumanoidViz/`.
You would typically:
1.  Open the `HumanoidViz` project in Unity.
2.  Configure the ROS 2 Unity Bridge (or similar mechanism) to connect to the running Gazebo simulation.
3.  Run the Unity scene to visualize the robot's state and interactions in real-time.

---
**Further Reading:**
-   [Gazebo Documentation](http://gazebosim.org/docs)
-   [Unity Robotics Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub)
-   [ROS 2 Unity Bridge](https://github.com/Unity-Technologies/ROS-TCP-Endpoint)

