from unittest import TestCase
from iksolver import CustomKukaIKSolver, dh_KR360_R2830
from test.test_fwd_kin import InputKinematicData
import mpmath as mp
import transformations.transformations as tf

dtor = mp.radians


class TestIK(TestCase):
    def setUp(self):
        self.ik_solver = CustomKukaIKSolver(dh_KR360_R2830)

    def solve_ik(self, test_data):

        calc_axes = self.ik_solver.perform_ik(test_data.e6pos)

        self.assertAlmostEqual(test_data.e6axis.A1, calc_axes.A1, delta=0.01)
        self.assertAlmostEqual(test_data.e6axis.A2, calc_axes.A2, delta=0.01)
        self.assertAlmostEqual(test_data.e6axis.A3, calc_axes.A3, delta=0.01)
        # self.assertAlmostEqual(test_data.e6axis.A4, calc_axes.A4, delta=0.01)
        #self.assertAlmostEqual(test_data.e6axis.A5, calc_axes.A5, delta=0.01)
        # self.assertAlmostEqual(test_data.e6axis.A6, calc_axes.A6, delta=0.01)


    def test_case1(self):
        input_data = InputKinematicData(
            robot_axes=[0, -90, 45, 0, 0, 0],
            target_xyz=[1468.736, 0.000, 3235.954],
            target_abc=[0, 45.0, 0.0])
        self.solve_ik(input_data)

    def test_case2(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 45, 0, 0, 0],
            target_xyz=[1038.553, -1038.553, 3235.954],
            target_abc=[0.0, 45.0, -45.0])
        self.solve_ik(input_data)

    def test_case3(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 0, 0],
            target_xyz=[1283.399, -1283.399, 2290.000],
            target_abc=[45.0, 90.0, 0.0])
        self.solve_ik(input_data)

    def test_case4(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 30, 0],
            target_xyz=[1255.926, -1255.926, 2145.000],
            target_abc=[0.0, 120.0, -45.0])
        self.solve_ik(input_data)

    def test_case5(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 30, 30],
            target_xyz=[1255.926, -1255.926, 2145.000],
            target_abc=[40.893, 131.410, 4.107])
        self.solve_ik(input_data)

    def test_case6(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 30, 30, 30],
            target_xyz=[1204.661, -1307.191, 2164.426],
            target_abc=[61.813, 156.453, 16.813])
        self.solve_ik(input_data)

    def test_case7(self):
        input_data = InputKinematicData(
            robot_axes=[45, -45, 120, 60, -60, 45],
            target_xyz=[1419.677, -1112.085, 852.371],
            target_abc=[-114.990, 28.605, -93.717])
        self.solve_ik(input_data)