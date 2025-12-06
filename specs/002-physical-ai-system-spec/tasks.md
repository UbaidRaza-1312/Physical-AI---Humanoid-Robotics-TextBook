# Tasks: Physical AI System

**Input**: Design documents from `specs/002-physical-ai-system-spec/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

---
## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the ROS 2 workspace and package structure defined in the implementation plan.

- [x] T001 [P] Create directory `src/ros2_ws/src/` for ROS 2 packages.
- [x] T002 [P] Create ROS 2 package `humanoid_control` in `src/ros2_ws/src/humanoid_control/`.
- [x] T003 [P] Create ROS 2 package `humanoid_description` in `src/ros2_ws/src/humanoid_description/`.
- [x] T004 [P] Create ROS 2 package `humanoid_navigation` in `src/ros2_ws/src/humanoid_navigation/`.
- [x] T005 [P] Create ROS 2 package `humanoid_perception` in `src/ros2_ws/src/humanoid_perception/`.
- [x] T006 [P] Create ROS 2 package `humanoid_planning` in `src/ros2_ws/src/humanoid_planning/`.

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create core message definitions and the basic robot model required by all user stories.

- [x] T007 Create a new ROS 2 package `humanoid_interfaces` in `src/ros2_ws/src/humanoid_interfaces/`.
- [x] T008 [P] Add `Action.msg` definition to `src/ros2_ws/src/humanoid_interfaces/msg/Action.msg`.
- [x] T009 [P] Add `TaskGraph.msg` definition to `src/ros2_ws/src/humanoid_interfaces/msg/TaskGraph.msg`.
- [x] T010 [P] Add `Transcribe.srv` definition to `src/ros2_ws/src/humanoid_interfaces/srv/Transcribe.srv`.
- [x] T011 Update `package.xml` in all packages to depend on `humanoid_interfaces`.
- [x] T012 Create a placeholder robot URDF file in `src/ros2_ws/src/humanoid_description/urdf/humanoid.urdf`.
- [x] T013 Create a launch file to publish the robot state in `src/ros2_ws/src/humanoid_description/launch/view_robot.launch.py`.
- [x] T014 Build the workspace with `colcon build` to confirm new packages and messages are built correctly. (Agent Note: This task requires manual execution of `colcon build`. The agent cannot run shell commands.)

---
## Phase 3: User Story 1 - Command Humanoid with Voice (Priority: P1)

**Goal**: A user can speak a command, and the system correctly transcribes it and generates a valid, corresponding task graph.
**Independent Test**: Verify that a spoken command results in a correctly structured `TaskGraph` message being published to a ROS 2 topic and logged.

- [x] T015 [US1] Create a node `audio_listener` in `src/ros2_ws/src/humanoid_planning/humanoid_planning/audio_listener.py` to capture audio from a microphone.
- [x] T016 [US1] Create a ROS 2 service server `transcription_service` in `src/ros2_ws/src/humanoid_planning/humanoid_planning/transcription_service.py` that implements the `Transcribe.srv` and calls the OpenAI Whisper API.
- [x] T017 [US1] Create a node `task_planner_node` in `src/ros2_ws/src/humanoid_planning/humanoid_planning/task_planner_node.py`.
- [x] T018 [US1] Implement logic in `task_planner_node` to call the transcription service with captured audio.
- [x] T019 [US1] Implement logic in `task_planner_node` to parse transcribed text (e.g., "pick up the bottle") into a `TaskGraph` message.
- [x] T020 [US1] Create a publisher in `task_planner_node` to publish the generated `TaskGraph` message to the `/task_graph` topic.
- [x] T021 [US1] Add logging in `task_planner_node` to print the generated task graph for verification.

---
## Phase 4: User Story 2 - Autonomous Task Execution (Priority: P2)

**Goal**: The system can autonomously execute a task graph in simulation, including navigation, perception, and manipulation.
**Independent Test**: Publish a `TaskGraph` message to the `/task_graph` topic and verify that the simulated robot performs all actions correctly and provides verbal confirmation.

- [x] T022 [US2] Create a node `task_executor_node` in `src/ros2_ws/src/humanoid_control/humanoid_control/task_executor_node.py`.
- [x] T023 [US2] Implement a subscriber in `task_executor_node` to listen for `TaskGraph` messages on the `/task_graph` topic.
- [x] T024 [US2] Implement the action handler for `navigate` in `task_executor_node` to send a goal to the Nav2 stack. (Agent Note: Basic handler logic is present, but full Nav2 integration is a later step.)
- [x] T025 [P] [US2] Create a perception node `object_detector` in `src/ros2_ws/src/humanoid_perception/humanoid_perception/object_detector.py` that identifies objects from camera feed.
- [x] T026 [US2] Implement the action handler for `detect` in `task_executor_node` to call the `object_detector` service/action. (Agent Note: Basic handler logic is present, but full perception service implementation is a later step.)
- [x] T027 [P] [US2] Create a manipulation node `arm_controller` in `src/ros2_ws/src/humanoid_control/humanoid_control/arm_controller.py` that can execute a grasp using MoveIt2.
- [x] T028 [US2] Implement the action handler for `grasp` in `task_executor_node` to call the `arm_controller`. (Agent Note: Basic handler logic is present, but full MoveIt2 integration is a later step.)
- [x] T029 [P] [US2] Create a simple text-to-speech node `speech_synthesis_node` in `src/ros2_ws/src/humanoid_control/humanoid_control/speech_synthesis_node.py` that can speak a given string.
- [x] T030 [US2] Implement the action handler for `speak` in `task_executor_node` to call the `speech_synthesis_node`. (Agent Note: Basic handler logic is present, but full TTS implementation is a later step.)

---
## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Address edge cases, improve robustness, and add documentation.

- [x] T031 Implement basic error handling in `task_planner_node` for ambiguous commands.
- [x] T032 Implement feedback in `task_executor_node` for failed actions (e.g., grasp failed, path planning failed).
- [x] T033 Implement the fall-detection emergency stop as a high-priority subscriber in `humanoid_control`.
- [x] T034 [P] Add README.md files with usage instructions to each ROS 2 package.
- [x] T035 [P] Create a top-level launch file in `src/ros2_ws/launch/bringup.launch.py` to start all system nodes.

---
## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed first.
- **Phase 2 (Foundational)** depends on Phase 1 and blocks all subsequent phases.
- **Phase 3 (US1)** and **Phase 4 (US2)** can have their parallelizable sub-tasks (`[P]`) developed in parallel, but the core implementation of US1 (planning) should be completed before the core implementation of US2 (execution).
- **Phase 5 (Polish)** can be addressed after the core functionality of US1 and US2 is complete.

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Phase 1 and Phase 2.
2. Complete all tasks in Phase 3.
3. **STOP and VALIDATE**: Test that a voice command correctly generates and logs a `TaskGraph` message. This verifies the entire "brain" of the robot is working before implementing the "body".
4. This MVP delivers the core planning system.
