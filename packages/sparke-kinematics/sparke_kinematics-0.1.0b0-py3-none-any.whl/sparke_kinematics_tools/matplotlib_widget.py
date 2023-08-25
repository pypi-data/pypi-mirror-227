import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sparke_kinematics_tools.bezier_utils import *

class Matplotlib3DWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.button_pressed = False
        self.start_x = None
        self.start_y = None
        self.start_rotation = None
        self.trajectory = None
        self.points = None
        self.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion_notify)
        self.canvas.mpl_connect('button_release_event', self.on_button_release)

    def on_button_press(self, event):
        if event.button == Qt.LeftButton:
            self.button_pressed = True
            self.start_x = event.x
            self.start_y = event.y
            self.start_rotation = self.ax.azim, self.ax.elev

    def on_motion_notify(self, event):
        if self.button_pressed:
            dx = event.x - self.start_x
            dy = -(event.y - self.start_y)  # invert the y direction
            rotation = self.start_rotation[1] + dy/2, self.start_rotation[0] - dx/2
            self.ax.view_init(*rotation)
            self.canvas.draw()

    def on_button_release(self, event):
        if event.button == Qt.LeftButton:
            self.button_pressed = False

    def update_plot(self, positions, color='blue'):
        """
        Update the plot with an array of 3D positions, connected by a line with the specified color.
        :param positions: list of 3D positions, each of the form [x, y, z]
        :param color: optional color string for the line
        """
        xs, ys, zs = zip(*positions)
        self.ax.plot(xs, ys, zs, color=color)

        self.ax.set_xlim(-0.3, 0.3)
        self.ax.set_ylim(-0.2, 0.2)
        self.ax.set_zlim(-0.18384776, 0.18384776)

        self.canvas.draw()

    def plot_points(self, positions):
        """
        Plot each point in the list of positions as an independent point.
        :param positions: list of 3D positions, each of the form [x, y, z]
        """
        self.clear_points()
        xs, ys, zs = zip(*positions)
        
        self.points = self.ax.scatter(xs, ys, zs, color='cyan')

        self.ax.set_xlim(-0.3, 0.3)
        self.ax.set_ylim(-0.2, 0.2)
        self.ax.set_zlim(-0.18384776, 0.18384776)

        self.canvas.draw()

    def plot_trajectory(self, control_points):
        self.clear_trajectory()
        control_points = np.array(control_points)
        curve = bezier_curve(control_points)
        xs = curve[:, 0]
        ys = curve[:, 1]
        zs = curve[:, 2]
        self.trajectory, = self.ax.plot(xs, ys, zs, color='orange')
        self.canvas.draw()

    def clear_trajectory(self):
        if self.trajectory is not None:
            try:
                self.trajectory.remove()
            except:
                pass
        self.canvas.draw()

    def clear_points(self):
        if self.points is not None:
            try:
                self.points.remove()
            except:
                pass
        self.canvas.draw()

    def clear_plot(self):
        self.ax.clear()
        self.canvas.draw()