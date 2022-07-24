from math import cos as c
from math import sin as s
from typing import List

import numpy as np

from lyb import address
from lyb.connector import MySocket


class Manager(object):
    x, y, z = 0, 1, 2
    sock = MySocket(address.addr_M)
    sock.sock.settimeout(6)

    def __init__(self):
        self.pos = np.zeros(3)
        self.orientation = np.zeros(3)
        self.linear_velocity = np.zeros(3)
        self.angular_velocity = np.zeros(3)
        self.height = 0
        self.clientID = None
        self.worked = False
        self.time_start_simulation = 0

        self.cam_worked = False
        self.list_red_objects: List[RedObject] = []
        self.list_connection = []
        for i in range(5):
            self.list_connection.append(True)

    def setPos(self, x: float, y: float, z: float):
        self.pos[self.x] = x
        self.pos[self.y] = y
        self.pos[self.z] = z

    def setOrientation(self, alpha: float, betta: float, gamma: float):
        self.orientation[self.x] = alpha
        self.orientation[self.y] = betta
        self.orientation[self.z] = gamma

    def setLinearVelocity(self, v_x: float, v_y: float, v_z: float):
        self.linear_velocity[self.x] = v_x
        self.linear_velocity[self.y] = v_y
        self.linear_velocity[self.z] = v_z

    def setAngularVelocity(self, w_x: float, w_y: float, w_z: float):
        self.angular_velocity[self.x] = w_x
        self.angular_velocity[self.y] = w_y
        self.angular_velocity[self.z] = w_z

    @staticmethod
    def MatrixEl(ang):
        array = np.array([[c(ang[1]) * c(ang[2]), -c(ang[1]) * s(ang[2]), s(ang[1])],
                          [c(ang[0]) * s(ang[2]) + c(ang[2]) * s(ang[0]) * s(ang[1]),
                           c(ang[0]) * c(ang[2]) - s(ang[0]) * s(ang[1]) * s(ang[2]), -c(ang[1]) * s(ang[0])],
                          [s(ang[0]) * s(ang[2]) - c(ang[0]) * c(ang[2]) * s(ang[1]),
                           c(ang[2]) * s(ang[0]) + c(ang[0]) * s(ang[1]) * s(ang[2]), c(ang[0]) * c(ang[1])]])
        return array


class RedObject(object):
    def __init__(self, x, y, mg: Manager):
        self.norm = np.sqrt(x * x + y * y)

        pos_target_loc = np.array([x * mg.height,
                                   y * mg.height,
                                   -mg.height])
        print(pos_target_loc)
        pos_target_glob = np.dot(mg.MatrixEl(mg.orientation), pos_target_loc)
        pos_target_glob[0] += mg.pos[0]
        pos_target_glob[1] += mg.pos[1]
        pos_target_glob[2] += mg.pos[2]
        self.pos = pos_target_glob


manager = Manager()
