---
id: ros2-fundamentals
title: ROS 2 Fundamentals and Packages
---

Welcome to Module 1, where you will dive into the **Robotic Operating System 2 (ROS 2)**, the essential middleware for modern robotics development. This module covers the core concepts, architecture, and practical usage of ROS 2, preparing you to build and control robotic systems.

## What is ROS 2?

ROS 2 is a flexible framework for writing robot software. It's not an operating system in the traditional sense, but rather a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot applications across a wide variety of robotic platforms.

Key features and benefits of ROS 2 include:
-   **Distributed System**: Designed to work across multiple processes, machines, and even operating systems.
-   **Real-time Capabilities**: Enhanced support for real-time control, crucial for physical robots.
-   **Quality of Service (QoS)**: Configurable settings for reliability, latency, and throughput of data communication.
-   **Security**: Built-in security features using DDS (Data Distribution Service).
-   **Python & C++ APIs**: Supports both `rclpy` (Python) and `rclcpp` (C++) for developing nodes.

## ROS 2 Architecture

At the heart of ROS 2 are several fundamental concepts that enable inter-process communication and modular development:

### Nodes
A **Node** is an executable process that performs computation. In a typical ROS 2 system, multiple nodes work together, each responsible for a specific function (e.g., a camera driver node, a motor control node, a path planning node). Nodes communicate with each other using various mechanisms.

### Topics
**Topics** are named buses over which nodes exchange messages. This is a publish/subscribe model:
-   A node can **publish** messages to a topic.
-   Other nodes can **subscribe** to a topic to receive messages.
Messages sent on a topic are essentially data structures (e.g., sensor readings, command velocities).

### Services
**Services** are a request/reply communication mechanism. They are used for synchronous operations where a client node sends a request to a service server node and waits for a reply. This is suitable for tasks that require an immediate response, such as getting a single sensor reading or triggering an action.

### Actions
**Actions** provide a long-running goal-feedback-result communication pattern. They are built on top of topics and services and are designed for tasks that may take a significant amount of time to complete (e.g., navigating to a goal, picking up an object). An action client sends a goal, receives continuous feedback on its progress, and eventually gets a result.

### Parameters
**Parameters** allow nodes to expose configuration values that can be changed at runtime. This enables flexible configuration without recompiling code.

## Python Integration with `rclpy`

`rclpy` is the Python client library for ROS 2, providing a clean and intuitive API for creating ROS 2 nodes, publishers, subscribers, services, and actions using Python. This textbook will primarily utilize `rclpy` for its ease of use and rapid prototyping capabilities.

## URDF (Unified Robot Description Format)

The **Unified Robot Description Format (URDF)** is an XML file format used in ROS to describe all elements of a robot. This includes:
-   **Links**: The rigid bodies of the robot (e.g., torso, arm, wheel).
-   **Joints**: The connections between links, defining their kinematic and dynamic properties (e.g., revolute, prismatic).
-   **Visual Properties**: How the robot looks (e.g., colors, textures).
-   **Collision Properties**: How the robot interacts physically with its environment.
-   **Inertial Properties**: Mass, center of mass, and inertia matrix.

URDF is crucial for simulating robots in environments like Gazebo and for motion planning.

## ROS 2 Package Creation

A **ROS 2 package** is the fundamental unit of software organization in ROS 2. It contains nodes, launch files, message definitions, and other resources related to a specific functionality. You will learn how to:
-   Create new ROS 2 packages using `colcon`.
-   Define package dependencies.
-   Implement nodes in Python.
-   Create `launch` files to start multiple nodes and configure parameters.

## Sample Project: Controlling Joints and Reading Sensor Data

In this module's sample project, you will build a basic ROS 2 package that can:
1.  Publish commands to control the joints of a simulated humanoid robot.
2.  Subscribe to a topic to receive sensor data (e.g., joint states).
3.  Process and log this data.

This foundational project will demonstrate the core communication mechanisms of ROS 2 and set the stage for more complex robotic applications.

## Bringing It All Together: Your First ROS 2 Package

Let's integrate the concepts we've learned by building and running the sample package.

### 1. The Code

**`publisher_node.py`**
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('publisher_node')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS 2: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**`subscriber_node.py`**
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2. The Robot Model

**`basic_humanoid.urdf`**
```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">

  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </visual>
  </link>

  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.2 0.3 0.5"/>
      </geometry>
      <material name="grey">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
  </link>

  <joint name="base_to_torso" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.25"/>
  </joint>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
  </link>

  <joint name="torso_to_head" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.3"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="100"/>
  </joint>

  <!-- Right Arm -->
  <link name="right_upper_arm">
    <visual>
      <geometry>
        <cylinder radius="0.04" length="0.3"/>
      </geometry>
       <material name="grey"/>
    </visual>
  </link>

  <joint name="torso_to_right_upper_arm" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_arm"/>
    <origin xyz="0 -0.2 0.2"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="100"/>
  </joint>

  <!-- Left Arm -->
  <link name="left_upper_arm">
    <visual>
      <geometry>
        <cylinder radius="0.04" length="0.3"/>
      </geometry>
       <material name="grey"/>
    </visual>
  </link>

  <joint name="torso_to_left_upper_arm" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="0 0.2 0.2"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="100"/>
  </joint>

</robot>
```

### 3. The Build Files

**`package.xml`**
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_ros2_pkg</name>
  <version>0.0.0</version>
  <description>Sample ROS 2 Python package for basic joint and sensor control</description>
  <maintainer email="your.email@example.com">Your Name</maintainer>
  <license>Apache License 2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>

  <test_depend>pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

**`setup.py`**
```python
from setuptools import setup

package_name = 'my_ros2_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/my_ros2_pkg_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='Sample ROS 2 Python package for basic joint and sensor control',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher_node = my_ros2_pkg.publisher_node:main',
            'subscriber_node = my_ros2_pkg.subscriber_node:main',
        ],
    },
)
```

### 4. The Launch File

**`my_ros2_pkg_launch.py`**
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_ros2_pkg',
            executable='publisher_node',
            name='simple_publisher',
            output='screen'
        ),
        Node(
            package='my_ros2_pkg',
            executable='subscriber_node',
            name='simple_subscriber',
            output='screen'
        ),
    ])
```

### 5. Build and Run

1.  Navigate to the root of your ROS 2 workspace containing the `my_ros2_pkg`.
2.  Build the package: `colcon build --packages-select my_ros2_pkg`
3.  Source the setup files: `source install/setup.bash`
4.  Run the launch file: `ros2 launch my_ros2_pkg my_ros2_pkg_launch.py`

You should now see the publisher and subscriber nodes communicating with each other!

---
**Further Reading:**
-   [ROS 2 Documentation](https://docs.ros.org/en/humble/index.html)
-   [rclpy Documentation](https://docs.ros.org/en/humble/p/rclpy/index.html)
-   [URDF Tutorials](https://classic.gazebosim.org/tutorials?tut=ros_urdf)
