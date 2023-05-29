import rclpy
import serial
import time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
from pynput import keyboard
import threading
from math import pi, atan2, sqrt
import math

class RobotManipulatorPlanner(Node):
    def __init__(self):
        super().__init__('robot_manipulator_planner')
        self.publisher_vel = self.create_publisher(Vector3, '/robot_manipulator_goal', 10)

        # Definir dimensiones del robot 
        self.l1 = 0.5  # dimensión 1 (metros)
        self.l2 = 0.5  # dimensión 2 (metros)
        self.l3 = 0.5  # dimensión 3 (metros)

        # Se pregunta al usuario que valores desea ingresar
        while True:
            try:
                self.x = float(input("Ingrese la coordenada x que desea de la posición del end-effector : "))
                self.y = float(input("Ingrese la coordenada y que desea de la posición del end-effector : "))
                self.z = float(input("Ingrese la coordenada z que desea de la posición del end-effector : "))
                break
            except ValueError:
                print("Entrada invalida. Porfavor ingrese un número.")

    def cinematicaInversa(self):
       
        # Calculos de cinematica inversa
        
        q1 = atan2(self.y, self.x)
        d = sqrt(self.x**2 + self.y**2)
        a = self.z - self.l1
        alpha = atan2(a, d)
        q2 = pi/2 - alpha - atan2(sqrt(self.l3**2 - self.l2**2), self.l2 + self.l3*math.cos(alpha + pi/2))
        q3 = pi - atan2(self.l2*math.sin(pi - q2 - alpha) + self.l3*math.sin(alpha + pi/2), self.l2*math.cos(pi - q2 - alpha) + self.l3*math.cos(alpha + pi/2))

        self.publicar(q1, q2, q3)
    
    def publicar(self, q1, q2, q3):
        msg = Vector3(x=q1, y=q2, z=q3)
        self.publisher_vel.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotManipulatorPlanner()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
   
