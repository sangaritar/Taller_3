import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Vector3


class RobotManipulatorTareaf(Node):
    def __init__(self):
        super().__init__('robot_manipulator_tarea')
        self.publisher_f = self.create_publisher(Vector3, '/robot_manipulator_vel', 10)

        gRot = float(45)
        gj1 = float(105)
        gj2 = float(45)
        

        message = Vector3()
        message.x = gRot
        message.y = gj1
        message.z = gj2
        self.publisher_f.publish(message)

def main():
    rclpy.init()
    node = RobotManipulatorTareaf()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
   