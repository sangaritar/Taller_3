import rclpy
import serial,time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Vector3


class Robot_manipulador_controller(Node):
    def __init__(self):
     
     super().__init__('robot_manipulator_controller')
     self.subscription_vel = self.create_subscription(Vector3,'/robot_manipulator_vel', self.listener_callback,10)
     self.publisher_graf = self.create_publisher(Vector3, '/robot_manipulator_graf', 10)
     #self.susbscription_vel2 =  self.create_subscription(Vector3,'/robot_manipulator_goal', self.listener_callback,50)
     self.subscription_vel
     self.publisher_graf
     #self.susbscription_vel2

     self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
     
 
    def listener_callback(self, msg):

       rotacion = msg.x
       cuerpo = msg.y
       brazo = msg.z
       arduino = (str(rotacion) + "," + str(cuerpo) + "," + str(brazo) + "," +'p') 
       print("send " + arduino)
       self.ser.write(arduino.encode()) 
       self.recibir_mensaje()
       #self.get_logger().info(str(msg))

    def recibir_mensaje(self):

      l = self.ser.readline()
      print(l)
      linea = l.decode('utf-8').rstrip()
      print(linea)
      if linea:
            sp = linea.split(",")
            posx, posy, posz = sp[0], sp[1], sp[2]

            entrada1 = float(posx)
            entrada2 = float(posy)
            entrada3 = float(posz)

            message = Vector3()
            message.x = entrada1
            message.y = entrada2
            message.z = entrada3

            print(message)
      
      #self.publisher_vel.publish(message)

def main():

        rclpy.init()
        robot_manipulator_controller = Robot_manipulador_controller()
        rclpy.spin(robot_manipulator_controller)
        robot_manipulator_controller.destroy_node()
        rclpy.shutdown()
       

if __name__ == '__main__':

        main()
