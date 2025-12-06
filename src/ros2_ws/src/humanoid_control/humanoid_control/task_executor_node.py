import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from humanoid_interfaces.msg import TaskGraph, Action
from std_msgs.msg import Bool # Import Bool message type

# Placeholder for Nav2 and MoveIt2 integration
# from nav2_msgs.action import NavigateToPose
# from moveit_msgs.srv import Grasp


class TaskExecutorNode(Node):
    def __init__(self):
        super().__init__('task_executor_node')
        self.get_logger().info('Task Executor Node started.')

        self.cb_group = MutuallyExclusiveCallbackGroup()

        self.task_graph_subscriber = self.create_subscription(
            TaskGraph,
            '/task_graph',
            self.task_graph_callback,
            10,
            callback_group=self.cb_group
        )
        self.get_logger().info('Subscribed to /task_graph topic.')

        # T033: Implement fall-detection emergency stop subscriber
        self.emergency_stop_subscriber = self.create_subscription(
            Bool, # Assuming a std_msgs/Bool message for fall detection
            '/fall_detected',
            self.emergency_stop_callback,
            1, # High priority, best effort
            callback_group=self.cb_group
        )
        self.get_logger().info('Emergency stop subscriber initialized.')

        # TODO: Initialize clients/publishers for other systems (Nav2, MoveIt2, Perception Service, TTS)
        # self.nav2_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        # self.grasp_client = self.create_client(Grasp, 'execute_grasp')
        # self.perception_client = self.create_client(DetectObject, 'detect_object')
        # self.tts_publisher = self.create_publisher(String, '/speech_synthesis', 10)


    async def task_graph_callback(self, msg: TaskGraph):
        self.get_logger().info(f'Received TaskGraph with ID: {msg.graph_id}')
        for action in msg.actions:
            self.get_logger().info(f'Executing action: {action.type} with params: {action.params}')
            success = await self.execute_action(action)
            if not success:
                self.get_logger().error(f'Action {action.type} failed. Aborting TaskGraph.')
                # Implement feedback for failed actions (T032)
                error_action = Action(action_id=action.action_id, type="speak", params=[f"Failed to {action.type}."])
                await self._handle_speak_action(error_action.params)
                # TODO: Implement error recovery or alternative actions
                return
        self.get_logger().info(f'TaskGraph {msg.graph_id} completed successfully.')
        # Provide final confirmation
        final_speak_action = Action(action_id=999, type="speak", params=["All tasks completed."])
        await self._handle_speak_action(final_speak_action.params)


    async def emergency_stop_callback(self, msg: Bool):
        if msg.data:
            self.get_logger().fatal('FALL DETECTED! Initiating emergency stop procedures.')
            # TODO: Implement actual emergency stop logic (e.g., cut power, lock joints)
            # For now, just log and halt further task execution (if possible)
            self._mock_abort_current_task() # A conceptual method
            emergency_speak_action = Action(action_id=998, type="speak", params=["Fall detected! Emergency stop initiated."])
            await self._handle_speak_action(emergency_speak_action.params)


    def _mock_abort_current_task(self):
        self.get_logger().warn("Mock: Aborting current task execution due to emergency stop.")
        # In a real system, this would involve cancelling active actions,
        # stopping motors, etc.


    async def execute_action(self, action: Action) -> bool:
        """Executes a single action based on its type."""
        if action.type == "navigate":
            return await self._handle_navigate_action(action.params)
        elif action.type == "detect":
            return await self._handle_detect_action(action.params)
        elif action.type == "grasp":
            return await self._handle_grasp_action(action.params)
        elif action.type == "speak":
            return await self._handle_speak_action(action.params)
        else:
            self.get_logger().warn(f'Unknown action type: {action.type}')
            return False


    async def _handle_navigate_action(self, params: list[str]) -> bool:
        self.get_logger().info(f'Navigating to: {params}')
        # TODO: Implement Nav2 integration
        await self._mock_delay(3.0) # Simulate navigation time
        return True


    async def _handle_detect_action(self, params: list[str]) -> bool:
        self.get_logger().info(f'Detecting object: {params}')
        # TODO: Implement perception service call
        await self._mock_delay(2.0) # Simulate detection time
        return True


    async def _handle_grasp_action(self, params: list[str]) -> bool:
        self.get_logger().info(f'Grasping object: {params}')
        # TODO: Implement MoveIt2 integration
        await self._mock_delay(4.0) # Simulate grasping time
        return True


    async def _handle_speak_action(self, params: list[str]) -> bool:
        text_to_speak = params[0] if params else "Unknown command"
        self.get_logger().info(f'Speaking: "{text_to_speak}"')
        # TODO: Implement TTS publisher
        await self._mock_delay(1.0) # Simulate speaking time
        return True

    async def _mock_delay(self, duration: float):
        await rclpy.sleep(duration)


def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor()
    task_executor_node = TaskExecutorNode()
    executor.add_node(task_executor_node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        task_executor_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
