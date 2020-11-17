from unittest import TestCase
from custom_iksolver import CustomKukaIKSolver, E6Axis, dh_KR360_R2830
import transformations as tf


class Test_FK(TestCase):
    def setUp(self):
        self.ik_solver = CustomKukaIKSolver(dh_KR360_R2830)

    def test_case1(self):
        test_e6axis = E6Axis([0, -90, 45, 0, 0, 0])
        target_xyz = [1468.736, 0.000, 3235.954]
        target_abc = [0.0, 45.0, 0.0]
        #TODO RADIANS!
        target_quat1 = tf.transformations.euler_matrix(target_abc[0], target_abc[1], target_abc[2], 'sxyz')
        target_quat2 = tf.transformations.quaternion_from_euler(target_abc[0], target_abc[1], target_abc[2], 'rxyz')
        target_quat3 = tf.transformations.quaternion_from_euler(target_abc[0], target_abc[1], target_abc[2], 'szyx')
        target_quat4 = tf.transformations.quaternion_from_euler(target_abc[0], target_abc[1], target_abc[2], 'rzyx')

        calc_frame = self.ik_solver.performFK(test_e6axis, debug_print=False)

        self.assertAlmostEqual(target_xyz[0]/1000, calc_frame.x, delta=0.1)
        self.assertAlmostEqual(target_xyz[1]/1000, calc_frame.y, delta=0.1)
        self.assertAlmostEqual(target_xyz[2]/1000, calc_frame.z, delta=0.1)