from setuptools import setup

package_name = 'mi_robot_manipulador_3'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robotica',
    maintainer_email='angaritar0806@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'robot_manipulator_teleop = mi_robot_manipulador_3.TeleopRobot:main',
        'robot_manipulator_controller = mi_robot_manipulador_3.manipulador_controller:main',
        'robot_manipulator_planner = mi_robot_manipulador_3.manipulador_planner:main',
        'robot_manipulator_interface = mi_robot:manipulador_3.manipulador_vista:main',

        ],
    },
)
