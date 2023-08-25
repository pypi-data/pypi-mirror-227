from sparke_kinematics import base_transformations as basetf
from sparke_kinematics import leg_transformations as legtf
# from sparke_kinematics.sparke_base_IK import SparkeBase
from matplotlib_widget import Matplotlib3DWidget
from sparke_kinematics.sparke_leg_IK import SparkeLeg
from PyQt5.QtWidgets import QTreeView, QApplication, QWidget, QVBoxLayout, QSizePolicy, QMainWindow
import numpy as np
from mainwindow import Ui_MainWindow
from kinematics_controller_utils import *
import forward_kinematics_utils as fk_utils
import time
import copy
class kinematicsController():
    HOME_POSITIONS = [
            [0.101, 0.055, 0.], #Base FL
            [0.101, 0.11, 0.], #FL Shoulder
            [0.01261165, 0.11, -0.08838835], #FL Leg
            [0.10807107, 0.11, -0.18384776], #FL Wrist
            [0.101, -0.055, 0.], #Base FR
            [0.101, -0.11, 0.], #FR Shoulder
            [0.01261165, -0.11, -0.08838835], #FR Leg
            [0.10807107, -0.11, -0.18384776], #FR Wrist
            [-0.101, 0.055, 0.], #Base BL
            [-0.101, 0.11, 0.], #BL Shoulder
            [-0.18938835, 0.11, -0.08838835], #BL Leg
            [-0.09392893, 0.11, -0.18384776], #BL Wrist
            [-0.101, -0.055, 0.], #Base BR
            [-0.101, -0.11, 0.], #BR Shoulder
            [-0.18938835, -0.11, -0.08838835], #BR Leg
            [-0.09392893, -0.11, -0.18384776], #BR Wrist
    ]
    HOME_ANGLES = [
        [0, 0.7853981633974481, 1.5707963267948968],
        [0, 0.7853981633974481, 1.5707963267948968],
        [0, 0.7853981633974481, 1.5707963267948968],
        [0, 0.7853981633974481, 1.5707963267948968],
    ]
    JOINT_DICT = {
            0: 'Shoulder',
            1: 'Leg',
            2: 'Wrist',
        }
    LEG_DICT = {
            0: 'Front Left',
            1: 'Front Right',
            2: 'Back Left',
            3: 'Back Right',
        }
    
    def __init__(self, parent, model, plot_widget):
        self.current_positions = copy.deepcopy(kinematicsController.HOME_POSITIONS)
        self.current_angles = copy.deepcopy(kinematicsController.HOME_ANGLES)
        self.parent = parent
        self.model = model
        self.plot_widget: Matplotlib3DWidget
        self.plot_widget = plot_widget
        self.sparke_legs = []
        for leg in range(1, 5):
            self.sparke_legs.append(SparkeLeg(leg))
        self.home()

    def home(self):
        self.model.blockSignals(True)
        self.current_positions = copy.deepcopy(kinematicsController.HOME_POSITIONS)
        self.current_angles = copy.deepcopy(kinematicsController.HOME_ANGLES)
        self.Tm = basetf.create_base_transformation(0, 0, 0, 0, 0, 0)
        set_positions(self.model, 'Base', [0.,0.,0.])
        set_base_rotations(self.model, [0.,0.,0.])
        for i in range(4):
            self.sparke_legs[i].update_Tb0(self.Tm)
            set_positions(self.model, kinematicsController.LEG_DICT[i], kinematicsController.HOME_POSITIONS[(4*i)+1], kinematicsController.JOINT_DICT[0])
            set_positions(self.model, kinematicsController.LEG_DICT[i], kinematicsController.HOME_POSITIONS[(4*i)+2], kinematicsController.JOINT_DICT[1])
            set_positions(self.model, kinematicsController.LEG_DICT[i], kinematicsController.HOME_POSITIONS[(4*i)+3], kinematicsController.JOINT_DICT[2])
            set_joint_angle(self.model, kinematicsController.LEG_DICT[i], kinematicsController.JOINT_DICT[0], kinematicsController.HOME_ANGLES[i][0])
            set_joint_angle(self.model, kinematicsController.LEG_DICT[i], kinematicsController.JOINT_DICT[1], kinematicsController.HOME_ANGLES[i][1])
            set_joint_angle(self.model, kinematicsController.LEG_DICT[i], kinematicsController.JOINT_DICT[2], kinematicsController.HOME_ANGLES[i][2])
        self.model.blockSignals(False)
        self.update_plot()
        
    def solve_ik(self):
        old_angles = copy.deepcopy(self.current_angles)
        old_positions = copy.deepcopy(self.current_positions)
        self.update_Tm()
        try:
            for i in range(4):
                end_effector_positions = get_positions(self.model, kinematicsController.LEG_DICT[i], 'Wrist')
                self.sparke_legs[i].solve_angles(self.Tm, end_effector_positions[0], end_effector_positions[1], end_effector_positions[2])
                self.current_angles[i][0] = self.sparke_legs[i].theta1
                self.current_angles[i][1] = self.sparke_legs[i].theta2
                self.current_angles[i][2] = self.sparke_legs[i].theta3
                for j in range(3):
                    set_joint_angle(self.model, kinematicsController.LEG_DICT[i], kinematicsController.JOINT_DICT[j], self.current_angles[i][j])
            self.solve_fk()
        except:
            print('No Possible Solution For Given End Effectors')
            self.restore_old_angles(old_angles)
            self.restore_old_positions(old_positions)

    def solve_fk(self):
        old_positions = copy.deepcopy(self.current_positions)
        old_angles = copy.deepcopy(self.current_angles)
        try:
            self.update_Tm()
            self.current_angles = self.get_angles_from_tree()
            for i in range(4):
                positions = fk_utils.get_leg_positions(self.sparke_legs[i], self.Tm, self.current_angles[i])
                self.current_positions[(i*4)] = positions[0]
                self.current_positions[(i*4)+1] = positions[1]
                self.current_positions[(i*4)+2] = positions[2]
                self.current_positions[(i*4)+3] = positions[3]
            self.set_tree_to_current_vals()        
        except:
            print('Invalid Inputs For FK, Unable to Solve')
            self.restore_old_positions(old_positions)
            self.restore_old_angles(old_angles)
                
    def data_changed(self):
        self.model.blockSignals(True)
        if(self.data_different()):
            mode = self.parent.kinematics_tree_widget.mode
            if(mode == 'fk'):
                self.solve_fk()
            if(mode == 'ik'):
                self.solve_ik()
            self.update_plot()
        self.model.blockSignals(False)

    def data_different(self):
        if(self.current_angles == self.get_angles_from_tree()):
            if(self.current_positions == self.get_positions_from_tree()):
                if(self.base_positions == get_positions(self.model, 'Base')):
                    if(self.base_rotations == get_base_rotations(self.model)):
                        return False
        return True

    def update_plot(self):
        # Retrieve the updated data from the model
        # and perform calculations to get new x, y, and z values
        self.plot_widget.clear_plot()
        colors = {
            0: 'blue',
            1: 'red',
            2: 'green',
            3: 'purple',
        }
        base_array = [
            self.current_positions[0],
            self.current_positions[4],
            self.current_positions[12],
            self.current_positions[8],
            self.current_positions[0],
        ]
        self.plot_widget.update_plot(base_array, color='orange')

        for i in range(4):
            array = []
            array.append(self.current_positions[(4*i)])
            array.append(self.current_positions[(4*i)+1])
            array.append(self.current_positions[(4*i)+2])
            array.append(self.current_positions[(4*i)+3])
            self.plot_widget.update_plot(array, colors[i])

    def set_tree_to_current_vals(self):
        for i in range(4):
            set_positions(self.model, kinematicsController.LEG_DICT[i], self.current_positions[(4*i)+1], kinematicsController.JOINT_DICT[0])
            set_positions(self.model, kinematicsController.LEG_DICT[i], self.current_positions[(4*i)+2], kinematicsController.JOINT_DICT[1])
            set_positions(self.model, kinematicsController.LEG_DICT[i], self.current_positions[(4*i)+3], kinematicsController.JOINT_DICT[2])
            set_joint_angle(self.model, kinematicsController.LEG_DICT[i], kinematicsController.JOINT_DICT[0], self.current_angles[i][0])
            set_joint_angle(self.model, kinematicsController.LEG_DICT[i], kinematicsController.JOINT_DICT[1], self.current_angles[i][1])
            set_joint_angle(self.model, kinematicsController.LEG_DICT[i], kinematicsController.JOINT_DICT[2], self.current_angles[i][2])

    def restore_old_positions(self, old_positions):
        self.current_positions = copy.deepcopy(old_positions)
        for i in range(4):
            set_positions(self.model, kinematicsController.LEG_DICT[i], self.current_positions[(4*i)+1], \
                            kinematicsController.JOINT_DICT[0])
            set_positions(self.model, kinematicsController.LEG_DICT[i], self.current_positions[(4*i)+2], \
                            kinematicsController.JOINT_DICT[1])
            set_positions(self.model, kinematicsController.LEG_DICT[i], self.current_positions[(4*i)+3], \
                            kinematicsController.JOINT_DICT[2])
            
    def restore_old_angles(self, old_angles):
        self.current_angles = copy.deepcopy(old_angles)
        for i in range(4):
            for j in range(3):
                set_joint_angle(self.model, kinematicsController.LEG_DICT[i], kinematicsController.JOINT_DICT[j], self.current_angles[i][j])

    def update_Tm(self):
        self.base_positions = get_positions(self.model, 'Base')
        self.base_rotations = get_base_rotations(self.model)
        self.Tm = basetf.create_base_transformation(self.base_positions[0], self.base_positions[1], self.base_positions[2], \
                                                     self.base_rotations[0], self.base_rotations[1], self.base_rotations[2])

    def get_angles_from_tree(self):
        angles = []
        for i in range(4):
            joint_angles = []
            for j in range(3):
                angle = get_joint_angle(self.model, kinematicsController.LEG_DICT[i], kinematicsController.JOINT_DICT[j])
                joint_angles.append(float(np.deg2rad(angle)))
            angles.append(joint_angles)
        return angles
    
    def get_positions_from_tree(self):
        positions = []
        for i in range(4):
            for j in range(3):
                position = get_positions(self.model, kinematicsController.LEG_DICT[i], kinematicsController.JOINT_DICT[j])
                positions.append(position)
        return positions