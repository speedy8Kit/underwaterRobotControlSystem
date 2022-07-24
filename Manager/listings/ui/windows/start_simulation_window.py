# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_simulation_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(990, 645)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(245, 160, 152)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_map = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_map.sizePolicy().hasHeightForWidth())
        self.label_map.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(12)
        self.label_map.setFont(font)
        self.label_map.setObjectName("label_map")
        self.verticalLayout_4.addWidget(self.label_map)
        self.holst = QtWidgets.QWidget(self.centralwidget)
        self.holst.setMinimumSize(QtCore.QSize(400, 400))
        self.holst.setStyleSheet("background-color: white;")
        self.holst.setObjectName("holst")
        self.verticalLayout_4.addWidget(self.holst)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pos_x = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pos_x.sizePolicy().hasHeightForWidth())
        self.pos_x.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(16)
        self.pos_x.setFont(font)
        self.pos_x.setObjectName("pos_x")
        self.verticalLayout_6.addWidget(self.pos_x)
        self.pos_y = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pos_y.sizePolicy().hasHeightForWidth())
        self.pos_y.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(16)
        self.pos_y.setFont(font)
        self.pos_y.setObjectName("pos_y")
        self.verticalLayout_6.addWidget(self.pos_y)
        self.pos_z = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pos_z.sizePolicy().hasHeightForWidth())
        self.pos_z.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(16)
        self.pos_z.setFont(font)
        self.pos_z.setObjectName("pos_z")
        self.verticalLayout_6.addWidget(self.pos_z)
        self.number_objects = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number_objects.sizePolicy().hasHeightForWidth())
        self.number_objects.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(16)
        self.number_objects.setFont(font)
        self.number_objects.setObjectName("number_objects")
        self.verticalLayout_6.addWidget(self.number_objects)
        self.horizontalLayout_11.addLayout(self.verticalLayout_6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_11)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_12.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_vectorVelocity = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_vectorVelocity.sizePolicy().hasHeightForWidth())
        self.label_vectorVelocity.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(12)
        self.label_vectorVelocity.setFont(font)
        self.label_vectorVelocity.setObjectName("label_vectorVelocity")
        self.horizontalLayout_3.addWidget(self.label_vectorVelocity)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_velocity = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_velocity.sizePolicy().hasHeightForWidth())
        self.label_velocity.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(12)
        self.label_velocity.setFont(font)
        self.label_velocity.setObjectName("label_velocity")
        self.horizontalLayout_3.addWidget(self.label_velocity)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.g_hight = PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g_hight.sizePolicy().hasHeightForWidth())
        self.g_hight.setSizePolicy(sizePolicy)
        self.g_hight.setMinimumSize(QtCore.QSize(120, 130))
        self.g_hight.setStyleSheet("background-color: white;")
        self.g_hight.setObjectName("g_hight")
        self.horizontalLayout_2.addWidget(self.g_hight)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.g_linearVelocity = PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g_linearVelocity.sizePolicy().hasHeightForWidth())
        self.g_linearVelocity.setSizePolicy(sizePolicy)
        self.g_linearVelocity.setStyleSheet("background-color: white;")
        self.g_linearVelocity.setObjectName("g_linearVelocity")
        self.horizontalLayout_2.addWidget(self.g_linearVelocity)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.linearVelocity_x = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linearVelocity_x.sizePolicy().hasHeightForWidth())
        self.linearVelocity_x.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(16)
        self.linearVelocity_x.setFont(font)
        self.linearVelocity_x.setObjectName("linearVelocity_x")
        self.horizontalLayout.addWidget(self.linearVelocity_x)
        self.linearVelocity_y = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linearVelocity_y.sizePolicy().hasHeightForWidth())
        self.linearVelocity_y.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(16)
        self.linearVelocity_y.setFont(font)
        self.linearVelocity_y.setObjectName("linearVelocity_y")
        self.horizontalLayout.addWidget(self.linearVelocity_y)
        self.linearVelocity_z = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linearVelocity_z.sizePolicy().hasHeightForWidth())
        self.linearVelocity_z.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(16)
        self.linearVelocity_z.setFont(font)
        self.linearVelocity_z.setObjectName("linearVelocity_z")
        self.horizontalLayout.addWidget(self.linearVelocity_z)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lable_angulaVelocity_y = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lable_angulaVelocity_y.sizePolicy().hasHeightForWidth())
        self.lable_angulaVelocity_y.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(12)
        self.lable_angulaVelocity_y.setFont(font)
        self.lable_angulaVelocity_y.setObjectName("lable_angulaVelocity_y")
        self.horizontalLayout_5.addWidget(self.lable_angulaVelocity_y)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.lable_angularVelocity_z = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lable_angularVelocity_z.sizePolicy().hasHeightForWidth())
        self.lable_angularVelocity_z.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(12)
        self.lable_angularVelocity_z.setFont(font)
        self.lable_angularVelocity_z.setObjectName("lable_angularVelocity_z")
        self.horizontalLayout_5.addWidget(self.lable_angularVelocity_z)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.g_angularVelocity_heading = PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g_angularVelocity_heading.sizePolicy().hasHeightForWidth())
        self.g_angularVelocity_heading.setSizePolicy(sizePolicy)
        self.g_angularVelocity_heading.setMinimumSize(QtCore.QSize(120, 130))
        self.g_angularVelocity_heading.setStyleSheet("background-color: white;")
        self.g_angularVelocity_heading.setObjectName("g_angularVelocity_heading")
        self.horizontalLayout_6.addWidget(self.g_angularVelocity_heading)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_6.addWidget(self.line_2)
        self.g_angular_velocity_trim = PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g_angular_velocity_trim.sizePolicy().hasHeightForWidth())
        self.g_angular_velocity_trim.setSizePolicy(sizePolicy)
        self.g_angular_velocity_trim.setMinimumSize(QtCore.QSize(120, 130))
        self.g_angular_velocity_trim.setStyleSheet("background-color: white;")
        self.g_angular_velocity_trim.setObjectName("g_angular_velocity_trim")
        self.horizontalLayout_6.addWidget(self.g_angular_velocity_trim)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.angularWelocity_y = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.angularWelocity_y.sizePolicy().hasHeightForWidth())
        self.angularWelocity_y.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(16)
        self.angularWelocity_y.setFont(font)
        self.angularWelocity_y.setObjectName("angularWelocity_y")
        self.horizontalLayout_7.addWidget(self.angularWelocity_y)
        self.angularWelocity_z = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.angularWelocity_z.sizePolicy().hasHeightForWidth())
        self.angularWelocity_z.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(16)
        self.angularWelocity_z.setFont(font)
        self.angularWelocity_z.setObjectName("angularWelocity_z")
        self.horizontalLayout_7.addWidget(self.angularWelocity_z)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_12.addLayout(self.verticalLayout_3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.cb_camera = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_camera.sizePolicy().hasHeightForWidth())
        self.cb_camera.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(14)
        self.cb_camera.setFont(font)
        self.cb_camera.setIconSize(QtCore.QSize(40, 40))
        self.cb_camera.setCheckable(True)
        self.cb_camera.setTristate(False)
        self.cb_camera.setObjectName("cb_camera")
        self.verticalLayout_5.addWidget(self.cb_camera)
        self.horizontalLayout_8.addLayout(self.verticalLayout_5)
        self.timer = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(26)
        self.timer.setFont(font)
        self.timer.setObjectName("timer")
        self.horizontalLayout_8.addWidget(self.timer)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.bt_save = QtWidgets.QPushButton(self.centralwidget)
        self.bt_save.setMinimumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(14)
        font.setItalic(False)
        self.bt_save.setFont(font)
        self.bt_save.setStyleSheet("QPushButton {\n"
"    background-color:rgb(41, 3, 79);\n"
"    border: 2px solid rgb(255, 90, 129);\n"
"    border-radius: 20px;\n"
"    color: white;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color:rgb(22, 1, 43);\n"
"}")
        self.bt_save.setObjectName("bt_save")
        self.horizontalLayout_8.addWidget(self.bt_save)
        self.bt_stop = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.bt_stop.sizePolicy().hasHeightForWidth())
        self.bt_stop.setSizePolicy(sizePolicy)
        self.bt_stop.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(14)
        self.bt_stop.setFont(font)
        self.bt_stop.setStyleSheet("QPushButton {\n"
"    background-color:rgb(41, 3, 79);\n"
"    border: 2px solid rgb(255, 90, 129);\n"
"    border-radius: 20px;\n"
"    color: white;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color:rgb(22, 1, 43);\n"
"}")
        self.bt_stop.setCheckable(False)
        self.bt_stop.setAutoRepeat(False)
        self.bt_stop.setAutoExclusive(False)
        self.bt_stop.setObjectName("bt_stop")
        self.horizontalLayout_8.addWidget(self.bt_stop)
        self.verticalLayout_8.addLayout(self.horizontalLayout_8)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_map.setText(_translate("MainWindow", "map"))
        self.pos_x.setText(_translate("MainWindow", "X = 0.00"))
        self.pos_y.setText(_translate("MainWindow", "Y = 0.00"))
        self.pos_z.setText(_translate("MainWindow", "Z = 0.00"))
        self.number_objects.setText(_translate("MainWindow", "objecrts: 0"))
        self.label_vectorVelocity.setText(_translate("MainWindow", "height"))
        self.label_velocity.setText(_translate("MainWindow", "velocity"))
        self.linearVelocity_x.setText(_translate("MainWindow", "Vx = 0.00"))
        self.linearVelocity_y.setText(_translate("MainWindow", "Vy = 0.00"))
        self.linearVelocity_z.setText(_translate("MainWindow", "Vz = 0.00"))
        self.lable_angulaVelocity_y.setText(_translate("MainWindow", "angular velocity heading"))
        self.lable_angularVelocity_z.setText(_translate("MainWindow", "angular velocity trim"))
        self.angularWelocity_y.setText(_translate("MainWindow", "W heading = 0.00"))
        self.angularWelocity_z.setText(_translate("MainWindow", "W trim = 0.00"))
        self.cb_camera.setText(_translate("MainWindow", "camera"))
        self.timer.setText(_translate("MainWindow", "00:00"))
        self.bt_save.setText(_translate("MainWindow", "Save"))
        self.bt_stop.setText(_translate("MainWindow", "Stop"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
