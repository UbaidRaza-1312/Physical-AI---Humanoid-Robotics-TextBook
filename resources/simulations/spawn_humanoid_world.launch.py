from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os

def generate_launch_description():
    # Get the path to the simulation resources
    pkg_path = os.path.join(os.getenv('AMENT_PREFIX_PATH').split(os.pathsep)[0], 'share', 'my_ros2_pkg') # This assumes my_ros2_pkg is installed and sourced
    if not os.path.exists(pkg_path): # Fallback if not sourced (e.g. running from build)
        pkg_path = os.path.join(os.getcwd(), 'resources', 'code', 'module1-ros2', 'my_ros2_pkg')
        if not os.path.exists(pkg_path): # Fallback to a common docusaurus root
            pkg_path = os.path.join(os.getcwd(), '../../resources', 'code', 'module1-ros2', 'my_ros2_pkg')
            if not os.path.exists(pkg_path): # Final fallback, assumes ros_fundamentals is the cwd
                 pkg_path = os.path.join(os.getcwd(), 'resources', 'code', 'module1-ros2', 'my_ros2_pkg')
    
    urdf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'basic_humanoid.urdf') # Direct path relative to this launch file
    
    # Check if the URDF file exists at this path, if not try another fallback for docusaurus
    if not os.path.exists(urdf_file):
        urdf_file = os.path.join(os.getcwd(), 'resources', 'simulations', 'basic_humanoid.urdf')
        if not os.path.exists(urdf_file):
            urdf_file = os.path.join(os.getcwd(), '../../resources', 'simulations', 'basic_humanoid.urdf')

    world_file_name = 'humanoid_simple_world.world'
    world_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), world_file_name)
    
    # Check if the world file exists, if not try another fallback
    if not os.path.exists(world_file_path):
        world_file_path = os.path.join(os.getcwd(), 'resources', 'simulations', world_file_name)
        if not os.path.exists(world_file_path):
            world_file_path = os.path.join(os.getcwd(), '../../resources', 'simulations', world_file_name)

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument(
            'world',
            default_value=[world_file_path],
            description='SDF world file'),

        Node(
            package='gazebo_ros',
            executable='gazebo_entity',
            name='spawn_entity',
            output='screen',
            arguments=['-entity', 'simple_humanoid', '-file', urdf_file, '-x', '0', '-y', '0', '-z', '0.5']
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': open(urdf_file, 'r').read()}],
            arguments=[urdf_file]
        ),
    ])
