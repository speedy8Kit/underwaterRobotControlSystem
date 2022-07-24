import time

import numpy as np

import listings.regulator as reg
import sim
from listings.path import Path, PointPath
from lyb import address
from lyb.connector import MySocket


class ControlSystem(object):
    r, l, t, b = 0, 1, 2, 3
    x, y, z = 0, 1, 2
    socket = MySocket(address.addr_CS)

    def __init__(self):

        self.path = Path()

        self.pos = np.zeros(3)
        self.orientation = np.zeros(3)
        self.linear_velocity = np.zeros(3)

        self.height_b = 0
        self.height_f = 0

        self.cons_z = 0

        self.clientID = 0

        self.signals = [1.0, 1, 1, 1]
        """значения сигналов подаваемых на вентили"""

        self.__time = 0
        self.__time_step = 0

        self.limiter = reg.Limiter(10000, 100)
        self.pid_velocity = reg.PID_Regulator(cof_p=12, cof_i=10, cof_d=0.0002)
        self.pid_distance = reg.PID_Regulator(cof_p=10, cof_i=1, cof_d=0.0005)
        self.pid_heading = reg.PID_Regulator(cof_p=14, cof_i=0, cof_d=0.001)
        """курс"""
        self.pid_trim = reg.PID_Regulator(cof_p=14, cof_i=3, cof_d=0.0003)
        """диффепент"""
        self.trust_distance = 0.5
        """радиус окружности заход в которую прираввнивается к приходу в точку"""

        self.sensor_right = None
        self.sensor_mid = None
        self.sensor_left = None

        self.sensor_height_f = None
        self.sensor_height_b = None

        self.god_mod = True

    @staticmethod
    def M_z_t(ang):
        return np.array([[np.cos(ang), np.sin(ang), 0],
                         [-np.sin(ang), np.cos(ang), 0],
                         [0, 0, 1]])

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

    def count_signals(self):
        point: PointPath = self.path.getPoint()

        _, state, point_detect_height_f, _, _ = \
            sim.simxReadProximitySensor(self.clientID, self.sensor_height_f, sim.simx_opmode_buffer)
        if state:
            self.height_f = np.linalg.norm(point_detect_height_f)
        else:
            self.height_f = point.h
        _, state, point_detect_height_b, _, _ = \
            sim.simxReadProximitySensor(self.clientID, self.sensor_height_b, sim.simx_opmode_buffer)
        if state:
            self.height_b = np.linalg.norm(point_detect_height_b)
        else:
            self.height_b = point.h

        ############### преобразовать в связанную СК ###############
        pos = np.array([point.x - self.pos[0], point.y - self.pos[1], 0])
        pos = np.dot(self.M_z_t(self.orientation[2]), pos)
        x = pos[0]
        y = pos[1]

        braking_distances = point.v
        self.__time_step = time.time() - self.__time
        self.__time = time.time()
        if self.__time_step < 0.001:
            self.__time_step = 0.001

        norm_target = np.linalg.norm(np.array([x, y]))

        norm_velocity = np.linalg.norm(self.linear_velocity)

        # при приближении к целевой точке,
        # точка должна двигаться от робота
        if point.is_stop:
            if norm_target < self.trust_distance:
                self.path.nextPoint()
        else:
            if norm_target < braking_distances * 1.1:
                self.path.nextPoint()

        if point.is_turn_around and np.abs(np.arctan2(y, x)) > 0.1:
            # если нелбходимо развернуться и угол ненулевой
            value_heading = self.pid_heading.regulate(5 * np.arctan2(y, x),
                                                      self.__time_step)
            sig_r = value_heading
            sig_l = -value_heading
            sig_t = 0
            sig_b = 0
        else:
            point.is_turn_around = False
            if norm_target > self.trust_distance:
                if norm_target > braking_distances:
                    # классическое движение регулируется по ошибке скорости

                    desired_velocity = point.v

                    value = self.pid_velocity.regulate(desired_velocity - norm_velocity,
                                                       self.__time_step)
                    sig_r = value
                    sig_l = value
                    sig_t = value
                    sig_b = value
                else:
                    # движение торможения регулируется по ошибке положения другим ПИДом
                    # приемущество в "обнулении" интегральной составляющей

                    # когда цель находится сбоку от кита для возможности повернуть двигаться назад
                    if x < 0.2:
                        value = self.pid_distance.regulate(-norm_target, self.__time_step)
                    else:
                        value = self.pid_distance.regulate(norm_target - norm_velocity, self.__time_step)

                    sig_r = value
                    sig_l = value
                    sig_t = value
                    sig_b = value

                # регулировани курса и крена происходит всегда одинаково пока кит не приблизится на расстояние доверия
                value_heading = self.pid_heading.regulate(np.arctan2(y, x), self.__time_step)

                if point.constant_height:
                    err = (self.cons_z - self.pos[2]) / 3
                else:
                    # print(self.height_b, self.height_f)
                    self.cons_z = self.pos[2]

                    err_height = (point.h - (self.height_b + self.height_f) / 2) * point.v
                    if err_height < -2.1:
                        err_height = -2.1
                    if err_height > 2.6:
                        err_height = 2.6
                    err_delta = (self.height_b - self.height_f) * 3
                    # print("delta: ", err_delta)
                    # print("height: ", err_height)
                    err = err_delta + err_height
                # print(err)
                value_trim = self.pid_trim.regulate(err, self.__time_step)
                sig_r += value_heading
                sig_l -= value_heading
                sig_t -= value_trim
                sig_b += value_trim
            else:
                # после приближения к цели на расстояние доверия обнуление интегральных составляющих всех ПИДов
                # это необходимо чтобы перемещения от точки к точки с остановкой были независимы друг от друга
                self.pid_velocity.zeroing()
                self.pid_trim.zeroing()
                self.pid_distance.zeroing()
                self.pid_heading.zeroing()

                if x > 0.08:
                    # при возможности максимально приблизится к цели двигаясь с нуливым курсом и диффернтом
                    # воспользуемся ей, чтобы при минимальных смещения от цели не начинать движение по новой
                    value = self.pid_distance.regulate(norm_target - norm_velocity, self.__time_step)
                    sig_r = value
                    sig_l = value
                    sig_t = value
                    sig_b = value
                else:
                    sig_r = 0
                    sig_l = 0
                    sig_t = 0
                    sig_b = 0

        sig_r, sig_l, sig_t, sig_b, state = self.passObstacle(sig_r, sig_l, sig_t, sig_b)
        if point.is_spline and state:
            self.path.nextPoint()
        sig_r = self.limiter.limitationSignal(sig_r, self.__time_step)
        sig_l = self.limiter.limitationSignal(sig_l, self.__time_step)
        sig_t = self.limiter.limitationSignal(sig_t, self.__time_step)
        sig_b = self.limiter.limitationSignal(sig_b, self.__time_step)
        self.signals[self.r] = sig_r
        self.signals[self.l] = sig_l
        self.signals[self.t] = sig_t
        self.signals[self.b] = sig_b

    def passObstacle(self, sig_r, sig_l, sig_t, sig_b):
        max_length = 6
        cod, state_r, point_r, _, _ = sim.simxReadProximitySensor(self.clientID, self.sensor_right,
                                                                  sim.simx_opmode_buffer)

        cod, state_l, point_l, _, _ = sim.simxReadProximitySensor(self.clientID, self.sensor_left,
                                                                  sim.simx_opmode_buffer)
        cod, state_m, point_m, _, _ = sim.simxReadProximitySensor(self.clientID, self.sensor_mid,
                                                                  sim.simx_opmode_buffer)
        if state_r:
            len_r = np.linalg.norm(point_r)
        else:
            len_r = max_length
        if state_l:
            len_l = np.linalg.norm(point_l)
        else:
            len_l = max_length
        if state_m:
            len_m = np.linalg.norm(point_m)
        else:
            len_m = max_length

        r = (sig_r + 10 * ((1 / len_r) * max_length) - 10 * ((1 / len_l) * max_length)) / (max_length / len_m)**5
        l = (sig_l + 10 * ((1 / len_l) * max_length) - 10 * ((1 / len_r) * max_length))
        t = sig_t / (max_length / len_m)
        b = sig_b / (max_length / len_m)

        return r, l, t, b, (state_r or state_l or state_m)



propeller_controller = ControlSystem()
