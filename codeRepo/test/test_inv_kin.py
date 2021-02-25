import unittest
from iksolver import CustomKukaIKSolver, dh_KR360_R2830
from test.test_fwd_kin import InputKinematicData


class TestIK(unittest.TestCase):
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

    # TODO >> A2, A3 in quadrant III should be also tested, reachability avalaible on KUKA KR120 R2500 Pro
    def test_A2A3_elbow_up_and_in_quadrant_IV_WCP_in_quadrant_IV(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, 3.0, 62.0, 5.0, 50.0, 30.0],
            target_xyz=[2059.763983, -19.3609071, -237.726233],
            target_abc=[36.3241115, -157.337019, -11.2437047],
            S=18, T=0)
        self.solve_ik(input_data)

    def test_A2A3_elbow_down_and_in_quadrant_IV_WCP_in_quadrant_IV(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, 20.0, -25.0, 5.0, 50.0, 30.0],
            target_xyz=[2952.490195, -19.3604456, 430.7211721],
            target_abc=[41.56864940, 145.4685071, 31.26293290],
            S=16, T=4)
        self.solve_ik(input_data)

    def test_A2A3_elbow_down_and_in_quadrant_IV_WCP_in_quadrant_I(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, 20.0, -90.0, 5.0, 50.0, 30.0],
            target_xyz=[2395.559263, -19.3606717, 1644.261998],
            target_abc=[-65.1385245, 52.95478560, -55.2899104],
            S=16, T=4)
        self.solve_ik(input_data)

    def test_A2A3_elbow_up_and_in_quadrant_I_WCP_in_quadrant_IV(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, -27.0, 62.0, 5.0, 50.0, 30.0],
            target_xyz=[2492.15954,  -19.3607102, 714.0156365],
            target_abc=[33.16221580, 177.8193610, 5.997348200],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_A2A3_elbow_up_and_in_quadrant_I_WCP_in_quadrant_I(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, -58.0, 62.0, 5.0, 50.0, 30.0],
            target_xyz=[2378.085131, -19.3607347, 1787.334949],
            target_abc=[38.08749070, 152.3895679, 24.53577020],
            S=18, T=2)
        self.solve_ik(input_data)

    def test_A2A3_elbow_down_and_in_quadrant_I_WCP_in_quadrant_I(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, -24.0, -45.0, 5.0, 50.0, 30.0],
            target_xyz=[2379.694422, -19.3607339, 2605.688204],
            target_abc=[-66.3579830, 53.36636810, -56.8135700],
            S=16, T=6)
        self.solve_ik(input_data)

    def test_A2A3_elbow_up_and_in_quadrant_II_WCP_in_quadrant_I(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, -107.0, 82.0, 5.0, -45.0, 30.0],
            target_xyz=[1171.648017, 17.87279090, 2943.336919],
            target_abc=[-34.7683285, 14.74968830, -14.2597367],
            S=22, T=18)
        self.solve_ik(input_data)

    def test_A2A3_elbow_down_and_in_quadrant_I_WCP_in_quadrant_II(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, -70.245, -60.143, 169.518, -19.802, -136.586],
            target_xyz=[213.9328963, 17.87245040, 3355.270074],
            target_abc=[-35.7312686, -19.2098284, 9.080257400],
            S=20, T=54)
        self.solve_ik(input_data)

    def test_A2A3_elbow_up_and_in_quadrant_II_WCP_in_quadrant_II(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, -120.00, 13.000, 5.0, -45.0, 30.0],
            target_xyz=[-652.3629424, 17.87200000, 3303.521190],
            target_abc=[-56.6678734, -48.6966242, 44.56188900],
            S=23, T=18)
        self.solve_ik(input_data)

    def test_A2A3_elbow_down_and_in_quadrant_II_WCP_in_quadrant_II(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, -105.833, -19.135, 7.766, -27.135, 26.620],
            target_xyz=[-652.3629424, 17.87200000, 3303.521190],
            target_abc=[-56.6678734, -48.6966242, 44.56188900],
            S=21, T=22)
        self.solve_ik(input_data)

    def test_A2A3_elbow_down_and_in_quadrant_II_WCP_in_quadrant_I(self):
        input_data = InputKinematicData(
            robot_axes=[0.0, -129.000, 143.000, -8.0, 118.0, 30.0],
            target_xyz=[469.6913171, 35.63617090, 1540.857654],
            target_abc=[39.83456740, -149.460794, -31.4434278],
            S=18, T=10)
        self.solve_ik(input_data)