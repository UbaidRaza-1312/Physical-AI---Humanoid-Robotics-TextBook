# Data Model for Physical AI & Humanoid Robotics Textbook

## Entities

### Textbook Module
Represents a distinct section of the textbook content.
- **Attributes**:
    - `id`: Unique identifier (e.g., "module1-ros2")
    - `title`: Title of the module (e.g., "Robotic Nervous System (ROS 2)")
    - `description`: Brief overview of the module
    - `word_count`: Total word count for the module (5,000–7,000 words)
    - `learning_objectives`: List of key learning outcomes
    - `tutorials`: List of associated tutorials (references `Tutorial` entity)
    - `code_examples`: List of associated code examples (references `CodeExample` entity)
    - `hardware_requirements`: Description of hardware needed for the module
    - `cloud_alternatives`: Description of cloud-based options
    - `citation_references`: List of APA-formatted citations

### Tutorial
A step-by-step guide within a module.
- **Attributes**:
    - `id`: Unique identifier
    - `title`: Title of the tutorial
    - `module_id`: Foreign key referencing `TextbookModule.id`
    - `description`: Overview of the tutorial's goal
    - `steps`: Ordered list of instructions
    - `code_snippets`: Inline code examples (references `CodeSnippet` entity)
    - `expected_output`: Description or image of expected results

### Code Example
A reproducible code segment or project.
- **Attributes**:
    - `id`: Unique identifier
    - `name`: Name of the code example (e.g., "publisher_node.py")
    - `module_id`: Foreign key referencing `TextbookModule.id`
    - `path`: File path to the code example in the `resources/code` directory
    - `language`: Programming language (e.g., "Python", "C++")
    - `description`: Explanation of the code's functionality
    - `dependencies`: List of required libraries/packages

### Robot Model
Represents a virtual or physical robot.
- **Attributes**:
    - `id`: Unique identifier
    - `name`: Name of the robot (e.g., "humanoid_v1")
    - `type`: "Simulated" or "Physical"
    - `urdf_sdf_path`: Path to URDF/SDF file for simulated robots
    - `joint_states`: Current configuration of robot joints (dynamic, not persistent)
    - `sensor_data`: Real-time data from robot sensors (dynamic, not persistent)
    - `capabilities`: List of actions the robot can perform (e.g., "navigate", "manipulate")

### ROS 2 Package
A standard ROS 2 software unit.
- **Attributes**:
    - `id`: Unique identifier
    - `name`: Package name (e.g., "my_ros2_pkg")
    - `path`: File path to the package in `resources/code`
    - `dependencies`: List of other ROS 2 packages or system libraries
    - `nodes`: List of executables/nodes within the package
    - `topics`: List of communication topics
    - `services`: List of offered services
    - `actions`: List of available actions
    - `launch_files`: List of launch configurations

### Simulation Environment
Software platform for robot simulation.
- **Attributes**:
    - `id`: Unique identifier (e.g., "gazebo", "unity", "isaac_sim")
    - `name`: Name of the environment
    - `version`: Software version
    - `physics_engine`: Name of the physics engine used
    - `sensor_simulation_features`: Capabilities for simulating sensors
    - `3d_models_path`: Path to 3D assets used in simulation
    - `world_files`: List of simulation world configurations

### AI Model
Represents a deployed Artificial Intelligence model.
- **Attributes**:
    - `id`: Unique identifier (e.g., "gpt_planner", "whisper_asr")
    - `name`: Name of the model
    - `type`: (e.g., "LLM", "VLA", "ASR", "Perception")
    - `api_endpoint`: URL for API access (if applicable)
    - `input_format`: Expected input data structure
    - `output_format`: Expected output data structure
    - `description`: High-level functionality

### Hardware Component
Physical computer or robotic part.
- **Attributes**:
    - `id`: Unique identifier
    - `name`: Component name (e.g., "RTX 4070 Ti", "Jetson Orin Nano", "RealSense D435i")
    - `type`: (e.g., "GPU", "SBC", "Sensor", "Robot")
    - `specifications`: Detailed technical specs
    - `usage_context`: Where and how it's used in the textbook

---

## Relationships

- `TextbookModule` HAS MANY `Tutorial`
- `TextbookModule` HAS MANY `CodeExample`
- `Tutorial` HAS MANY `CodeSnippet` (inline, not a separate top-level entity)
- `CodeExample` MAY USE `ROS2Package`, `RobotModel`, `SimulationEnvironment`, `AIModel`, `HardwareComponent`
- `ROS2Package` INTERACTS WITH `RobotModel`, `SimulationEnvironment`, `AIModel`
- `SimulationEnvironment` HOSTS `RobotModel`
- `AIModel` CONTROLS / PROCESSES DATA FROM `RobotModel` / `SimulationEnvironment`
- `HardwareComponent` IS REQUIRED BY `TextbookModule`, `CodeExample`, `RobotModel`, `SimulationEnvironment`, `AIModel`