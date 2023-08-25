from sparke_kinematics import base_transformations as basetf
from sparke_kinematics import leg_transformations as legtf
from sparke_kinematics.sparke_base_IK import SparkeBase
from sparke_kinematics.sparke_leg_IK import SparkeLeg
from PyQt5.QtWidgets import QTreeView, QApplication, QWidget, QVBoxLayout, QSizePolicy, QMainWindow
from PyQt5.QtCore import Qt, QModelIndex
import numpy as np
from mainwindow import Ui_MainWindow

def get_link_index(model, link_name):
    linkDict = {
        'Base': 0,
        'Front Left': 1,
        'Front Right': 2,
        'Back Left': 3,
        'Back Right': 4,
    }
    return model.index(linkDict[link_name], 0, QModelIndex())

def get_joint_index(model, link_index, joint_name):
    jointDict = {
        'Shoulder': 0,
        'Leg': 1,
        'Wrist': 2,
    }
    return model.index(jointDict[joint_name], 0, link_index)

def get_position_index(model, index):
    position_index = model.index(0,0,index)
    return position_index

def get_angle_index(model, index):
    angle_index = model.index(1,0,index)
    return angle_index

def get_positions(model, link_name, joint_name=None):
    link_index = get_link_index(model, link_name)
    if joint_name==None:
        position_index = get_position_index(model, link_index)
    else:
        position_index = get_position_index(model, get_joint_index(model, link_index, joint_name))
    positions = []
    for i in range(3):
        val_index = model.index(i,1,position_index)
        positions.append(float(val_index.data()))
    return positions

def set_positions(model, link_name, positions, joint_name=None):
    link_index = get_link_index(model, link_name)
    if joint_name==None:
        position_index = get_position_index(model, link_index)
    else:
        position_index = get_position_index(model, get_joint_index(model, link_index, joint_name))
    for i in range(3):
        val_index = model.index(i,1,position_index)
        val_model = val_index.model()
        val_model.setData(val_index, float(positions[i]))

def get_base_rotations(model):
    link_index = get_link_index(model, 'Base')
    base_rotation_index = model.index(1, 0, link_index)
    rotations = []
    for i in range(3):
        val_index = model.index(i,1,base_rotation_index)
        rotations.append(float(val_index.data()))
    return rotations

def set_base_rotations(model, rotations):
    link_index = get_link_index(model, 'Base')
    base_rotation_index = model.index(1, 0, link_index)
    for i in range(3):
        val_index = model.index(i,1,base_rotation_index)
        val_model = val_index.model()
        val_model.setData(val_index, float(rotations[i]))

def get_joint_angle(model, link_name, joint_name):
    link_index = get_link_index(model, link_name)
    angle_index = get_angle_index(model, get_joint_index(model, link_index, joint_name))
    val_index = model.index(0,1,angle_index)
    return float(val_index.data())

def set_joint_angle(model, link_name, joint_name, angle):
    angle = np.rad2deg(angle)
    angle = float(round(angle))
    link_index = get_link_index(model, link_name)
    angle_index = get_angle_index(model, get_joint_index(model, link_index, joint_name))
    val_index = model.index(0,1,angle_index)
    val_model = val_index.model()
    val_model.setData(val_index, float(angle))