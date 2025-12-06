# Humanoid Control Package

This package contains the core control nodes for the humanoid robot, including the `TaskExecutorNode` which interprets and executes task graphs received from the `humanoid_planning` package.

## Nodes

- `task_executor_node`: Subscribes to `/task_graph` and dispatches actions to other control and perception systems.

## Usage

To launch the task executor (after building the workspace):

```bash
ros2 run humanoid_control task_executor_node
```

## Dependencies

- `humanoid_interfaces`
- ROS 2 Nav2 stack (for navigation actions)
- ROS 2 MoveIt2 (for grasping actions)
- `humanoid_perception` (for object detection actions)
- `speech_synthesis_node` (for speak actions)
