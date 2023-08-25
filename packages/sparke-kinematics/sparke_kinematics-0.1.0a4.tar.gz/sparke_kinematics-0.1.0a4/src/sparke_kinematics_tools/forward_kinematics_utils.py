import numpy as np
from sparke_kinematics.sparke_leg_IK import SparkeLeg
import sparke_kinematics.leg_transformations as legtf

def get_leg_positions(leg: SparkeLeg, Tm: np.matrix, angles):
    leg.update_Tb0(Tm)
    leg_positions = []
    leg_positions.append(get_postions_from_tf(leg.t_b0))
    leg_positions.append(get_postions_from_tf(get_fk_tb1(leg.t_b0, angles)))
    leg_positions.append(get_postions_from_tf(get_fk_tb2(leg.t_b0, angles)))
    leg_positions.append(get_postions_from_tf(get_fk_tb3(leg.t_b0, angles)))
    return leg_positions

def get_postions_from_tf(tf: np.matrix):
    positions = [
        tf[0,3],
        tf[1,3],
        tf[2,3],
    ]
    return positions

def get_fk_tb1(t_b0: np.matrix, angles):
    t_01 = legtf.create_T01(angles[0])
    t_b1 = np.matmul(t_b0, t_01)
    return t_b1

def get_fk_tb2(t_b0: np.matrix, angles):
    t_12 = legtf.create_T12(angles[1])
    t_b2 = np.matmul(get_fk_tb1(t_b0, angles), t_12)
    return t_b2

def get_fk_tb3(t_b0: np.matrix, angles):
    t_23 = legtf.create_T23(angles[2])
    t_b3 = np.matmul(get_fk_tb2(t_b0, angles), t_23)
    return t_b3