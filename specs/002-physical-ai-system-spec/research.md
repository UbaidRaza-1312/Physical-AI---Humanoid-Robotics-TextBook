# Research Document: Physical AI System

## 1. VSLAM Algorithm Selection

- **Decision**: `rtabmap_ros` will be used as the primary VSLAM package.
- **Rationale**: RTAB-Map (Real-Time Appearance-Based Mapping) is a mature, feature-rich package that is well-supported in the ROS 2 ecosystem. It handles loop closures, generates dense 3D point clouds, and integrates seamlessly with Nav2 for path planning. It supports the required sensor inputs (RGB-D, IMU).
- **Alternatives considered**:
    - `orb_slam3_ros`: Highly accurate, but integration with ROS 2 is less mature, and it is more focused on visual odometry than full mapping and navigation integration.
    - `slam_toolbox`: A solid choice for 2D LiDAR-based SLAM, but less suited for the 3D, vision-based requirements of this project.

## 2. NVIDIA Isaac Sim to ROS 2 Integration

- **Decision**: Use the built-in `omni.isaac.ros2_bridge` extension in Isaac Sim.
- **Rationale**: This is the official, NVIDIA-supported method for connecting Isaac Sim to a ROS 2 network. It provides high-performance, low-latency communication for sensor data (cameras, LiDAR, IMU), robot state (TF transforms, joint states), and receiving control commands. It is configurable to map Isaac Sim data types to ROS 2 messages.
- **Alternatives considered**: None. Using the official bridge is the only viable and supported option.

## 3. OpenAI Whisper API Integration

- **Decision**: A dedicated ROS 2 service will be created to handle interactions with the Whisper API. The service will accept an audio stream and return transcribed text.
- **Rationale**: Encapsulating the API call in a ROS 2 service abstracts the web logic away from the core planning nodes. This makes the system more modular and allows for easier testing. The service will implement a retry-with-backoff mechanism to handle transient network errors and API rate limits. Error states (e.g., API key invalid, network down) will be published to a status topic.
- **Alternatives considered**:
    - Direct API call from the planning node: This would tightly couple the planning logic with the web API, making it less modular and harder to test independently.
