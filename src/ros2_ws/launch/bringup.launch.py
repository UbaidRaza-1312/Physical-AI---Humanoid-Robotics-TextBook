import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # --- humanoid_description ---
    # Launch the robot state publisher and joint state publisher (from view_robot.launch.py)
    humanoid_description_launch_dir = os.path.join(
        get_package_share_directory('humanoid_description'), 'launch')
    
    ld.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                humanoid_description_launch_dir, 'view_robot.launch.py')])
        )
    )

    # --- humanoid_planning ---
    # Launch transcription service
    ld.add_action(
        Node(
            package='humanoid_planning',
            executable='transcription_service',
            name='transcription_service',
            output='screen'
        )
    )
    # Launch task planner node
    ld.add_action(
        Node(
            package='humanoid_planning',
            executable='task_planner_node',
            name='task_planner_node',
            output='screen'
        )
    )
    # Launch audio listener node
    ld.add_action(
        Node(
            package='humanoid_planning',
            executable='audio_listener',
            name='audio_listener',
            output='screen'
        )
    )

    # --- humanoid_control ---
    # Launch task executor node
    ld.add_action(
        Node(
            package='humanoid_control',
            executable='task_executor_node',
            name='task_executor_node',
            output='screen',
            # remapping certain topics if necessary, e.g., for TTS
            # remappings=[('/speech_synthesis', '/humanoid_control/speech_synthesis')],
        )
    )
    # Launch arm controller node
    ld.add_action(
        Node(
            package='humanoid_control',
            executable='arm_controller',
            name='arm_controller',
            output='screen'
        )
    )
    # Launch speech synthesis node
    ld.add_action(
        Node(
            package='humanoid_control',
            executable='speech_synthesis_node',
            name='speech_synthesis_node',
            output='screen'
        )
    )

    # --- humanoid_perception ---
    # Launch object detector node
    ld.add_action(
        Node(
            package='humanoid_perception',
            executable='object_detector',
            name='object_detector',
            output='screen'
        )
    )

    # --- humanoid_navigation ---
    # TODO: Add launch for Nav2 and VSLAM integration here once those packages are defined

    return ld
