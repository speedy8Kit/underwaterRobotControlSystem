class Point(object):
    def __init__(self, x: float, y: float, h: float,
                 v: float, move_mode: int, height_mode: int, number: int):
        self.x = x
        self.y = y
        self.h = h

        self.v = v
        self.move_mode = move_mode
        self.height_mode = height_mode
        self.number = number
        self.alpha = None

    class move_mode(object):
        spline, line, to_point = 0, 1, 2

    class height_mode(object):
        constant_height, above_ground = 0, 1

    class pos(object):
        x, y, z = 0, 1, 2
