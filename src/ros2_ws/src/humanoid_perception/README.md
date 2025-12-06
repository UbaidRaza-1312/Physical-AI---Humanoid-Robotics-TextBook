# Humanoid Perception Package

This package is responsible for processing sensor data (e.g., from RGB-D cameras) to perform tasks such as object detection, segmentation, and potentially object pose estimation.

## Nodes

- `object_detector`: Identifies objects from camera feeds and provides detection results to other systems.

## Usage

To launch the object detector (after building the workspace):

```bash
ros2 run humanoid_perception object_detector
```

## Dependencies

- `humanoid_interfaces`
- ROS 2 camera drivers (e.g., `realsense2_camera`)
- OpenCV (for image processing)
- Deep learning framework (e.g., PyTorch, TensorFlow) and trained models for object detection.
