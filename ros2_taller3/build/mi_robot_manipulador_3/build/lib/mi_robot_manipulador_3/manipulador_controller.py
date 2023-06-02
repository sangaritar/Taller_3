import rclpy
import serial,time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
import math


class Robot_manipulador_controller(Node):
    def __init__(self):
     
     super().__init__('robot_manipulator_controller')
     self.subscription_vel = self.create_subscription(Vector3,'/robot_manipulator_vel', self.listener_callback,10)
     self.publisher_graf = self.create_publisher(Vector3, '/robot_manipulator_graf', 10)
     self.susbscription_vel2 =  self.create_subscription(Vector3,'/robot_manipulator_goal', self.listener_callback,10)
     self.subscription_vel
     self.publisher_graf
     self.susbscription_vel2

     self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
     
 
    def listener_callback(self, msg):

       rotacion = msg.x
       cuerpo = msg.y
       brazo = msg.z
       arduino = (str(rotacion) + "," + str(cuerpo) + "," + str(brazo) + "," +'p') 
       print("send " + arduino)
       self.ser.write(arduino.encode()) 
       #self.get_logger().info(str(msg))

    def cinematica_directa(self, rotacion, cuerpo, brazo):

      posin_rota = 45 
      posin_cuerpo = 45
      posin_brazo = 45

      posicion_actual_rota = posin_rota + rotacion
      posicion_actual_cuerpo = posin_cuerpo + cuerpo
      posicion_actual_brazo = posin_brazo + brazo

      theta1 = posicion_actual_rota  # Ángulo de rotación del servo 1
      theta2 = posicion_actual_cuerpo  # Ángulo de rotación del servo 2
      theta3 = posicion_actual_brazo  # Ángulo de rotación del servo 3

      #Condiciones del manipulador (longitudes)
      distancia1 = 102.4
      distancia2 = 138.6
      distancia3 = 155

      dis_x = distancia1*math.cos(theta2)*math.cos(theta1) + distancia2*math.cos(theta2 + theta3)*math.cos(theta1)
      dis_y = distancia1*math.cos(theta2)*math.sin(theta1) + distancia2*math.cos(theta2 + theta3)*math.sin(theta1)
      dis_z = distancia3 + distancia1*math.sin(theta2) + distancia2*math.sin(theta2 + theta3)

      message_graf = Vector3()
      message_graf.x = dis_x
      message_graf.y = dis_y
      message_graf.z = dis_z
      
      self.publisher_graf.publish(message_graf)

def main():

        rclpy.init()
        robot_manipulator_controller = Robot_manipulador_controller()
        rclpy.spin(robot_manipulator_controller)
        robot_manipulator_controller.destroy_node()
        rclpy.shutdown()
       

if __name__ == '__main__':

        main()
