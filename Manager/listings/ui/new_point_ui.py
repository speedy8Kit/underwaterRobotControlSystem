from typing import List

from PyQt5.QtWidgets import QWidget

from listings.point import Point
from listings.ui.windows.new_point_widget import Ui_NewPoint


class PointWidget(QWidget):
    number = 0
    list_point_widget = None

    __max_x = 0
    __min_x = 0
    __max_y = 0
    __min_y = 0

    @staticmethod
    def setMaxMin(min_x, max_x, min_y, max_y):
        PointWidget.__min_x = min_x
        PointWidget.__max_x = max_x
        PointWidget.__min_y = min_y
        PointWidget.__max_y = max_y

    def __init__(self, point: Point, number):
        super().__init__()
        self.ui = Ui_NewPoint()
        self.ui.setupUi(self)

        self.fun = None
        self.point = point

        self.number = number
        self.ui.pointNumber.setText(f"point: {number}")

        self.ui.spin_x.setValue(point.x)
        self.ui.spin_y.setValue(point.y)
        self.ui.spin_h.setValue(point.h)
        self.ui.spin_v.setValue(point.v)

        self.ui.cb_move_mode.setCurrentIndex(self.point.move_mode)
        self.ui.cb_height_mode.setCurrentIndex(self.point.height_mode)

        self.ui.cb_move_mode.currentIndexChanged.connect(self.changePoint)
        self.ui.cb_height_mode.currentIndexChanged.connect(self.changePoint)
        self.ui.spin_h.valueChanged.connect(self.changePoint)
        self.ui.spin_x.valueChanged.connect(self.changePoint)
        self.ui.spin_y.valueChanged.connect(self.changePoint)
        self.ui.spin_v.valueChanged.connect(self.changePoint)

    def changePoint(self):
        self.point.move_mode = self.ui.cb_move_mode.currentIndex()
        self.point.height_mode = self.ui.cb_height_mode.currentIndex()

        self.point.x = self.ui.spin_x.value()
        self.point.y = self.ui.spin_y.value()
        self.point.h = self.ui.spin_h.value()
        self.point.v = self.ui.spin_v.value()

        if self.point.height_mode != Point.height_mode.above_ground:
            self.ui.spin_h.setReadOnly(True)
        else:
            self.ui.spin_h.setReadOnly(False)

        if PointWidget.update_map is not None:
            PointWidget.update_map()

    @classmethod
    def update_map_connect(cls, fun):
        cls.update_map = fun


if __name__ == "__main__":
    a: List[int] = [1, 2, 3, 4]
    print(a)
    a.append(12)
    a.remove(2)
