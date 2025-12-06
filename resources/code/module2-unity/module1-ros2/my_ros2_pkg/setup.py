from setuptools import setup

package_name = 'my_ros2_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/my_ros2_pkg_launch.py']),
        ('share/' + package_name + '/urdf', ['urdf/basic_humanoid.urdf']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='Sample ROS 2 Python package for basic joint and sensor control',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher_node = my_ros2_pkg.publisher_node:main',
            'subscriber_node = my_ros2_pkg.subscriber_node:main',
        ],
    },
)
