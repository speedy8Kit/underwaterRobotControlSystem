import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from listings.ui.mUi_btclickevents import MUI_BtClickEvents
from listings.ui.set_mission_ui import SetMissionWindow
from listings.ui.smUi_btclickevent import SMUI_BtClickEvent
from listings.ui.ssUi_btclickevents import SSUI_BtClickEvent
from listings.ui.start_simulation_ui import StartSimulationWindow
from listings.ui.windows.main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupUi_py()

        self.ui.bt_connect.clicked.connect(MUI_BtClickEvents.connect)
        self.ui.bt_mission.clicked.connect(MUI_BtClickEvents.setMission)

        self.ui.bt_start.clicked.connect(MUI_BtClickEvents.startSimulation)

        self.ui.bt_exit.clicked.connect(MUI_BtClickEvents.exitWindow)

    def setupUi_py(self):
        self.setWindowTitle("Whale")
        self.setWindowIcon(
            QIcon("C:/MyFolder/MyWorks/university/IUS_Uhimec_Karmanova/Kyrsach/programm/prog/Manager/res/icon.jpg")
        )


class PlotMainWindow(object):
    app = QtWidgets.QApplication(sys.argv)

    def __init__(self):
        self.main_window = MainWindow()
        self.start_window = StartSimulationWindow()
        self.set_mission_window = SetMissionWindow()

    def plotMainWindow(self):
        MUI_BtClickEvents.main_window = self.main_window
        MUI_BtClickEvents.start_simulation_window = self.start_window
        MUI_BtClickEvents.set_mission_window = self.set_mission_window

        SMUI_BtClickEvent.main_window = self.main_window
        SMUI_BtClickEvent.set_mission_window = self.set_mission_window

        SSUI_BtClickEvent.start_simulation_window = self.start_window
        SSUI_BtClickEvent.main_window = self.main_window

        self.main_window.show()
        sys.exit(self.app.exec_())
