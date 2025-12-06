from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_ros2_pkg',
            executable='publisher_node',
            name='simple_publisher',
            output='screen'
        ),
        Node(
            package='my_ros2_pkg',
            executable='subscriber_node',
            name='simple_subscriber',
            output='screen'
        ),
    ])
