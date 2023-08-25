import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTreeWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QModelIndex
from mainwindow import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib_widget import Matplotlib3DWidget
from kinematics_tree_widget import KinematicsTree
from trajectory_tree_widget import TrajectoryTree
from kinematics_controller import kinematicsController
import csv

class App(QMainWindow):
    kinematics_data_changed_signal = pyqtSignal(QModelIndex, QModelIndex)
    trajectory_data_changed_signal = pyqtSignal(QModelIndex, QModelIndex)
    kinematics_header = [
        '',
        'X',
        'Y',
        'Z',
        'θ',
    ]
    trajectory_header = [
        'Point',
        'X',
        'Y',
        'Z',
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Robot Dog Control')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))

        # Set up the UI from the converted Python module
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Get the plot widget and layout from the UI
        self.plot_widget = Matplotlib3DWidget(self)
        self.plot_layout = self.ui.plot_layout
        self.plot_layout.addWidget(self.plot_widget)

        self.kinematics_tree_widget = KinematicsTree(self)
        self.kinematics_tree_layout = self.ui.kinematics_tree_layout
        self.kinematics_tree_layout.addWidget(self.kinematics_tree_widget)
        kinematics_model = self.kinematics_tree_widget.tree.model()

        self.trajectory_tree_widget = TrajectoryTree(self)
        self.trajectory_tree_layout = self.ui.trajectory_tree_layout
        self.trajectory_tree_layout.addWidget(self.trajectory_tree_widget)
        trajectory_model = self.trajectory_tree_widget.tree.model()
        
        self.controller = kinematicsController(self, kinematics_model, self.plot_widget)
        # Connect the dataChanged signal to the controller's slot
        self.kinematics_data_changed_signal.connect(self.controller.data_changed)
        self.trajectory_data_changed_signal.connect(self.trajectory_tree_widget.data_changed)
        self.ui.actionReset.triggered.connect(self.reset_triggered)
        self.ui.actionExportKinematics.triggered.connect(self.export_kinematics)
        self.ui.actionExportPoints.triggered.connect(self.export_points)
        self.ui.toggle_points_button.pressed.connect(self.trajectory_tree_widget.toggle_points)
        self.ui.clear_trajectory_plot_button.pressed.connect(self.plot_widget.clear_trajectory)
        self.ui.plot_trajectory_button.pressed.connect(self.trajectory_tree_widget.plot_trajectory)

        # Emit the signal when the model's data changes
        kinematics_model.dataChanged.connect(lambda i1, i2: self.kinematics_data_changed_signal.emit(i1, i2))
        trajectory_model.dataChanged.connect(lambda i1, i2: self.trajectory_data_changed_signal.emit(i1, i2))

    def reset_triggered(self):
        self.controller.home()
        self.trajectory_tree_widget.reset_trajectory()
        self.trajectory_tree_widget.reset_velocity()

    def export_kinematics(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Export Kinematics", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            if fileName.endswith('.csv'):
                angles = self.controller.get_angles_from_tree()
                positions = self.controller.get_positions_from_tree()
                with open(fileName, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(self.kinematics_header)
                    for i in range(4):
                        writer.writerow([self.controller.LEG_DICT[i]])
                        for j in range(3):
                            writer.writerow([self.controller.JOINT_DICT[j], positions[(i*3)+j][0], \
                                            positions[(i*3)+j][1], positions[(i*3)+j][2], angles[i][j]])

    def export_points(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Export Points", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            if fileName.endswith('.csv'):
                control_points = self.trajectory_tree_widget.generate_control_points()
                with open(fileName, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(self.trajectory_header)
                    for i in range(12):
                        writer.writerow([i, control_points[i][0], control_points[i][1], control_points[i][2]])
                    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
