import time as t

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor
from PyQt5.QtWidgets import QWidget

from listings.manager import manager
from listings.point import Point, list_point
from listings.ui.ssUi_btclickevents import SSUI_BtClickEvent
from listings.ui.windows.start_simulation_window import Ui_MainWindow
from lyb.address import addr_DS
from lyb.commandList import REQ_PROCESS_PICTURE


class StartSimulationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(StartSimulationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timer = QTimer(self)
        self.painter = QPainter()

        self.ui.bt_stop.clicked.connect(SSUI_BtClickEvent.stopSimulation)
        self.ui.bt_stop.clicked.connect(self.timer.stop)
        self.ui.bt_save.clicked.connect(SSUI_BtClickEvent.save)

        self.listVelocity = []
        self.listHeight = []
        self.listAngularVelocityTrim = []
        self.listAngularVelocityHeading = []

        self.list = []
        self.list = []
        self.listTime = []

        self.map = Holst(self.ui.holst)

    def show(self) -> None:
        manager.linear_velocity = np.zeros(3)
        manager.angular_velocity = np.zeros(3)
        manager.pos = np.zeros(3)

        super(StartSimulationWindow, self).show()
        self.listVelocity.clear()
        self.listTime.clear()
        self.listAngularVelocityTrim.clear()
        self.listAngularVelocityHeading.clear()
        self.listHeight.clear()
        cod, x, y = self.map.cord_mapToHolst(list_point[0].x, list_point[0].y)
        self.map.listPath = [[x, y]]
        for i in range(500):
            self.listVelocity.append(0)
        for i in range(500):
            self.listAngularVelocityTrim.append(0)
        for i in range(500):
            self.listAngularVelocityHeading.append(0)
        for i in range(500):
            self.listHeight.append(0)
        for i in range(500):
            self.listTime.append(0)

        self.timer.timeout.connect(self.update_window)

        self.timer.start(50)

    def update_window(self):
        self.map.update()
        time = t.time() - manager.time_start_simulation
        self.ui.timer.setText(
            f"{t.gmtime(time).tm_min}:{t.gmtime(time).tm_sec}.{int((time - t.gmtime(time).tm_min * 60 - t.gmtime(time).tm_sec) * 100)}")

        self.ui.pos_x.setText(f"X: {round(manager.pos[manager.x], 2)}")
        self.ui.pos_y.setText(f"Y: {round(manager.pos[manager.y], 2)}")
        self.ui.pos_z.setText(f"Z: {round(manager.pos[manager.z], 2)}")

        self.ui.linearVelocity_x.setText(f"Vx = {round(manager.linear_velocity[manager.x], 2)}")
        self.ui.linearVelocity_y.setText(f"Vy = {round(manager.linear_velocity[manager.y], 2)}")
        self.ui.linearVelocity_z.setText(f"Vz = {round(manager.linear_velocity[manager.z], 2)}")

        self.ui.angularWelocity_z.setText(f"Wz = {round(manager.angular_velocity[manager.z], 3)}")
        self.ui.angularWelocity_y.setText(f"Wy = {round(manager.angular_velocity[manager.y], 3)}")

        self.ui.number_objects.setText(f"objects: {len(manager.list_red_objects)}")

        self.listVelocity = self.listVelocity[1:]
        self.listVelocity.append(np.linalg.norm(manager.linear_velocity))

        self.listAngularVelocityTrim = self.listAngularVelocityTrim[1:]
        self.listAngularVelocityTrim.append(manager.angular_velocity[manager.y])

        self.listAngularVelocityHeading = self.listAngularVelocityHeading[1:]
        self.listAngularVelocityHeading.append(manager.angular_velocity[manager.z])

        self.listHeight = self.listHeight[1:]
        self.listHeight.append(manager.height)

        self.listTime = self.listTime[1:]
        self.listTime.append(time)

        self.ui.g_linearVelocity.clear()
        self.ui.g_linearVelocity.plot(self.listTime, self.listVelocity)

        self.ui.g_angular_velocity_trim.clear()
        self.ui.g_angular_velocity_trim.plot(self.listTime, self.listAngularVelocityTrim)

        self.ui.g_angularVelocity_heading.clear()
        self.ui.g_angularVelocity_heading.plot(self.listTime, self.listAngularVelocityHeading)

        self.ui.g_hight.clear()
        self.ui.g_hight.plot(self.listTime, self.listHeight)

        state_cb = self.ui.cb_camera.isChecked()

        if (manager.cam_worked != state_cb) and state_cb:
            manager.sock.send_com(REQ_PROCESS_PICTURE(), addr_DS)
        manager.cam_worked = state_cb


class Holst(QWidget):
    """основной элемент окна который отображает положение всех целевых точе
    при изменении параметров с"""

    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.painter = QPainter()
        self.listPath = [[10, 10]]
        self.initUI(parent_window)

    def initUI(self, parent_window):
        self.setGeometry(parent_window.geometry())
        self.show()

    def cord_holstToMap(self, x, y):
        """переводит пиксиль холста в координату на карте"""
        width = self.size().width()
        height = self.size().height()
        try:
            coff_x = width / (-Point.x_min + Point.x_max)
            x_map = (x / coff_x) + Point.x_min
        except ZeroDivisionError:
            x_map = 0
        try:
            coff_y = height / (-Point.y_min + Point.y_max)
            y_map = ((height - y) / coff_y) + Point.y_min
        except ZeroDivisionError:
            y_map = 0
        return x_map, y_map

    def cord_mapToHolst(self, x, y):
        """переводит координату на карте в пиксиль холста
        вовращает 0, x_holst, y_holst
        при получении несуществующей координаты возвращает -1, 0, 0"""
        width = self.size().width()
        height = self.size().height()
        if x > Point.x_max or x < Point.x_min or (
                y > Point.y_max or y < Point.y_min):
            print("no gran: ", x, y)
            return -1, 0, 0
        try:
            coff_x = width / (-Point.x_min + Point.x_max)
            x_holst = ((x - Point.x_min) * coff_x)
        except ZeroDivisionError:
            x_holst = 250
        try:
            coff_y = height / (-Point.y_min + Point.y_max)
            y_holst = height - ((y - Point.y_min) * coff_y)
        except ZeroDivisionError:
            y_holst = 250

        return 0, x_holst, y_holst

    def paintEvent(self, event):
        self.painter.begin(self)

        # paint desired trajectory
        path = QPainterPath()
        p = list_point[0]
        code, x, y = self.cord_mapToHolst(p.x, p.y)
        path.moveTo(x, y)
        for p in list_point:
            code, x, y = self.cord_mapToHolst(p.x, p.y)
            path.lineTo(x, y)
            r1 = QRect(x - 5, y - 5, 10, 10)
            self.painter.drawEllipse(r1)
        self.painter.drawPath(path)

        # paint path object

        code, x, y = self.cord_mapToHolst(manager.pos[manager.x], manager.pos[manager.y])
        distance = np.sqrt((self.listPath[-1][0] - x) ** 2 + (self.listPath[-1][1] - y) ** 2)

        if code == 0 and distance > 10:
            self.listPath.append([x, y])
        for p in self.listPath:
            r = QRect(p[0] - 2, p[1] - 2, 4, 4)
            brush = QBrush()
            brush.setStyle(1)
            color = QColor('green')
            brush.setColor(color)
            self.painter.setBrush(brush)
            self.painter.drawEllipse(r)

        for obj in manager.list_red_objects:
            code, x_obj, y_obj = self.cord_mapToHolst(obj.pos[0], obj.pos[1])
            r = QRect(x_obj - 6, y_obj - 6, 12, 12)
            brush = QBrush()
            brush.setStyle(1)
            color = QColor('blue')
            brush.setColor(color)
            self.painter.setBrush(brush)
            self.painter.drawEllipse(r)

        # paint object
        if code == 0:
            r = QRect(x - 3, y - 3, 6, 6)
            brush = QBrush()
            brush.setStyle(1)
            color = QColor('red')
            brush.setColor(color)
            self.painter.setBrush(brush)
            self.painter.drawEllipse(r)

        self.painter.end()
