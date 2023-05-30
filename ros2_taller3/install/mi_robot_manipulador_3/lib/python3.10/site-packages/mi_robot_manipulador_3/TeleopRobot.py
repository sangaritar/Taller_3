import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
from pynput import keyboard
from pynput import keyboard as kb


class TeleopRobot(Node):
    def __init__(self):
        super().__init__('robot_manipulator_teleop')  
        self.publisher_vel = self.create_publisher(Vector3, '/robot_manipulator_vel', 10)

        timer_period= 0.5

        rotacion = input("Ingrese cuantos grados desea rotar el brazo:")

        print("El valor ingresado es:" , rotacion)

        self.rotacion= float(rotacion)

        cuerpo = input(" Ingrese la velocidad con la que desea mover el cuerpo:")

        print("El valor ingresado es:" , cuerpo)

        self.cuerpo = float(cuerpo)

        brazo = input("Ingrese la velocidad con la que desea mover el brazo:")

        print("El valor ingresado es:" , brazo)

        self.brazo= float(brazo)

        self.timer = self.create_timer(timer_period, self.publicar)

        self.velocity = {'rotacion': 0.0, 'cuerpo': 0.0, 'brazo': 0.0}
        
    def on_press(self, key):
        try:
            # Rotacion
            if key.char == 'q':
                self.velocity = {'rotacion': self.rotacion, 'cuerpo': 0.0, 'brazo': 0.0}
            elif key.char == 'a':
                self.velocity = {'rotacion': -self.rotacion, 'cuerpo': 0.0, 'brazo': 0.0}
            
            # Cuerpo 
            elif key.char == 'w':
                self.velocity = {'rotacion': 0.0, 'cuerpo': self.cuerpo, 'brazo': 0.0}
            elif key.char == 's':
                self.velocity = {'rotacion': 0.0, 'cuerpo': -self.cuerpo, 'brazo': 0.0}

            #Brazo
            elif key.char == 'e':
                self.velocity = {'rotacion': 0.0, 'cuerpo': 0.0, 'brazo': self.brazo}
            elif key.char == 'd':
                self.velocity = {'rotacion': 0.0, 'cuerpo': 0.0, 'brazo': -self.brazo}
        
            self.publicar(self.velocity['rotacion'], self.velocity['cuerpo'], self.velocity['brazo'])
            

        except AttributeError:
            print('Esa tecla no es valida')
            pass

        
    def on_release(self, key):
        self.velocity = {'rotacion': 0.0, 'cuerpo': 0.0, 'brazo': 0.0}
        self.publicar(self.velocity['rotacion'], self.velocity['cuerpo'], self.velocity['brazo'])
    
    def publicar(self,rotacion,cuerpo,brazo):
        message = Vector3()
        message.x = rotacion
        message.y = cuerpo
        message.z = brazo
        
        self.publisher_vel.publish(message)
        self.get_logger().info(str(message))

def main():
    rclpy.init()
    robot_manipulator_teleop = TeleopRobot()

    with kb.Listener(robot_manipulator_teleop.on_press, robot_manipulator_teleop.on_release) as escuchador:

        escuchador.join()

    rclpy.spin(robot_manipulator_teleop)
    robot_manipulator_teleop.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
