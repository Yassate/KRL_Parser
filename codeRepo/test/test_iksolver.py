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


class TestIK(TestCase):
    def setUp(self):
        self.ik_solver = CustomKukaIKSolver(dh_KR360_R2830)

    def solve_IK(self, testcase_data):
        target_xyz_m = [val / 1000 for val in testcase_data.target_xyz]
        target_abc_rad = [dtor(angle) for angle in testcase_data.target_abc]
        target_quat = tf.quaternion_from_euler(target_abc_rad[0], target_abc_rad[1], target_abc_rad[2], axes='sxyz')



        calc_frame = self.ik_solver.performIK(testcase_data.test_e6axis, debug_print=False)

        self.assert_pos(target_xyz_m, calc_frame, accuracy=0.01)
        self.assert_rot(target_quat, calc_frame, accuracy=0.00001)
