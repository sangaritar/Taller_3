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
        self.l1 = 102.4 # dimensión 1 (cm)
        self.l2 = 138.6  # dimensión 2 (cm)
        self.l3 = 155  # dimensión 3 (cm)


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
        
        distance = (((-self.x)**2 + (self.y)**2 + (self.z-self.l3)**2) - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2)
        theta1 = math.atan2(self.y, self.x)
        theta3 = math.atan2((-math.sqrt(1 - distance**2)), distance)
        theta2 = math.atan2(self.z - self.l3,math.sqrt(self.x**2+self.y**2)) - math.atan2((self.l2 * (-math.sqrt(1-distance**2))), (self.l1 + self.l2 * distance))  
        
        #Convertir angulos a valores entre -pi y pi
        if theta1 > math.pi:
            while theta1 > math.pi:
                theta1 = theta1 - math.pi
        elif theta1 < -math.pi:
            while theta1 < -math.pi:
                theta1 = theta1 + math.pi

        if theta2 > math.pi:
            while theta2 > math.pi:
                theta2 = theta2 - math.pi
        elif theta2 < -math.pi:
            while theta2 < -math.pi:
                theta2 = theta2 + math.pi

        if theta3 > math.pi:
            while theta3 > math.pi:
                theta3 = theta3 - math.pi
        elif theta3 < -math.pi:
            while theta3 < -math.pi:
                theta3 = theta3 + math.pi

        q1 = theta1
        q2 = theta2
        q3 = theta3

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
   
