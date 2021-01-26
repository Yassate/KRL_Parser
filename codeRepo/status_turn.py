from enum import IntEnum

class StatusBit(IntEnum):
    OH_AREA = 0
    A3_POSITIVE_AREA = 1
    A5_ON_PLUS = 2
    ACC_ROBOT = 3


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

    @property
    def a5_on_plus(self):
        shifted = self.val >> StatusBit.A5_ON_PLUS
        return Status.lsb(shifted)


class TurnBit(IntEnum):
    AXIS_1 = 0
    AXIS_2 = 1
    AXIS_3 = 2
    AXIS_4 = 3
    AXIS_5 = 4
    AXIS_6 = 5


class Turn:
    def __init__(self, val):
        self.val = val

    @staticmethod
    def lsb(val):
        return val & 1

    @property
    def a1_on_plus_or_zero(self):
        shifted = self.val >> TurnBit.AXIS_1
        return Status.lsb(shifted)

    @property
    def a2_on_plus_or_zero(self):
        shifted = self.val >> TurnBit.AXIS_2
        return Status.lsb(shifted)

    @property
    def a3_on_plus_or_zero(self):
        shifted = self.val >> TurnBit.AXIS_3
        return Status.lsb(shifted)

    @property
    def a4_on_plus_or_zero(self):
        shifted = self.val >> TurnBit.AXIS_4
        return Status.lsb(shifted)

    @property
    def a5_on_plus_or_zero(self):
        shifted = self.val >> TurnBit.AXIS_5
        return Status.lsb(shifted)

    @property
    def a6_on_plus_or_zero(self):
        shifted = self.val >> TurnBit.AXIS_6
        return Status.lsb(shifted)