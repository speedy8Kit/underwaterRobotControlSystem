import numpy as np
from numpy import cos as c
from numpy import sin as s
from numpy.lib import math
from pyquaternion import Quaternion
import pyquaternion
# a = np.array([ [2, 1, 3], [2, 2, 3], [4, 3, 1] ])
# b = np.array([ 1, 3, 1])
# d = np.linalg.inv(a)
# total = np.dot(d, b)
# print(total)
# total = np.dot(a, total)
# print(total)

qu_x = Quaternion(axis=[1, 0, 0], angle=np.pi)  #
qu_y = Quaternion(axis=[0, 1, 0], angle=np.pi)  #
qu_z = Quaternion(axis=[0, 0, 1], angle=0)  #
# qu = qu_y * qu_x * qu_z
#
# np.set_printoptions(suppress=True)
# vec = np.array([0, 0, 1])
# print(vec)
# v_prime = qu.rotate(vec)
# print(v_prime)
# print(vec)
# print(qu_y)
# qu_y._normalise()

@staticmethod
def rotate(ang, axis, x, y, z):
    # матрица поворотов по разным осям
    vector = [[x], [y], [z]]
    if axis == 'X':
        A = np.matrix([[1, 0, 0],
                       [0, np.cos(ang), -np.sin(ang)],
                       [0, np.sin(ang), np.cos(ang)]])
    if axis == 'Y':
        A = np.matrix([[np.cos(ang), 0, np.sin(ang)],
                       [0, 1, 0],
                       [-np.sin(ang), 0, np.cos(ang)]])
    if axis == 'Z':
        A = np.matrix([[np.cos(ang), -np.sin(ang), 0],
                       [np.sin(ang), np.cos(ang), 0],
                       [0, 0, 1]])
    if axis == '-X':
        A = np.matrix([[1, 0, 0],
                       [0, np.cos(ang), np.sin(ang)],
                       [0, -np.sin(ang), np.cos(ang)]])
    if axis == '-Y':
        A = np.matrix([[np.cos(ang), 0, -np.sin(ang)],
                       [0, 1, 0],
                       [np.sin(ang), 0, np.cos(ang)]])
    if axis == '-Z':
        A = np.matrix([[np.cos(ang), np.sin(ang), 0],
                       [-np.sin(ang), np.cos(ang), 0],
                       [0, 0, 1]])
    A_rotated = np.dot(A, vector)
    A_rotated = np.round(A_rotated, 3)
    A_rotated = A_rotated.tolist()
    return (A_rotated[0][0], A_rotated[1][0], A_rotated[2][0])


@staticmethod
def Mx(a):
    return np.matrix([[1, 0, 0],
                      [0, c(a), -s(a)],
                      [0, s(a), c(a)]])


@staticmethod
def My(a):
    return np.matrix([[np.cos(a), 0, np.sin(a)],
                      [0, 1, 0],
                      [-np.sin(a), 0, np.cos(a)]])


@staticmethod
def Mz(a):
    return np.matrix([[np.cos(a), -np.sin(a), 0],
                      [np.sin(a), np.cos(a), 0],
                      [0, 0, 1]])


def mat_total(x, y, z):
    return np.array(
        [[math.cos(x) * math.cos(z) - math.sin(x) * math.sin(y) * math.sin(z),
          -math.cos(y) * math.sin(x),
          math.cos(x) * math.sin(z) + math.cos(z) * math.sin(x) * math.sin(y)],

         [math.cos(z) * math.sin(x) + math.cos(x) * math.sin(y) * math.sin(z),
          math.cos(x) * math.cos(y),
          math.sin(x) * math.sin(z) - math.cos(x) * math.cos(z) * math.sin(y)],

         [-math.cos(y) * math.sin(z), math.sin(y), math.cos(z) * math.cos(y)]])


def rotate(ang, axis, x, y, z):

# матрица поворотов по разным осям
    vector = [[x], [y], [z]]
    if axis == 'X':
        A = np.matrix([[1, 0, 0],
                       [0, np.cos(ang), -np.sin(ang)],
                       [0, np.sin(ang), np.cos(ang)]])
    if axis == 'Y':
        A = np.matrix([[np.cos(ang), 0, np.sin(ang)],
                       [0, 1, 0],
                       [-np.sin(ang), 0, np.cos(ang)]])
    if axis == 'Z':
        A = np.matrix([[np.cos(ang), -np.sin(ang), 0],
                       [np.sin(ang), np.cos(ang), 0],
                       [0, 0, 1]])
    if axis == '-X':
        A = np.matrix([[1, 0, 0],
                       [0, np.cos(ang), np.sin(ang)],
                       [0, -np.sin(ang), np.cos(ang)]])
    if axis == '-Y':
        A = np.matrix([[np.cos(ang), 0, -np.sin(ang)],
                       [0, 1, 0],
                       [np.sin(ang), 0, np.cos(ang)]])
    if axis == '-Z':
        A = np.matrix([[np.cos(ang), np.sin(ang), 0],
                       [-np.sin(ang), np.cos(ang), 0],
                       [0, 0, 1]])

    A_rotated = np.dot(A, vector)
    A_rotated = np.round(A_rotated, 3)
    A_rotated = A_rotated.tolist()
    return (A_rotated[0][0], A_rotated[1][0], A_rotated[2][0])
# matrix = np.array([[math.cos(angles[0]) * math.cos(angles[2]) - math.sin(angles[0]) * math.sin(
#     angles[1]) * math.sin(angles[2]), -math.cos(angles[1]) * math.sin(angles[0]),
#                     math.cos(angles[0]) * math.sin(angles[2]) + math.cos(angles[2]) * math.sin(
#                         angles[0]) * math.sin(angles[1])],
#                    [math.cos(angles[2]) * math.sin(angles[0]) + math.cos(angles[0]) * math.sin(
#                        angles[1]) * math.sin(angles[2]),
#                     math.cos(angles[0]) * math.cos(angles[1]),
#                     math.sin(angles[0]) * math.sin(angles[2]) - math.cos(angles[0]) * math.cos(
#                         angles[2]) * math.sin(angles[1])],
#                    [-math.cos(angles[1]) * math.sin(angles[2]), math.sin(angles[1]),
#                     math.cos(angles[2]) * math.cos(angles[1])]])
# matrix = np.dot(RECEIVE_REQ_COUNT_NAVIG.Mx(god_orientation_x),
#                 RECEIVE_REQ_COUNT_NAVIG.My(god_orientation_y),
#                 RECEIVE_REQ_COUNT_NAVIG.Mz(god_orientation_z))#RECEIVE_REQ_COUNT_NAVIG.mat_total(god_orientation_x, god_orientation_y, god_orientation_z)
# return np.matrix(
#     [[c(y) * c(z), -c(y) * s(z), s(y)],
#      [c(x) * s(z) + c(z) * s(x) * s(y), c(x) * c(z) - s(x) * s(y) * s(z), - c(y) * s(x)],
#      [s(x) * s(z) - c(x) * c(z) * s(y), c(z) * s(x) + c(x) * s(y) * s(z), c(x) * c(y)]
#      ])
# return np.array([[c(y) * c(z) - s(y) * s(x) * s(z), -c(x) * s(z), c(z) * s(y) + c(y) * s(x) * s(z)],
#                  [c(y) * s(z) + c(z) * s(x) * s(y), c(x) * c(z), s(y) * s(z) - c(y) * c(z) * s(x)],
#                  [-c(x) * s(y), s(x), c(x) * c(y)]

def quant(self, gyroData, dt):  #

    globalAngSpeed = np.array(self.k.rotate(gyroData))

    dA = globalAngSpeed * dt
    qx = Quaternion._from_axis_angle(np.array([1, 0, 0]), dA[0])
    qy = Quaternion._from_axis_angle(np.array([0, 1, 0]), dA[1])
    qz = Quaternion._from_axis_angle(np.array([0, 0, 1]), dA[2])

    q = qx * qy * qz
    q._normalise()
    self.k = self.k._rotate_quaternion(q)
    self.k._normalise()
    sortSpeed = [globalAngSpeed[2], globalAngSpeed[0], globalAngSpeed[1]]
    return sortSpeed