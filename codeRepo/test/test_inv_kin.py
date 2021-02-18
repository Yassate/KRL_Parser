from unittest import TestCase
from iksolver import CustomKukaIKSolver, dh_KR360_R2830
from test.test_fwd_kin import InputKinematicData


class TestIK(TestCase):
    def setUp(self):
        self.ik_solver = CustomKukaIKSolver(dh_KR360_R2830)

    def solve_ik(self, test_data):

        calc_axes = self.ik_solver.perform_ik(input_e6pos=test_data.e6pos, prev_e6_axis=test_data.e6axis)


        self.assertAlmostEqual(test_data.e6axis.A1, calc_axes.A1, delta=0.01)
        self.assertAlmostEqual(test_data.e6axis.A2, calc_axes.A2, delta=0.01)
        self.assertAlmostEqual(test_data.e6axis.A3, calc_axes.A3, delta=0.01)
        self.assertAlmostEqual(test_data.e6axis.A4, calc_axes.A4, delta=0.01)
        self.assertAlmostEqual(test_data.e6axis.A5, calc_axes.A5, delta=0.01)
        self.assertAlmostEqual(test_data.e6axis.A6, calc_axes.A6, delta=0.01)

    def test_case1(self):
        input_data = InputKinematicData(
            robot_axes=[0, -90, 45, 0, 0, 0],
            target_xyz=[1468.736, 0.000, 3235.954],
            target_abc=[0, 45.0, 0.0],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_case2(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 45, 0, 0, 0],
            target_xyz=[1038.553, -1038.553, 3235.954],
            target_abc=[-45.0, 45.0, 0.0],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_case3(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 0, 0],
            target_xyz=[1283.399, -1283.399, 2290.000],
            target_abc=[0, 90.0, 45.0],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_case4(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 30, 0],
            target_xyz=[1255.926, -1255.926, 2145.000],
            target_abc=[-45, 120.0, 0],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_case5(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 0, 30, 30],
            target_xyz=[1255.926, -1255.926, 2145.000],
            target_abc=[4.107, 131.410, 40.893],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_case6(self):
        input_data = InputKinematicData(
            robot_axes=[45, -90, 90, 30, 30, 30],
            target_xyz=[1204.661, -1307.191, 2164.426],
            target_abc=[16.813, 156.453, 61.813],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_case7(self):
        input_data = InputKinematicData(
            robot_axes=[45, -45, 120, 60, -60, 45],
            target_xyz=[1419.677, -1112.085, 852.371],
            target_abc=[-93.717, 28.605, -114.990],
            S=22, T=18)
        self.solve_ik(input_data)

    def test_A1_0deg(self):
        input_data = InputKinematicData(
            robot_axes=[0, -117, 71, 2.5, 90, 30],
            target_xyz=[869.8150261, -12.6490703, 2701.174038],
            target_abc=[38.980989, 142.5682496, 29.0770778],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_A1_min35deg(self):
        input_data = InputKinematicData(
            robot_axes=[-35.0, -117.0, 71.0, 2.5, 90.0, 30.0],
            target_xyz=[719.7725193, 488.5480227, 2701.168885],
            target_abc=[73.9807575, 142.5685834, 29.0767376],
            S=18, T=3)
        self.solve_ik(input_data)

    def test_A1_plus35deg(self):
        input_data = InputKinematicData(
            robot_axes=[35.0, -117.0, 71.0, 2.5, 90.0, 30.0],
            target_xyz=[705.2621841, -509.2709511, 2701.168885],
            target_abc=[3.9808151, 142.5685834, 29.0767376],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_A1_minus126deg(self):
        input_data = InputKinematicData(
            robot_axes=[-126.0, -117.0, 71.0, 2.5, 90.0, 30.0],
            target_xyz=[-501.0260858, 711.1237675, 2701.189585],
            target_abc=[-15.0185889, 37.4324718, -150.9221871],
            S=18, T=3)
        self.solve_ik(input_data)

    def test_A1_plus126deg(self):
        input_data = InputKinematicData(
            robot_axes=[126.0, -117.0, 71.0, 2.5, 90.0, 30.0],
            target_xyz=[-521.4991595, -696.2615365, 2701.170063],
            target_abc=[-87.0191562, 142.5684501, 29.0768708],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_A1_plus3deg(self):
        input_data = InputKinematicData(
            robot_axes=[3.0, -117.0, 71.0, 2.5, 90.0, 30.0],
            target_xyz=[867.9684837, -58.1553497, 2701.168675],
            target_abc=[35.9807193, 142.5686257, 29.0766891],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_A1_minus177deg_OH(self):
        input_data = InputKinematicData(
            robot_axes=[-177.0, -104.626, -42.706, -177.431, 76.681, 29.408],
            target_xyz=[867.9684837, -58.1553497, 2701.168675],
            target_abc=[35.9807193, 142.5686257, 29.0766891],
            S=17, T=15)
        self.solve_ik(input_data)

    def test_A1_plus183deg_OH(self):
        input_data = InputKinematicData(
            robot_axes=[183.0, -104.626, -42.706, -177.431, 76.681, 29.408],
            target_xyz=[867.9684837, -58.1553497, 2701.168675],
            target_abc=[35.9807193, 142.5686257, 29.0766891],
            S=17, T=14)
        self.solve_ik(input_data)

    def test_A1_plus3deg_OH(self):
        input_data = InputKinematicData(
            robot_axes=[3.0, -128.0, 38.0, 2.5, 42.0, 30.0],
            target_xyz=[-51.8683036, -5.7574473, 3309.938091],
            target_abc=[-43.3435536, 35.414067, -24.2372062],
            S=19, T=2)
        self.solve_ik(input_data)

    def test_A1_minus177deg(self):
        input_data = InputKinematicData(
            robot_axes=[-177, -121.183, 52.171, -178.122, 62.973, 31.005],
            target_xyz=[-51.8683036, -5.7574473, 3309.938091],
            target_abc=[-43.3435536, 35.414067, -24.2372062],
            S=18, T=11)
        self.solve_ik(input_data)

    def test_A1_plus183deg(self):
        input_data = InputKinematicData(
            robot_axes=[183, -121.183, 52.171, -178.122, 62.973, 31.005],
            target_xyz=[-51.8683036, -5.7574473, 3309.938091],
            target_abc=[-43.3435536, 35.414067, -24.2372062],
            S=18, T=10)
        self.solve_ik(input_data)