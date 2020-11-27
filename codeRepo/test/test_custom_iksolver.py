from unittest import TestCase
from custom_iksolver import CustomKukaIKSolver, E6Axis, E6Pos, dh_KR360_R2830
import mpmath as mp
import transformations.transformations as tf

dtor = mp.radians


class InputKinematicData:
    def __init__(self, robot_axes, target_xyz, target_abc):
        self.e6axis = E6Axis(robot_axes)
        self.e6pos = E6Pos(target_xyz, target_abc)
        self.target_xyz = target_xyz
        self.target_abc = target_abc


class TestFK(TestCase):
    def setUp(self):
        self.ik_solver = CustomKukaIKSolver(dh_KR360_R2830)

    #TODO >> load test data from external source (?) and find the way to indicate which set failed (without separate names for each case it seems impossible)
    def set_up_test_data(self):
        pass

    def assert_pos(self, target_xyz_m, calc_frame, accuracy):
        self.assertAlmostEqual(target_xyz_m[0], calc_frame.x, delta=accuracy)
        self.assertAlmostEqual(target_xyz_m[1], calc_frame.y, delta=accuracy)
        self.assertAlmostEqual(target_xyz_m[2], calc_frame.z, delta=accuracy)

    def assert_rot(self, target_quat, calc_frame, accuracy):
        self.assertAlmostEqual(target_quat[0], calc_frame.orientation[0], delta=accuracy)
        self.assertAlmostEqual(target_quat[1], calc_frame.orientation[1], delta=accuracy)
        self.assertAlmostEqual(target_quat[2], calc_frame.orientation[2], delta=accuracy)
        self.assertAlmostEqual(target_quat[3], calc_frame.orientation[3], delta=accuracy)

    def solve_FK(self, test_data):
        target_xyz_m = [val / 1000 for val in test_data.target_xyz]
        target_abc_rad = [dtor(angle) for angle in test_data.target_abc]
        target_quat = tf.quaternion_from_euler(target_abc_rad[0], target_abc_rad[1], target_abc_rad[2], axes='sxyz')

        calc_frame = self.ik_solver.performFK(test_data.e6axis, debug_print=False)

        self.assert_pos(target_xyz_m, calc_frame, accuracy=0.01)
        self.assert_rot(target_quat, calc_frame, accuracy=0.00001)

    def test_case_1(self):
        input_data = InputKinematicData(
            robot_axes=[0, -90, 45, 0, 0, 0],
            target_xyz=[1468.736, 0.000, 3235.954],
            target_abc=[0, 45.0, 0.0])
        self.solve_FK(input_data)

    def test_case2(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 45, 0, 0, 0],
            target_xyz=[1038.553, -1038.553, 3235.954],
            target_abc=[0.0, 45.0, -45.0])
        self.solve_FK(input_data)

    def test_case3(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 0, 0],
            target_xyz=[1283.399, -1283.399, 2290.000],
            target_abc=[45.0, 90.0, 0.0])
        self.solve_FK(input_data)

    def test_case4(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 30, 0],
            target_xyz=[1255.926, -1255.926, 2145.000],
            target_abc=[0.0, 120.0, -45.0])
        self.solve_FK(input_data)

    def test_case5(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 30, 30],
            target_xyz=[1255.926, -1255.926, 2145.000],
            target_abc=[40.893, 131.410, 4.107])
        self.solve_FK(input_data)

    def test_case6(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 30, 30, 30],
            target_xyz=[1204.661, -1307.191, 2164.426],
            target_abc=[61.813, 156.453, 16.813])
        self.solve_FK(input_data)

    def test_case7(self):
        input_data = InputKinematicData(
            robot_axes=[45, -45, 120, 60, -60, 45],
            target_xyz=[1419.677, -1112.085, 852.371],
            target_abc=[-114.990, 28.605, -93.717])
        self.solve_FK(input_data)