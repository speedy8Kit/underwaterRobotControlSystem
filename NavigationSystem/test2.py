import numpy as np
from pyquaternion import Quaternion

# class Whale(object):
#     def __init__(self):
#         self.orient = Quaternion()
#
#     def pov(self, gyro_ang: np.array(3)):
#         glob_ang = np.array(self.orient.inverse.rotate(gyro_ang))
#         print(glob_ang)
#         qx = Quaternion(axis=np.array([1, 0, 0]), angle=glob_ang[0])
#         qy = Quaternion(axis=np.array([0, 1, 0]), angle=glob_ang[1])
#         qz = Quaternion(axis=np.array([0, 0, 1]), angle=glob_ang[2])
#         q = qz * qy * qx
#         self.orient.rotate(q)
#
# w = Whale()
# w.pov(np.array([0, np.pi/2, 0]))
# print(w.orient)
# w.pov(np.array([np.pi/3, 0, 0]))
# print(w.orient)
# w.pov(np.array([np.pi/3, np.pi/2, 0]))
# print(w.orient)
class Whale(object):
    def __init__(self):
        self.orient = Quaternion()     #

    # inverse

    def quant(self, gyroData):#

            globalAngSpeed = np.array(self.orient.rotate(gyroData))
            dA = globalAngSpeed
            qx = Quaternion._from_axis_angle(np.array([1,0,0]),dA[0])
            qy = Quaternion._from_axis_angle(np.array([0,1,0]),dA[1])
            qz = Quaternion._from_axis_angle(np.array([0,0,1]),dA[2])

            q = qx*qz*qy

            self.orient = q*self.orient

            sortSpeed = [globalAngSpeed[2],globalAngSpeed[0],globalAngSpeed[1]]
            return sortSpeed
w = Whale()
w.quant(np.array([0, np.pi/2, 0]))
print(w.orient)
w.quant(np.array([np.pi/3, 0, 0]))
print(w.orient)
w.quant(np.array([np.pi / 3, np.pi / 2, 0]))
print(w.orient)
# print(w.orient)
w.quant(np.array([np.pi / 4, np.pi / 6, np.pi / 3]))
# print(w.orient)

