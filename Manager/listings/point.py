class Point(object):
    x_min = -100
    x_max = 100
    y_min = -100
    y_max = 100

    class move_mode(object):
        spline, line, to_point = 0, 1, 2

    class height_mode(object):
        constant_height, above_ground = 0, 1

    def __init__(self, x=0, y=0, move_mode=2, height_mode=1):
        self.x = x
        self.y = y
        self.h = 10

        self.v = 1
        self.alpha = 90

        self.move_mode = move_mode
        self.height_mode = height_mode

        list_point.append(self)


list_point: list[Point] = []
