import rclpy
import serial,time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
from pynput import keyboard
import threading
#from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import filedialog
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

global x, y, z

x = []
y = []
z = []

class Manipulador_interfaz:
    def __init__(self):
        super().__init__('robot_manipulator_interface')
        self.root = tk.Tk()
        self.root.title("Interfaz de usuario")
        self.create_graph()
        self.root.resizable(0,0)
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

         # Botón para guardar la imagen
        button_guardar = tk.Button(master=self.root, text="Guardar imagen", command=self.save_image)
        button_guardar.pack(side=tk.BOTTOM)

        self.root.mainloop()

        global x, y, z
        while True:
            linea = self.ser.readline().decode('utf-8').rstrip()
            if linea:
                posx, posy, posz = linea.split(",")

                x.append(posx)
                y.append(posy)
                z.append(posz)
     

    def create_graph(self):
        global x, y, z

        self.figura = plt.figure()
        self.ax = self.figura.add_subplot(111)
        self.ax.set_title("Gráfica del manipulador")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        # Animación de la gráfica
        canvas = FigureCanvasTkAgg(self.figura, master=self.root)
        canvas.get_tk_widget().pack()

        self.line, = self.ax.plot(x, y)
        self.ani = animation.FuncAnimation(self.figura, self.update, interval=100)
        '''
        self.figura = plt.figure()
        self.ax = self.figura.add_subplot(111, projection='3d')
        self.ax.set_title("Gráfica del manipulador")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")

        # Animación de la gráfica
        canvas = FigureCanvasTkAgg(self.figura, master=self.root)
        canvas.get_tk_widget().pack()

        self.line = self.ax.plot(x, y, z)[0]
        self.ani = animation.FuncAnimation(self.figura, self.update, interval=100)
        '''
    def update(self, i):
        '''
        global x, y, z
        self.line.set_data(x, y)
        self.line.set_3d_properties(z)
        return self.line
        '''
        global x, y
        self.line.set_data(x, y)
        return self.line

    def save_image(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            plt.savefig(filename)

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
        robot_manipulator_interface = Manipulador_interfaz()
        rclpy.spin(robot_manipulator_interface)
        robot_manipulator_interface.destroy_node()
        rclpy.shutdown()
       

if __name__ == '__main__':

        main()