from typing import List

import numpy as np
from matplotlib import pyplot as plt

from listings.point import Point


class PointPath(object):
    def __init__(self, x, y, h, v, is_turn_around, is_stop, constant_height: bool, is_spline = False):
        self.x = x
        self.y = y
        self.h = h
        self.v = v
        self.constant_height = constant_height
        self.is_turn_around = is_turn_around
        self.is_stop = is_stop
        self.is_spline = is_spline


class Path(object):
    oneStep = 0.05

    def __init__(self):
        self.list_point_path: List[PointPath] = [PointPath(0, 0, 0, 1, False, False, True)]
        self.list_point: List[Point] = [Point(0, 0, 0, 1, 0, 0, 0)]
        self.point_path_number = 0

    def getPoint(self):
        return self.list_point_path[self.point_path_number]

    def creationParametricSpline(self, coord_start, coord_end, tangent_start, tangent_end):
        arr = np.empty((int(1 / self.oneStep) + 1))
        i = 0
        for t in np.arange(0, 1 + self.oneStep, self.oneStep):
            arr[i] = coord_start * (2 * t ** 3 - 3 * t ** 2 + 1) + coord_end * (-2 * t ** 3 + 3 * t ** 2)
            arr[i] += tangent_start * (t ** 3 - 2 * t ** 2 + t) + tangent_end * (t ** 3 - t ** 2)
            i += 1
        return arr

    def calculateSplineTrajectory(self, number: int):
        point_start = self.list_point[number - 1]
        point_end = self.list_point[number]

        line = np.sqrt((point_start.x - point_end.x) ** 2 + (point_start.y - point_end.y) ** 2) / 3 * point_end.v
        alpha_start = point_start.alpha
        alpha_end = point_end.alpha

        tangent_start = np.array([line * np.cos(alpha_start), line * np.sin(alpha_start) * 10])
        tangent_end = np.array([line * np.cos(alpha_end), line * np.sin(alpha_end) * 10])

        xArr = self.creationParametricSpline(point_start.x, point_end.x, tangent_start[0],
                                             tangent_end[0])
        yArr = self.creationParametricSpline(point_start.y, point_end.y, tangent_start[1],
                                             tangent_end[1])
        return xArr, yArr

    def addPoint(self, point: Point):
        self.list_point.append(point)

    def generatePath(self):
        i = 0
        point_past = None
        for point in self.list_point:
            if point_past is None:
                point.alpha = 0
            else:
                print(point.move_mode)
                if point.move_mode == Point.move_mode.line:
                    point.alpha = float(np.arctan2((point.y - point_past.y), (point.x - point_past.x)))
                if point.move_mode == Point.move_mode.spline:
                    line = np.sqrt((point_past.x - point.x) ** 2 + (point_past.y - point.y) ** 2) / 3 + point.v * 3
                    print(f"line: {line}")
                    y_target = point_past.y + line * np.sin(point_past.alpha)
                    x_target = point_past.x + line * np.cos(point_past.alpha)
                    point.alpha = float(np.arctan2((point.y - y_target), (point.x - x_target)))

                    x_arr, y_arr = self.calculateSplineTrajectory(i)
                    for j in range(len(x_arr)):
                        pp = PointPath(x_arr[j], y_arr[j], point.h, point.v, False, False, point.height_mode == 0, True)
                        self.list_point_path.append(pp)
                # если необходимо двигаться по прямой то в предидущей точке нужно остановиться
                elif point.move_mode == Point.move_mode.line:
                    self.list_point_path[-1].is_stop = True

                is_turn_around = point.move_mode == Point.move_mode.line
                pp = PointPath(point.x, point.y, point.h, point.v, is_turn_around, False, point.height_mode == 0)
                self.list_point_path.append(pp)
            point_past = point
            i += 1

    def nextPoint(self):
        print("number: ", self.point_path_number)
        if self.point_path_number + 1 < len(self.list_point_path):
            self.point_path_number += 1
            return False
        else:
            print("END")
            return True

    def printPath(self):

        x = []
        y = []
        for i in self.list_point_path:
            x.append(i.x)
            y.append(i.y)
        plt.plot(x, y)
        plt.show()
