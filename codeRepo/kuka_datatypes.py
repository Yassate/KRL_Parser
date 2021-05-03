from enum import IntEnum
from mpmath import radians as dtor
from transformations import transformations as tf


class E6Axis:
    def __init__(self, axis_values=None):
        self.axis_values = axis_values
        self.A1, self.A2, self.A3, self.A4, self.A5, self.A6 = axis_values

    def __repr__(self):
        return f"E6Axis: A1={self.A1}, A2={self.A2}, A3={self.A3}, A4={self.A4}, A5={self.A5}, A6={self.A6}"

    def get_in_radians(self):
        axes_radians = [dtor(axis) for axis in self.axis_values]
        return axes_radians


class E6Pos:
    def __init__(self):
        self.X, self.Y, self.Z = None, None, None
        self.A, self.B, self.C = None, None, None
        self.S, self.T = None, None
        self.quat = None

    def __repr__(self):
        return f"E6Pos: X={self.X}, Y={self.Y}, Z={self.Z}, A={self.A}, B={self.B}, C={self.C}, S={self.S}, T={self.T}"

    # TODO >> SETTERS FOR ABC TO UPDATE QUAT AND VICE-VERSA

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

    @classmethod
    def from_tuples(cls, xyz, abc, S, T):
        instance = cls()
        instance.X, instance.Y, instance.Z = xyz[:3]
        instance.A, instance.B, instance.C = abc
        instance.S = Status(S)
        instance.T = Turn(T)
        instance.update_quat()
        return instance

    @classmethod
    def from_krl_struct(cls, krl_struct_as_dict):
        # TODO >> exception should be raised if not all necessary elements are inside dictionary
        necessary_items = ('X', 'Y', 'Z', 'A', 'B', 'C', 'S', 'T')
        instance = cls()
        if all(item in krl_struct_as_dict.keys() for item in necessary_items):
            for key in krl_struct_as_dict:
                if hasattr(instance, key):
                    if key == 'S':
                        instance[key] = Status(krl_struct_as_dict[key])
                    elif key == 'T':
                        instance[key] = Turn(krl_struct_as_dict[key])
                    else:
                        instance[key] = krl_struct_as_dict[key]
            instance.update_quat()

        return instance

    def update_quat(self):
        if self.A is not None and self.B is not None and self.C is not None:
            self.quat = tf.quaternion_from_euler(dtor(self.A), dtor(self.B), dtor(self.C), axes='sxyz')
        else:
            self.quat = None

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

    def __repr__(self):
        return f"Status: S={self.val}"

    @staticmethod
    def lsb(val):
        return val & 1

    @property
    def in_OH_area(self):
        shifted = self.val >> StatusBit.OH_AREA
        return Status.lsb(shifted)

    @property
    def elbow_up(self):
        shifted = self.val >> StatusBit.A3_POSITIVE_AREA
        return Status.lsb(shifted)

    # TODO >> KUKA docu from resources is probably wrong (in old docu is opposite), need to be check with real robot
    @property
    def a5_on_plus(self):
        shifted = self.val >> StatusBit.A5_ON_PLUS
        return Status.lsb(shifted)


class Turn:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"Turn: T={self.val}"

    @staticmethod
    def lsb(val):
        return val & 1

    def get_turn_bit(self, axis_no):
        bit_no = TurnBit(axis_no)
        shifted = self.val >> bit_no
        return Turn.lsb(shifted)

    @property
    def get_axis_sign(self, axis_no):
        sign = 1 if self.get_turn_bit(axis_no) == 0 else -1
        return sign

    @property
    def a1_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_1
        return Turn.lsb(shifted)

    @property
    def a2_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_2
        return Turn.lsb(shifted)

    @property
    def a3_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_3
        return Turn.lsb(shifted)

    @property
    def a4_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_4
        return Turn.lsb(shifted)

    @property
    def a5_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_5
        return Turn.lsb(shifted)

    @property
    def a6_on_minus(self):
        shifted = self.val >> TurnBit.AXIS_6
        return Turn.lsb(shifted)
