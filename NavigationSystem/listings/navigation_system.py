import time

import numpy as np

from lyb import address
from lyb.connector import MySocket


class NavigationSystem(object):
    x, y, z = 0, 1, 2
    socket = MySocket(address.addr_NS)

    def __init__(self):
        self.pos = np.zeros(3)
        self.orientation = np.zeros(3)
        self.linear_velocity = np.zeros(3)
        self.angular_velocity = np.zeros(3)
        self.clientID = None

        self.time_last_step = time.time()


navigation_system = NavigationSystem()
