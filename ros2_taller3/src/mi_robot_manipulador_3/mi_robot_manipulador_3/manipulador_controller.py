import rclpy
import serial,time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
from pynput import keyboard


class Robot_manipulador_controller(Node):
    def __init__(self):
     
     super().__init__('robot_manipulator_interface')
     self.subscription_vel = self.create_subscription(Vector3,'/robot_manipulator_vel', self.listener_callback,50)
     #self.susbscription_vel2 =  self.create_subscription(Vector3,'/robot_manipulator_goal', self.listener_callback,50)
     self.subscription_vel
     #self.susbscription_vel2

     self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
     
 
    def listener_callback(self, msg):
       global x, y, z
       rotacion = msg.x
       cuerpo = msg.y
       brazo = msg.z
       arduino = (str(rotacion) + "," + str(cuerpo) + "," + str(brazo) + "," +'p') 
       print("send" + arduino)
       self.ser.write(arduino.encode()) 
       #self.get_logger().info(str(msg))

'''
class MyThread(threading.Thread):
    def __init__(self, node, gui):
          threading.Thread.__init__(self)
          self.node = node
          self.gui = gui
    
    def run(self):
          while True:
            rclpy.spin_once(self.node)
'''

def main():
        '''
        rclpy.init()
        my_node = Robot_manipulador_interfaces()
        my_thread = MyThread(my_node, None)
        my_thread.start()
        my_gui = InterfazManipulador()
        rclpy.spin(my_node)
        rclpy.shutdown
        '''
        rclpy.init()
        robot_manipulator_controller = Robot_manipulador_controller()
        rclpy.spin(robot_manipulator_controller)
        robot_manipulator_controller.destroy_node()
        rclpy.shutdown()
       

if __name__ == '__main__':

        main()
