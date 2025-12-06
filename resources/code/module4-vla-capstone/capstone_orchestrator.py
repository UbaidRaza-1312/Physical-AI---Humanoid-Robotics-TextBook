#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String # For simple command feedback/status
import threading
import time

# Assuming these modules will be implemented within the same package or accessible
from .voice_command_processor import transcribe_audio # Relative import
from .task_planner import generate_robot_plan     # Relative import

class CapstoneOrchestrator(Node):

    def __init__(self):
        super().__init__('capstone_orchestrator')
        self.get_logger().info('Capstone Orchestrator Node started.')

        # Initialize publishers/subscribers for robot actions (e.g., navigation goals, manipulation commands)
        self.status_publisher = self.create_publisher(String, '/robot_status', 10)
        # Placeholder for actual action clients/publishers (e.g., Nav2 Action Client, JointCommand Publisher)
        # self.nav_action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        # self.manipulation_publisher = self.create_publisher(JointState, '/joint_commands', 10)

        # State variables
        self.current_robot_status = "IDLE"
        self.command_in_progress = False

        # Start a thread for listening to voice commands (or a dedicated ROS 2 subscriber)
        self.voice_command_thread = threading.Thread(target=self._listen_for_commands)
        self.voice_command_thread.daemon = True
        self.voice_command_thread.start()

        self.timer = self.create_timer(1.0, self.timer_callback) # Publish status periodically

    def _listen_for_commands(self):
        """
        Simulates listening for a voice command. In a real system, this could
        be a loop polling a microphone or a ROS 2 audio subscriber.
        """
        self.get_logger().info("Listening for voice commands...")
        while rclpy.ok():
            if not self.command_in_progress:
                # Simulate a voice command being received
                # In a real system, replace this with actual audio capture & transcription
                # For demo, we'll use a hardcoded command every 10 seconds
                time.sleep(10) 
                simulated_command = "Go to the charging station and pick up the power pack."
                self.get_logger().info(f"Simulated voice command received: \"{simulated_command}\""
                self.process_voice_command(simulated_command)
            else:
                time.sleep(1) # Wait if a command is already being processed

    def process_voice_command(self, spoken_text):
        if self.command_in_progress:
            self.get_logger().warn("Already processing a command. Please wait.")
            return

        self.command_in_progress = True
        self.update_status(f"Received command: {spoken_text}")
        self.get_logger().info(f"Processing command: \"{spoken_text}\""

        # Step 1: Transcribe (simulated, as we directly receive text here)
        # In a full system, you'd use voice_command_processor.transcribe_audio()
        transcribed_text = spoken_text 

        # Step 2: Cognitive Planning using LLM
        robot_plan = generate_robot_plan(transcribed_text)

        if robot_plan:
            self.get_logger().info(f"Generated plan: {robot_plan}")
            self.execute_robot_plan(robot_plan)
        else:
            self.get_logger().error("Failed to generate a plan from the command.")
            self.update_status("Command failed: Could not plan.")
            self.command_in_progress = False

    def execute_robot_plan(self, plan):
        """
        Executes the generated robot plan by dispatching ROS 2 actions.
        """
        self.update_status("Executing plan...")
        for action in plan:
            action_type = action.get("action")
            target = action.get("target")
            obj = action.get("object")
            dest = action.get("destination")

            if action_type == "NAVIGATE":
                self.get_logger().info(f"Navigating to: {target}")
                self.update_status(f"Navigating to {target}")
                # Dispatch Nav2 action client goal
                # self.nav_action_client.send_goal_async(NavigateToPose.Goal(pose=target_pose))
                time.sleep(5) # Simulate navigation
                self.get_logger().info(f"Reached {target}.")
            elif action_type == "IDENTIFY":
                self.get_logger().info(f"Identifying object: {obj}")
                self.update_status(f"Identifying {obj}")
                # Call perception service or wait for perception topic
                time.sleep(2) # Simulate identification
                self.get_logger().info(f"Identified {obj}.")
            elif action_type == "GRASP":
                self.get_logger().info(f"Grasping object: {obj}")
                self.update_status(f"Grasping {obj}")
                # Dispatch manipulation action
                time.sleep(3) # Simulate grasping
                self.get_logger().info(f"Grasped {obj}.")
            elif action_type == "RELEASE":
                self.get_logger().info(f"Releasing object: {obj}")
                self.update_status(f"Releasing {obj}")
                # Dispatch manipulation action
                time.sleep(2) # Simulate releasing
                self.get_logger().info(f"Released {obj}.")
            elif action_type == "BRING":
                self.get_logger().info(f"Bringing {obj} to {dest}")
                self.update_status(f"Bringing {obj} to {dest}")
                # Sequence of NAVIGATE, GRASP, NAVIGATE, RELEASE
                time.sleep(10) # Simulate bringing
                self.get_logger().info(f"Brought {obj} to {dest}.")
            else:
                self.get_logger().warn(f"Unknown action type: {action_type}")
            
            # Check for rclpy.ok() to allow shutdown during long actions
            if not rclpy.ok():
                break

        self.update_status("Plan execution complete.")
        self.get_logger().info("Robot plan executed successfully.")
        self.command_in_progress = False


    def update_status(self, status_message):
        self.current_robot_status = status_message
        msg = String()
        msg.data = status_message
        self.status_publisher.publish(msg)
        self.get_logger().info(f"Status: {status_message}")

    def timer_callback(self):
        # Periodically publish the current status
        msg = String()
        msg.data = f"Current status: {self.current_robot_status}"
        self.status_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    orchestrator = CapstoneOrchestrator()
    rclpy.spin(orchestrator)
    orchestrator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
