import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from humanoid_interfaces.srv import Transcribe
from humanoid_interfaces.msg import TaskGraph, Action

import json # For parsing hypothetical planner models


class TaskPlannerNode(Node):
    def __init__(self):
        super().__init__('task_planner_node')
        self.get_logger().info('Task Planner Node started.')

        # Create a client for the transcription service
        self.transcription_client_cb_group = MutuallyExclusiveCallbackGroup()
        self.transcription_client = self.create_client(
            Transcribe,
            'transcribe_audio',
            callback_group=self.transcription_client_cb_group
        )
        while not self.transcription_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Transcription service not available, waiting...')

        # Create a publisher for the TaskGraph
        self.task_graph_publisher = self.create_publisher(
            TaskGraph,
            '/task_graph',
            10
        )

        # TODO: This node will need a way to receive audio data (e.g., from audio_listener node)
        # For now, let's create a timer to simulate receiving a command
        self.timer = self.create_timer(5.0, self.simulate_command_callback)
        self.get_logger().info('Simulating command every 5 seconds...')


    async def simulate_command_callback(self):
        # In a real scenario, this would come from an audio_listener or another source
        self.get_logger().info('Simulating voice command: "Pick up the red block"')
        
        # Create a dummy request for the transcription service
        transcribe_request = Transcribe.Request()
        transcribe_request.audio_data = b'dummy_audio_data' # Replace with actual audio bytes
        transcribe_request.encoding = 'wav'

        self.get_logger().info('Calling transcription service...')
        try:
            transcription_response = await self.transcription_client.call_async(transcribe_request)
            if transcription_response.success:
                self.get_logger().info(f'Transcribed text: {transcription_response.transcribed_text}')
                self.generate_and_publish_task_graph(transcription_response.transcribed_text)
            else:
                self.get_logger().error(f'Transcription failed: {transcription_response.error_message}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')


    def generate_and_publish_task_graph(self, command_text: str):
        self.get_logger().info(f'Generating task graph for command: "{command_text}"')

        task_graph_msg = TaskGraph()
        task_graph_msg.graph_id = 1 # Simple ID for now

        # Use a simple regex for parsing commands
        import re
        match = re.match(r"(?:pick up|grasp)\s+(?:the\s+)?(.+)", command_text.lower())

        if match:
            target_object = match.group(1).strip()
            
            # Example actions
            action1 = Action(action_id=1, type="navigate", params=[f"to_{target_object}"])
            action2 = Action(action_id=2, type="detect", params=[target_object])
            action3 = Action(action_id=3, type="grasp", params=[target_object])
            action4 = Action(action_id=4, type="speak", params=["Task complete"])

            task_graph_msg.actions = [action1, action2, action3, action4]
            self.get_logger().info(f'Generated TaskGraph: {json.dumps(self.task_graph_to_dict(task_graph_msg), indent=2)}')

            self.task_graph_publisher.publish(task_graph_msg)
            self.get_logger().info(f'Published TaskGraph with ID: {task_graph_msg.graph_id}')
        else:
            self.get_logger().warn(f'Could not parse command: "{command_text}". No TaskGraph generated.')
            # FR-014: Provide verbal feedback upon task completion for failures
            error_action = Action(action_id=1, type="speak", params=["I did not understand your command. Please try again."])
            task_graph_msg.actions = [error_action]
            self.task_graph_publisher.publish(task_graph_msg)
            self.get_logger().info(f'Published error TaskGraph for command: "{command_text}"')


    def task_graph_to_dict(self, task_graph_msg: TaskGraph):
        # Helper to convert TaskGraph message to a dictionary for logging
        return {
            "graph_id": task_graph_msg.graph_id,
            "actions": [
                {"action_id": a.action_id, "type": a.type, "params": a.params}
                for a in task_graph_msg.actions
            ]
        }


def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor()
    task_planner_node = TaskPlannerNode()
    executor.add_node(task_planner_node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        task_planner_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
