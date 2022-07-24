from PyQt5 import QtWidgets

import socket
import sim
import time

from threading import Thread
from termcolor import colored
from PyQt5.QtWidgets import QMessageBox

import lyb.address as address

import lyb.commandList as comList
from listings.manager import manager, Manager
import listings.manager as mg


class MUI_BtClickEvents(object):
    th = None

    main_window: QtWidgets.QMainWindow = None
    start_simulation_window: QtWidgets.QMainWindow = None
    set_mission_window: QtWidgets.QMainWindow = None

    @staticmethod
    def exitWindow():
        sim.simxStopSimulation(manager.clientID, sim.simx_opmode_oneshot)
        manager.worked = False
        exit()

    @staticmethod
    def connect():
        """после нажатия кнопки connect, необходимо проверить соединения всех модулей
        для этого отпровляются команды потключения и ожидаются ответы"""
        if manager.sock is not None:
            sim.simxFinish(0)

        mg.manager = Manager()

        print("connect...")

        manager.clientID = sim.simxStart('127.0.0.1', address.sim_port_M, True, True, 2000, 5)
        # очистка лишних сообщений из буфера
        try:
            manager.sock.sock.settimeout(0)
            while True:
                com_, addr_ = manager.sock.recv_com()
                print(com_.name)
        except:
            manager.sock.sock.settimeout(6)

        if manager.clientID != -1:
            print(colored('successful: ', 'green'), manager.clientID)
        else:
            print(colored('fail', 'red'))

        ok = True
        """указывает на коректность подключения всех модулей"""

        def connectModule(address_module: address.Address):
            manager.sock.send_com(comList.CMD_CONNECT(), address_module)
            print("send com")
            com_, addr_ = manager.sock.recv_com()
            com_.run(addr_, manager.sock)
            while com_.key != comList.EVENT_CONNECT.key:
                com_, addr_ = manager.sock.recv_com()
                com_.run(addr_, manager.sock)

        MUI_BtClickEvents.main_window.ui.label_mission.setText("No mission")

        # подключенея системы управления движителями
        try:
            connectModule(address.addr_CS)
            connectModule(address.addr_NS)
            connectModule(address.addr_DS)
        except socket.timeout:
            MUI_BtClickEvents.main_window.ui.label_connect.setText("not all included")
            ok = False
        except ConnectionResetError:
            MUI_BtClickEvents.main_window.ui.label_connect.setText("not all included")
            ok = False
        for include in manager.list_connection:
            if not include:
                MUI_BtClickEvents.main_window.ui.label_connect.setText(f"does not see sim")
                ok = False
        if ok:
            MUI_BtClickEvents.main_window.ui.label_connect.setText("ok")

    @staticmethod
    def startSimulation():
        """при нажатии кнопки начала симуляции, необходимо убедиться в
        наличии миссии и соединения всех модулей.
        После всего этого открыть второй поток приема/отправки сообщений
        и отправить первые запросы на все модули"""
        manager.list_red_objects.clear()
        if MUI_BtClickEvents.main_window.ui.label_connect.text() != "ok":
            MUI_BtClickEvents.error_no_connect()
        elif MUI_BtClickEvents.main_window.ui.label_mission.text() == "No mission":
            MUI_BtClickEvents.error_no_mission()
        else:
            MUI_BtClickEvents.start_simulation_window.show()
            MUI_BtClickEvents.main_window.close()
            manager.time_start_simulation = time.time()

            # первые запросы для запуска алгоритма
            manager.sock.send_com(comList.REQ_COUNT_PROPELLER_CONTROL_SIGNAL(), address.addr_CS)
            manager.sock.send_com(comList.REQ_COUNT_NAVIG(), address.addr_NS)
            manager.worked = True

            def start():
                sim.simxStartSimulation(manager.clientID, sim.simx_opmode_oneshot_wait)
                while manager.worked:
                    try:
                        com, addr = manager.sock.recv_com()
                    except socket.timeout:
                        continue
                    com.run(addr, manager.sock)

            MUI_BtClickEvents.th = Thread(target=start)
            MUI_BtClickEvents.th.start()

    @staticmethod
    def setMission():
        manager.sock.send_com(comList.CMD_CONNECT(), address.addr_CS)
        if MUI_BtClickEvents.main_window.ui.label_connect.text() != "ok":
            MUI_BtClickEvents.error_no_connect()
        else:
            MUI_BtClickEvents.set_mission_window.show()
            MUI_BtClickEvents.main_window.close()

    @staticmethod
    def error_no_connect():
        err = QMessageBox()
        err.setWindowTitle("error connect")
        err.setText("the connection string must be 'ok' ")
        err.setIcon(QMessageBox.Warning)
        err.setStandardButtons(QMessageBox.Ok)
        err.exec_()

    @staticmethod
    def error_no_mission():
        err = QMessageBox()
        err.setWindowTitle("error mission")
        err.setText("the connection string should contain the name of the mission file ")
        err.setIcon(QMessageBox.Warning)
        err.setStandardButtons(QMessageBox.Ok)
        err.exec_()

    @staticmethod
    def error():
        err = QMessageBox()
        err.setWindowTitle("БОЛЬШАЯ ОШИБКА")
        err.setText("кнопка пока не добавлена")
        err.setIcon(QMessageBox.Critical)
        err.setStandardButtons(QMessageBox.Ok)
        err.exec_()
