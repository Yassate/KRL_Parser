from unittest import TestCase
from iksolver import CustomKukaIKSolver, dh_KR360_R2830
from kuka_datatypes import E6Axis, E6Pos, Status, Turn


class InputKinematicData:
    #TODO >> Status and Turn should be not optional! Temporary solution
    def __init__(self, robot_axes, target_xyz, target_abc, S, T):
        self.e6axis = E6Axis(robot_axes)
        self.e6pos = E6Pos(target_xyz, target_abc, Status(S), Turn(T))


class TestFK(TestCase):
    def setUp(self):
        self.ik_solver = CustomKukaIKSolver(dh_KR360_R2830)

    #TODO >> load test data from external source (?) and find the way to indicate which set failed (without separate names for each case it seems impossible)
    def set_up_test_data(self):
        pass


    def solve_fk(self, test_data):
        pos_accuracy = 0.01
        rot_accuracy = 0.00001

        calc_e6pos = self.ik_solver.perform_fk(test_data.e6axis, debug_print=False)

        self.assertAlmostEqual(test_data.e6pos.x, calc_e6pos.x, delta=pos_accuracy)
        self.assertAlmostEqual(test_data.e6pos.y, calc_e6pos.y, delta=pos_accuracy)
        self.assertAlmostEqual(test_data.e6pos.z, calc_e6pos.z, delta=pos_accuracy)

        self.assertAlmostEqual(test_data.e6pos.ix, calc_e6pos.ix, delta=rot_accuracy)
        self.assertAlmostEqual(test_data.e6pos.iy, calc_e6pos.iy, delta=rot_accuracy)
        self.assertAlmostEqual(test_data.e6pos.iz, calc_e6pos.iz, delta=rot_accuracy)
        self.assertAlmostEqual(test_data.e6pos.w, calc_e6pos.w, delta=rot_accuracy)

    def test_case1(self):
        input_data = InputKinematicData(
            robot_axes=[0, -90, 45, 0, 0, 0],
            target_xyz=[1468.736, 0.000, 3235.954],
            target_abc=[0, 45.0, 0.0],
            S=18, T=2)
        self.solve_fk(input_data)

    def test_case2(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 45, 0, 0, 0],
            target_xyz=[1038.553, -1038.553, 3235.954],
            target_abc=[-45, 45.0, 0],
            S=18, T=2)
        self.solve_fk(input_data)

    def test_case3(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 0, 0],
            target_xyz=[1283.399, -1283.399, 2290.000],
            target_abc=[0, 90.0, 45.0],
            S=18, T=2)
        self.solve_fk(input_data)

    def test_case4(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 30, 0],
            target_xyz=[1255.926, -1255.926, 2145.000],
            target_abc=[-45.0, 120.0, 0],
            S=18, T=2)
        self.solve_fk(input_data)

    def test_case5(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 30, 30],
            target_xyz=[1255.926, -1255.926, 2145.000],
            target_abc=[4.107, 131.410, 40.893],
            S=18, T=2)
        self.solve_fk(input_data)

    def test_case6(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 30, 30, 30],
            target_xyz=[1204.661, -1307.191, 2164.426],
            target_abc=[16.813, 156.453, 61.813],
            S=18, T=2)
        self.solve_fk(input_data)

    def test_case7(self):
        input_data = InputKinematicData(
            robot_axes=[45, -45, 120, 60, -60, 45],
            target_xyz=[1419.677, -1112.085, 852.371],
            target_abc=[-93.717, 28.605, -114.990],
            S=22, T=18)
        self.solve_fk(input_data)