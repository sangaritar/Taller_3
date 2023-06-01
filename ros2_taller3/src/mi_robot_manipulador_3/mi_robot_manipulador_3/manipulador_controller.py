import rclpy
import serial,time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
from pynput import keyboard



class Robot_manipulador_controller(Node):
    def __init__(self):
     
     super().__init__('robot_manipulator_interface')
     self.publisher_graf = self.create_publisher(Vector3, '/robot_manipulator_graf', 10)
     self.subscription_vel = self.create_subscription(Vector3,'/robot_manipulator_vel', self.listener_callback,10)
     #self.susbscription_vel2 =  self.create_subscription(Vector3,'/robot_manipulator_goal', self.listener_callback,50)
     self.subscription_vel
     #self.susbscription_vel2

     self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
     
 
    def listener_callback(self, msg):

       rotacion = msg.x
       cuerpo = msg.y
       brazo = msg.z
       arduino = (str(rotacion) + "," + str(cuerpo) + "," + str(brazo) + "," +'p') 
       print("send" + arduino)
       self.ser.write(arduino.encode()) 
       #self.get_logger().info(str(msg))

    def recibir_mensaje(self):
      while True:
            linea = self.ser.readline().decode('utf-8').rstrip()
            if linea:
                  posx, posy, posz = linea.split(",")

                  entrada1 = posx
                  entrada2 = posy
                  entrada3 = posz

            message = Vector3()
            message.x = entrada1
            message.y = entrada2
            message.z = entrada3
        
            self.publisher_vel.publish(message)

def main():

        rclpy.init()
        robot_manipulator_controller = Robot_manipulador_controller()
        rclpy.spin(robot_manipulator_controller)
        robot_manipulator_controller.destroy_node()
        rclpy.shutdown()
       

if __name__ == '__main__':

        main()
