import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import matplotlib.animation as animation
from tkinter import filedialog
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Manipulador_interfaz(Node):
    def __init__(self):
        super().__init__('robot_manipulator_interface')
        self.subscription_graf = self.create_subscription(Vector3,'/robot_manipulator_graf', self.listener_callback,10)
        self.bandera_llego = False
        self.root = tk.Tk()
        self.root.title("Interfaz de usuario")
        self.create_graph()
        self.root.resizable(0,0)

        # Botón para guardar la imagen
        button_guardar = tk.Button(master=self.root, text="Guardar imagen", command=self.save_image)
        button_guardar.pack(side=tk.BOTTOM)
        self.root.mainloop()

    def listener_callback(self, msg):

       self.x = msg.x
       self.y = msg.y
       self.z = msg.z
       self.bandera_llego = True
       self.update(0)
       arduino = (str(self.x) + "," + str(self.y) + "," + str(self.z) + "," +'p')  
       print("send_grafica " + arduino)


    def create_graph(self):
        self.figura = plt.figure()
        self.ax = self.figura.add_subplot(111, projection='3d')
        self.ax.set_title("Gráfica del manipulador")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")

        # Animación de la gráfica
        canvas = FigureCanvasTkAgg(self.figura, master=self.root)
        canvas.get_tk_widget().pack()

        self.line = self.ax.plot([], [], [])[0]
        self.ani = animation.FuncAnimation(self.figura, self.update, frames=range(100), interval=100)

    def update(self, i):

        if self.bandera_llego == True:
            self.line.set_data([self.x], [self.y])
            self.line.set_3d_properties([self.z])
            return self.line
        else:
             pass

    def save_image(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            plt.savefig(filename)

def main():
        rclpy.init()
        robot_manipulator_interface = Manipulador_interfaz()
        rclpy.spin('robot_manipulator_interface')
        robot_manipulator_interface.destroy_node()
        rclpy.shutdown()
       

if __name__ == '__main__':
        main()