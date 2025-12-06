# Humanoid Planning Package

This package is responsible for processing natural language commands, transcribing speech to text, and generating task graphs for the humanoid robot. It serves as the cognitive "brain" for high-level decision making.

## Nodes

- `audio_listener`: Captures audio input (microphone) and potentially preprocesses it.
- `transcription_service`: A ROS 2 service server that calls the OpenAI Whisper API to transcribe audio.
- `task_planner_node`: Takes transcribed text, parses it into a structured command, and generates a `TaskGraph` message for execution.

## Usage

To launch the planning nodes (after building the workspace):

```bash
# Launch the transcription service
ros2 run humanoid_planning transcription_service

# Launch the task planner
ros2 run humanoid_planning task_planner_node

# Launch the audio listener (optional, if not integrated into task_planner_node)
ros2 run humanoid_planning audio_listener
```

## Dependencies

- `humanoid_interfaces`
- `rclpy` (ROS 2 Python client library)
- `OpenAI` Python client library (for Whisper API)
