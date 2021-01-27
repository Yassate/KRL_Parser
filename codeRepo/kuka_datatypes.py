from enum import IntEnum
from mpmath import radians as dtor
from transformations import transformations as tf


class E6Axis:
    def __init__(self, axis_values=None):
        self.axis_values = axis_values
        self.A1, self.A2, self.A3, self.A4, self.A5, self.A6 = axis_values

    def get_in_radians(self):
        axes_radians = [dtor(axis) for axis in self.axis_values]
        return axes_radians


class E6Pos:
    def __init__(self, xyz, abc, S, T):
        self.x, self.y, self.z = xyz[:3]
        self.a, self.b, self.c = abc
        self.S = S
        self.T = T
        self.quat = tf.quaternion_from_euler(dtor(self.a), dtor(self.b), dtor(self.c), axes='sxyz')
    #TODO SETTERS FOR ABC TO UPDATE QUAT AND VICEVERSA

    @property
    def ix(self):
        return self.quat[0]

    @property
    def iy(self):
        return self.quat[1]

    @property
    def iz(self):
        return self.quat[2]

    @property
    def w(self):
        return self.quat[3]


class StatusBit(IntEnum):
    OH_AREA = 0
    A3_POSITIVE_AREA = 1
    A5_ON_PLUS = 2
    ACC_ROBOT = 3


class TurnBit(IntEnum):
    AXIS_1 = 0
    AXIS_2 = 1
    AXIS_3 = 2
    AXIS_4 = 3
    AXIS_5 = 4
    AXIS_6 = 5


class Status:
    def __init__(self, val):
        self.val = val

    @staticmethod
    def lsb(val):
        return val & 1

    @property
    def in_OH_area(self):
        shifted = self.val >> StatusBit.OH_AREA
        return Status.lsb(shifted)

    @property
    def a3_in_pos_area(self):
        shifted = self.val >> StatusBit.A3_POSITIVE_AREA
        return Status.lsb(shifted)

    #TODO >> KUKA docu from resources is probably wrong (in old meaning is opposite), need to be check with real robot
    @property
    def a5_on_plus(self):
        shifted = self.val >> StatusBit.A5_ON_PLUS
        return Status.lsb(shifted)


class Turn:
    def __init__(self, val):
        self.val = val

    @staticmethod
    def lsb(val):
        return val & 1

    @property
    def a1_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_1
        return Status.lsb(shifted)

    @property
    def a2_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_2
        return Status.lsb(shifted)

    @property
    def a3_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_3
        return Status.lsb(shifted)

    @property
    def a4_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_4
        return Status.lsb(shifted)

    @property
    def a5_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_5
        return Status.lsb(shifted)

    @property
    def a6_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_6
        return Status.lsb(shifted)
