from setuptools import setup
import os
from glob import glob

package_name = 'my_gazebo_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob(os.path.join('launch', '*_launch.py'))),
        ('share/' + package_name + '/models', glob(os.path.join('models', '**', '*'), recursive=True)), # Placeholder for Gazebo models
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='ROS 2 Python package for Gazebo integration, including simulated sensors',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Placeholder for nodes that will publish sensor data or control the robot in Gazebo
        ],
    },
)