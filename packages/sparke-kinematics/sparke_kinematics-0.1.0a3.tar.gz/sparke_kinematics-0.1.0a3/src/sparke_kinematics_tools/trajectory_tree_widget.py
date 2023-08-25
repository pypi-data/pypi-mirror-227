from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QApplication, QWidget, QVBoxLayout, QSizePolicy, QMainWindow
from sparke_kinematics_tools.trajectory_utils import *
class TrajectoryTree(QWidget):
    DEFAULT_VEL = [
        0.1, 0.0, 0.0, 0.0, 0.0, 0.0,
    ]
    END_POINT = [0.10807106781186548, 0.11, -0.18384776310850237]
    DEFAULT_CONTROL_POINTS = [
        [END_POINT[0] - DEFAULT_VEL[0], END_POINT[1], END_POINT[2]], #0
        [END_POINT[0] - DEFAULT_VEL[0] - 0.01, END_POINT[1], END_POINT[2]], #1
        [END_POINT[0] - DEFAULT_VEL[0] - 0.02, END_POINT[1], END_POINT[2]+0.03], #2
        [END_POINT[0] - DEFAULT_VEL[0] - 0.02, END_POINT[1], END_POINT[2]+0.03], #3
        [END_POINT[0] - DEFAULT_VEL[0] - 0.02, END_POINT[1], END_POINT[2]+0.03], #4
        [END_POINT[0] - (DEFAULT_VEL[0]/2), END_POINT[1], END_POINT[2]+0.03], #5
        [END_POINT[0] - (DEFAULT_VEL[0]/2), END_POINT[1], END_POINT[2]+0.03], #6
        [END_POINT[0] - (DEFAULT_VEL[0]/2), END_POINT[1], END_POINT[2]+0.05], #7
        [END_POINT[0]+0.02, END_POINT[1], END_POINT[2]+0.05], #8 
        [END_POINT[0]+0.02, END_POINT[1], END_POINT[2]+0.05], #9 
        [END_POINT[0]+0.01, END_POINT[1], END_POINT[2]], #10
        END_POINT,
    ]

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.__parent = parent
        self.ui = parent.ui
        # Initialize the model and set the headers for the tree
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Control Points', ''])
        self.tree = QTreeView(self)
        self.tree.setModel(self.model)
        self.tree.setColumnWidth(0, 125)
        self.tree.setColumnWidth(1, 50)
        self.tree_model = self.tree.model()

        self.points_enabled = False

        # Add some items to the tree, with the first column unable to be edited
        self.parent_item = self.model.invisibleRootItem()

        self.parent_item.appendRow([self.generate_velocity_item(), self.generate_empty_item()])

        point_items = self.generate_point_items()
        for point in point_items:
            self.parent_item.appendRow([point, self.generate_empty_item()])

        set_velocity(self.tree_model, self.DEFAULT_VEL)
        set_points(self.tree_model, self.DEFAULT_CONTROL_POINTS)

        self.__parent.plot_widget.plot_points(self.DEFAULT_CONTROL_POINTS)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)

    def generate_velocity_item(self):
        vel_item = QStandardItem('Velocity')
        vel_item.setEditable(False)
        vel_item.appendRow([self.generate_linear_vel_item(), self.generate_empty_item()])
        vel_item.appendRow([self.generate_angular_vel_item(), self.generate_empty_item()])
        return vel_item

    def generate_linear_vel_item(self):
        linear_vel_parent_item = QStandardItem('Linear')
        linear_vel_parent_item.setEditable(False)
        linear_vels = ['X', 'Y', 'Z']
        for vel in linear_vels:
            vel_item = QStandardItem(vel)
            vel_item.setEditable(False)
            if vel == 'Z':
                editing = False
            else:
                editing = True
            linear_vel_parent_item.appendRow([vel_item, self.generate_empty_item(editing)])
        return linear_vel_parent_item
    
    def generate_angular_vel_item(self):
        angular_vel_parent_item = QStandardItem('Angular')
        angular_vel_parent_item.setEditable(False)
        angular_vels = ['X\'', 'Y\'', 'Z\'']
        for vel in angular_vels:
            vel_item = QStandardItem(vel)
            vel_item.setEditable(False)
            if vel == 'Z\'':
                editing = True
            else:
                editing = False
            angular_vel_parent_item.appendRow([vel_item, self.generate_empty_item(editing)])
        return angular_vel_parent_item

    def generate_point_items(self):
        points = []
        for i in range(12):
            points.append(f'P{i+1}')
        
        positions = ['X', 'Y', 'Z']
            
        point_items = []
        for i in range(len(points)):
            pos_parent_item = QStandardItem(points[i])
            pos_parent_item.setEditable(False)
            if i in range(1,11):
                editing = True
            else:
                editing = False
            for position in positions:
                position_item = QStandardItem(position)
                position_item.setEditable(False)
                pos_parent_item.appendRow([position_item, self.generate_empty_item(editing)])
            point_items.append(pos_parent_item)
        return point_items
    
    def generate_empty_item(self, editable = False):
        item = QStandardItem('')
        item.setEditable(editable)
        return item

    def toggle_points(self):
        self.points_enabled = not self.points_enabled
        if self.points_enabled:
            control_points = self.generate_control_points()
            self.__parent.plot_widget.plot_points(control_points)
        else:
            self.__parent.plot_widget.clear_points()
    
    def reset_trajectory(self):
        set_points(self.tree_model, self.DEFAULT_CONTROL_POINTS)

    def reset_velocity(self):
        set_velocity(self.tree_model, self.DEFAULT_VEL)

    def plot_trajectory(self):
        control_points = self.generate_control_points()
        self.__parent.plot_widget.plot_trajectory(control_points)

    def generate_control_points(self):
        model = self.tree.model()
        vel = get_velocity(self.tree_model)
        points = get_points(self.tree_model)

        points[0][0] = self.END_POINT[0] - vel[0]
        points[0][1] = self.END_POINT[1] - vel[1]
        points[0][2] = self.END_POINT[2] - vel[2]
        points[11] = self.END_POINT
        
        model.blockSignals(True)
        set_points(self.tree_model, points)
        model.blockSignals(False)
        return points
        
    def data_changed(self):
        if self.points_enabled:
            control_points = self.generate_control_points()
            self.__parent.plot_widget.plot_points(control_points)