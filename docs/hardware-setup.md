---
id: hardware-setup
title: Hardware & Environment Setup Guide
---

This guide details the recommended and minimum hardware specifications, as well as the software environment setup required to effectively utilize this textbook and successfully complete its modules and projects. Adhering to these guidelines is crucial for reproducibility and optimal performance.

## 1. Digital Twin Workstation (per student)

This is the primary development machine for most simulation and AI development tasks.

-   **Operating System**: Ubuntu 22.04 LTS
-   **Processor**: Intel i7 (10th Gen or newer) / AMD Ryzen 7 (3000 series or newer), or equivalent. A modern multi-core CPU is essential for efficient compilation and simulation.
-   **Graphics Card (GPU)**: NVIDIA RTX 4070 Ti+ (or equivalent with at least 12GB VRAM). An NVIDIA GPU is **critical** for Isaac Sim, Isaac ROS, and other CUDA-accelerated tasks. Lower-end GPUs may result in significantly reduced simulation performance and extended training times.
-   **RAM**: 64GB DDR4 (or better). High RAM capacity is necessary for running complex simulations, large AI models, and multiple development tools concurrently.
-   **Storage**: 1TB NVMe SSD (minimum). High-speed storage is vital for fast loading of simulation assets, datasets, and project files.

## 2. Physical AI Edge Kit (Optional, but Recommended for Real-World Deployment)

This kit allows for real-world deployment of AI models developed in simulation.

-   **Compute Module**: NVIDIA Jetson Orin Nano / Orin NX (e.g., Jetson Orin Nano Developer Kit). These edge AI platforms provide the necessary compute for on-device inference.
-   **Depth Camera**: Intel RealSense D435i / D455. Used for 3D perception, object detection, and localization.
-   **Inertial Measurement Unit (IMU)**: USB IMU (e.g., a low-cost MPU-9250 based sensor). Provides orientation and acceleration data for robot state estimation.
-   **Audio Interface**: USB microphone and speaker. Required for voice command processing (OpenAI Whisper) and auditory feedback.

## 3. Robot Lab Options (Optional, for Physical Interaction)

While the textbook heavily relies on simulation, physical robots offer invaluable real-world experience.

-   **Proxy Robot**: Quadruped (e.g., Unitree Go2 Education Version) or a Robotic Arm. Excellent for learning basic locomotion, manipulation, and ROS 2 integration without the complexity of a full humanoid.
-   **Miniature Humanoid**: Hiwonder TonyPi Pro or similar. Provides an accessible platform for humanoid-specific kinematics and control.
-   **Premium Humanoid**: Unitree G1. A full-fledged humanoid robot offering advanced capabilities for research and complex capstone projects.

## 4. Cloud Lab Option (for GPU-Intensive Tasks)

For students without access to high-end local workstations or NVIDIA Jetson kits.

-   **Cloud Provider**: AWS, Azure, Google Cloud Platform (GCP).
-   **Instance Type**: GPU instances suitable for deep learning workloads (e.g., NVIDIA V100, A100, or H100 powered instances).
-   **Edge Kit for Deployment**: Even with cloud simulation, a local Physical AI Edge Kit is recommended for real-world deployment exercises to manage latency and physical interaction.

## 5. Software Environment

The primary software stack will be Ubuntu 22.04 LTS. Specific versions and installation instructions for key software will be provided in their respective modules:

-   **ROS 2**: Humble Hawksbill or Iron Irwini.
-   **Python**: Version 3.10+ (compatible with ROS 2).
-   **Gazebo**: Latest supported version for ROS 2.
-   **Unity**: A recent LTS version with relevant robotics packages.
-   **NVIDIA Isaac Sim**: Latest version, requiring an NVIDIA GPU.
-   **NVIDIA Isaac ROS**: Latest version, compatible with Isaac Sim.
-   **Development Tools**: VS Code, Git, Docker, etc.

By ensuring your environment meets these specifications, you will be well-prepared to follow the tutorials and complete the projects in this textbook.
