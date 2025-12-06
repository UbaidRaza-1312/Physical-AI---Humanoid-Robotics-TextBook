# Humanoid Interfaces Package

This package defines the custom ROS 2 message (`.msg`) and service (`.srv`) types used throughout the Physical AI System. These interfaces enable different ROS 2 packages to communicate and exchange structured data.

## Contents

- `msg/Action.msg`: Defines a single action to be performed by the robot.
- `msg/TaskGraph.msg`: Defines a sequence of `Action` messages that constitute a robot task plan.
- `srv/Transcribe.srv`: Defines the request and response for the audio transcription service.

## Usage

These messages and services are automatically generated when the workspace is built. Other ROS 2 packages can then declare dependencies on `humanoid_interfaces` to use these custom types.

## Dependencies

- None (this is a foundational interface package)
