import time
from math import cos as c
from math import sin as s

import numpy as np

import listings.navigation_system as ns
import lyb.address as address
import lyb.commandList as comList
import lyb.connector as connector
import sim


class Filter(object):
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.sig_filt_prev = [0, 0]

    def filt(self, sig):
        val = ((1 - self.alpha + self.beta) * sig) + (self.alpha * self.sig_filt_prev[0]) - (
                self.beta * self.sig_filt_prev[1])

        self.sig_filt_prev.append(val)
        self.sig_filt_prev = self.sig_filt_prev[1:]
        return val


class RECEIVE_REQ_COUNT_NAVIG(comList.REQ_COUNT_NAVIG):
    add_commands = True
    filter_x = Filter(0.97, 0.01)
    filter_y = Filter(0.97, 0.01)
    filter_z = Filter(0.97, 0.01)

    linear_velocity_last = np.array([0, 0, 0])
    matrixPov = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def run(self, senders: address.Address, socket: connector.MySocket):
        time_now = time.time()
        delta_time = time_now - ns.navigation_system.time_last_step
        if delta_time > 1:
            print("big delta_time")
            delta_time = 10 ** -7
        ns.navigation_system.time_last_step = time_now

        buf = sim.simx_opmode_buffer
        ID = ns.navigation_system.clientID
        _, velocity_x = sim.simxGetFloatSignal(ID, 'velocity_x', buf)
        _, velocity_y = sim.simxGetFloatSignal(ID, 'velocity_y', buf)
        _, velocity_z = sim.simxGetFloatSignal(ID, 'velocity_z', buf)

        _, angular_velocity_x = sim.simxGetFloatSignal(ID, 'angular_velocity_x', buf)
        _, angular_velocity_y = sim.simxGetFloatSignal(ID, 'angular_velocity_y', buf)
        _, angular_velocity_z = sim.simxGetFloatSignal(ID, 'angular_velocity_z', buf)

        _, god_orientation_x = sim.simxGetFloatSignal(ID, 'god_whale_orientation_x', buf)
        _, god_orientation_y = sim.simxGetFloatSignal(ID, 'god_whale_orientation_y', buf)
        _, god_orientation_z = sim.simxGetFloatSignal(ID, 'god_whale_orientation_z', buf)
        #
        # _, god_linear_velocity_x = sim.simxGetFloatSignal(ID, 'god_linear_velocity_x', buf)
        # _, god_linear_velocity_y = sim.simxGetFloatSignal(ID, 'god_linear_velocity_y', buf)
        # _, god_linear_velocity_z = sim.simxGetFloatSignal(ID, 'god_linear_velocity_z', buf)

        god_orientation = np.array([god_orientation_x, god_orientation_y, god_orientation_z])

        linear_velocity_own = np.array([velocity_x, velocity_y, velocity_z])
        linear_velocity_own[0] = self.filter_x.filt(linear_velocity_own[0])
        linear_velocity_own[1] = self.filter_y.filt(linear_velocity_own[1])
        linear_velocity_own[2] = self.filter_z.filt(linear_velocity_own[2])

        angular_velocity_own = np.array([angular_velocity_x, angular_velocity_y, angular_velocity_z])
        delta_angular = angular_velocity_own * delta_time

        matrix_changes = RECEIVE_REQ_COUNT_NAVIG.MatrixEl(delta_angular)  ##№№№№№№№№№№№№№№№№№№№
        RECEIVE_REQ_COUNT_NAVIG.matrixPov = np.dot(RECEIVE_REQ_COUNT_NAVIG.matrixPov, matrix_changes)  ##№№№№№№№№№№

        linear_velocity = np.dot(RECEIVE_REQ_COUNT_NAVIG.MatrixEl(god_orientation), linear_velocity_own)
        # linear_velocity = np.dot(RECEIVE_REQ_COUNT_NAVIG.matrixPov, linear_velocity_own)

        ns.navigation_system.pos += (linear_velocity + self.linear_velocity_last) / 2 * delta_time

        self.linear_velocity_last = linear_velocity
        ns.navigation_system.orientation += angular_velocity_own * delta_time

        # отправляет полученные навигационные значения на менеджера
        socket.send_com(comList.MSG_NAVIG(*ns.navigation_system.pos,
                                          *god_orientation,
                                          *linear_velocity_own,
                                          *angular_velocity_own),
                        address.addr_M)

    @staticmethod
    def MatrixEl(ang):
        array = np.array([[c(ang[1]) * c(ang[2]), -c(ang[1]) * s(ang[2]), s(ang[1])],
                          [c(ang[0]) * s(ang[2]) + c(ang[2]) * s(ang[0]) * s(ang[1]),
                           c(ang[0]) * c(ang[2]) - s(ang[0]) * s(ang[1]) * s(ang[2]), -c(ang[1]) * s(ang[0])],
                          [s(ang[0]) * s(ang[2]) - c(ang[0]) * c(ang[2]) * s(ang[1]),
                           c(ang[2]) * s(ang[0]) + c(ang[0]) * s(ang[1]) * s(ang[2]), c(ang[0]) * c(ang[1])]])
        return array


class RECEIVE_CMD_CONNECT(comList.CMD_CONNECT):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        if ns.navigation_system.clientID is not None:
            sim.simxFinish(0)
        ns.navigation_system = ns.NavigationSystem()

        ns.navigation_system.socket = socket
        ns.navigation_system.clientID = sim.simxStart('127.0.0.1', address.sim_port_NS, True, True, 2000, 5)
        print(1)
        if ns.navigation_system.clientID == -1:
            print("connect fail")
            socket.send_com(comList.EVENT_CONNECT(False), address.addr_M)
        else:
            socket.send_com(comList.EVENT_CONNECT(True), address.addr_M)

            ID = ns.navigation_system.clientID
            stream = sim.simx_opmode_streaming
            _, ns.navigation_system.linear_velocity[ns.NavigationSystem.x] = sim.simxGetFloatSignal(ID, 'velocity_x',
                                                                                                    stream)
            _, ns.navigation_system.linear_velocity[ns.NavigationSystem.y] = sim.simxGetFloatSignal(ID, 'velocity_y',
                                                                                                    stream)
            _, ns.navigation_system.linear_velocity[ns.NavigationSystem.z] = sim.simxGetFloatSignal(ID, 'velocity_z',
                                                                                                    stream)

            _, angular_velocity_x = sim.simxGetFloatSignal(ID, 'angular_velocity_x', stream)
            _, angular_velocity_y = sim.simxGetFloatSignal(ID, 'angular_velocity_y', stream)
            _, angular_velocity_z = sim.simxGetFloatSignal(ID, 'angular_velocity_z', stream)

            # _, ns.navigation_system.linear_velocity[ns.NavigationSystem.x] = sim.simxGetFloatSignal(
            #     ID, 'god_linear_velocity_x', stream)
            # _, ns.navigation_system.linear_velocity[ns.NavigationSystem.y] = sim.simxGetFloatSignal(
            #     ID, 'god_linear_velocity_y', stream)
            # _, ns.navigation_system.linear_velocity[ns.NavigationSystem.z] = sim.simxGetFloatSignal(
            #     ID, 'god_linear_velocity_z', stream)

            _, ns.navigation_system.orientation[ns.NavigationSystem.x] = sim.simxGetFloatSignal(ID,
                                                                                                'god_whale_orientation_x',
                                                                                                stream)
            _, ns.navigation_system.orientation[ns.NavigationSystem.y] = sim.simxGetFloatSignal(ID,
                                                                                                'god_whale_orientation_y',
                                                                                                stream)
            _, ns.navigation_system.orientation[ns.NavigationSystem.z] = sim.simxGetFloatSignal(ID,
                                                                                                'god_whale_orientation_z',
                                                                                                stream)

            print("connect ok")


def receive():
    RECEIVE_REQ_COUNT_NAVIG()
    RECEIVE_CMD_CONNECT()
