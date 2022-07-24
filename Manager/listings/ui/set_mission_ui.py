import button as button
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget

from listings.point import Point, list_point
from listings.ui.new_point_ui import PointWidget
from listings.ui.smUi_btclickevent import SMUI_BtClickEvent
from listings.ui.windows.set_mission_window import Ui_SetMissionWindow


class SetMissionWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SetMissionWindow()
        self.ui.setupUi(self)

        PointWidget.list_point_widget = self.ui.list_points
        self.ui.list_points.itemClicked.connect(SMUI_BtClickEvent.rowChanged)
        self.map = Holst(self.ui.holst,
                         x_min=self.ui.spin_x_min,
                         x_max=self.ui.spin_x_max,
                         y_min=self.ui.spin_y_min,
                         y_max=self.ui.spin_y_max)

        self.ui.bt_add.clicked.connect(SMUI_BtClickEvent.addPoint)
        self.ui.bt_remove.clicked.connect(SMUI_BtClickEvent.removePoint)
        self.ui.bt_save.clicked.connect(SMUI_BtClickEvent.save)
        self.ui.bt_cancel.clicked.connect(SMUI_BtClickEvent.cancel)
        self.ui.bt_scan.clicked.connect(SMUI_BtClickEvent.scan)
        self.ui.bt_scan.clicked.connect(self.map.update)

        self.update_window()
        SMUI_BtClickEvent.addPoint()

    def update_window(self):
        """по нпжатию любой кнопки в окне должна обнавляться карта
         со всеми точками на ней"""
        self.ui.bt_add.clicked.connect(self.map.update)
        self.ui.bt_remove.clicked.connect(self.map.update)

        self.ui.spin_x_min.valueChanged.connect(self.map.update)
        self.ui.spin_y_min.valueChanged.connect(self.map.update)
        self.ui.spin_x_max.valueChanged.connect(self.map.update)
        self.ui.spin_y_max.valueChanged.connect(self.map.update)

        PointWidget.update_map_connect(self.map.update)


class Holst(QWidget):
    """основной элемент окна который отображает положение всех целевых точе
    при изменении параметров с"""

    def __init__(self, parent_window,
                 x_min: QtWidgets.QDoubleSpinBox, x_max: QtWidgets.QDoubleSpinBox,
                 y_min: QtWidgets.QDoubleSpinBox, y_max: QtWidgets.QDoubleSpinBox):
        super().__init__(parent_window)
        self.spin_x_min: QtWidgets.QDoubleSpinBox = x_min
        self.spin_x_max: QtWidgets.QDoubleSpinBox = x_max
        self.spin_y_min: QtWidgets.QDoubleSpinBox = y_min
        self.spin_y_max: QtWidgets.QDoubleSpinBox = y_max

        self.painter = QPainter()

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

    def mousePressEvent(self, event: {button}):
        """при нажатии на холст необходимо добавить новую точку с координтами нажатия"""
        if event.button() == Qt.LeftButton:
            x, y = self.cord_holstToMap(event.pos().x(), event.pos().y())
            SMUI_BtClickEvent.addPoint(x, y)
            self.update()

    def paintEvent(self, event):
        Point.x_min = self.spin_x_min.value()
        Point.x_max = self.spin_x_max.value()
        Point.y_min = self.spin_y_min.value()
        Point.y_max = self.spin_y_max.value()

        path = QPainterPath()
        self.painter.begin(self)
        p = list_point[0]
        code, x, y = self.cord_mapToHolst(p.x, p.y)
        path.moveTo(x, y)
        for p in list_point:
            code, x, y = self.cord_mapToHolst(p.x, p.y)
            path.lineTo(x, y)
            r1 = QRect(x - 5, y - 5, 10, 10)
            self.painter.drawEllipse(r1)
        self.painter.drawPath(path)
        self.painter.end()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = SetMissionWindow()
    MainWindow.show()
    sys.exit(app.exec_())
