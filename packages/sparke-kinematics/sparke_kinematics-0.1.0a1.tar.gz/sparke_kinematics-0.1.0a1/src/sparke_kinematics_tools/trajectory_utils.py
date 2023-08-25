from PyQt5.QtCore import QModelIndex

def get_velocity(model):
    lin_vel_index = get_lin_vel_index(model)
    ang_vel_index = get_ang_vel_index(model)
    vel = []
    for i in range(3):
        val_index = model.index(i, 1, lin_vel_index)
        vel.append(float(val_index.data()))

    for j in range(3):
        val_index = model.index(j, 1, ang_vel_index)
        vel.append(float(val_index.data()))
    return vel

def set_velocity(model, cmd_vel):
    lin_vel_index = get_lin_vel_index(model)
    ang_vel_index = get_ang_vel_index(model)
    vel = []
    for i in range(3):
        val_index = model.index(i, 1, lin_vel_index)
        val_model = val_index.model()
        val_model.setData(val_index, float(cmd_vel[i]))
        val_index = model.index(i, 1, ang_vel_index)
        val_model = val_index.model()
        val_model.setData(val_index, float(cmd_vel[i+3]))

def get_points(model):
    points = []
    for i in range(1, 13):
        position = []
        point_index = get_point_index(model, i)
        for j in range(3):
            val_index = model.index(j, 1, point_index)
            position.append(float(val_index.data()))
        points.append(position)
    return points

def set_points(model, points):
    for i in range(1, 13):
        position = points[i-1]
        point_index = get_point_index(model, i)
        for j in range(3):
            val_index = model.index(j, 1, point_index)
            val_model = val_index.model()
            val_model.setData(val_index, float(position[j]))

def get_vel_index(model):
    return model.index(0,0, QModelIndex())

def get_lin_vel_index(model):
    vel_index = get_vel_index(model)
    return model.index(0,0, vel_index)

def get_ang_vel_index(model):
    vel_index = get_vel_index(model)
    return model.index(1,0, vel_index)

def get_point_index(model, point_num):
    return model.index(point_num, 0, QModelIndex())