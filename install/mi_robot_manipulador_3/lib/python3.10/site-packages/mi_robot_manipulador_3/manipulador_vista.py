import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d


class Manipulador_interfaz(Node):
    def __init__(self):
        super().__init__('robot_manipulator_interface')
        self.subscription_graf = self.create_subscription(Vector3, '/robot_manipulator_graf', self.listener_callback, 10)
        self.bandera_llego = False

        # Crear la figura y el eje 3D
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Coordenadas acumulativas
        self.cumulative_x = []
        self.cumulative_y = []
        self.cumulative_z = []

    def listener_callback(self, msg):
        self.bandera_llego = True
        x = msg.x
        y = msg.y
        z = msg.z

        # Agregar las coordenadas a las coordenadas acumulativas
        if not self.cumulative_x:
            # Si es la primera coordenada, simplemente la agregamos
            self.cumulative_x.append(x)
            self.cumulative_y.append(y)
            self.cumulative_z.append(z)
        else:
            # Si ya hay coordenadas acumulativas, sumamos las nuevas coordenadas a las existentes
            last_x = self.cumulative_x[-1]
            last_y = self.cumulative_y[-1]
            last_z = self.cumulative_z[-1]
            self.cumulative_x.append(last_x + x)
            self.cumulative_y.append(last_y + y)
            self.cumulative_z.append(last_z + z)

        # Llamar a la función para actualizar la gráfica
        self.update_graph()

    def update_graph(self):
        # Limpiar la gráfica
        self.ax.clear()

        # Dibujar la gráfica de línea en 3D
        self.ax.plot(self.cumulative_x, self.cumulative_y, self.cumulative_z)

        # Establecer etiquetas de los ejes
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Actualizar la gráfica
        plt.draw()
        plt.pause(0.001)


def main():
    rclpy.init()
    robot_manipulator_interface = Manipulador_interfaz()
    rclpy.spin(robot_manipulator_interface)  # Pass the instance, not the string
    robot_manipulator_interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
