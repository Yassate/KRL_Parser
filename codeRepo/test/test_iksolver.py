import unittest
from iksolver import KukaIKSolver, dtor, rtod

def axes_deg_to_radian(axis_pos):
    new_axes = []
    for axis in axis_pos:
        new_axes.append(dtor(axis))
    return new_axes

class FK_tester(unittest.TestCase):
    def setUp(self):
        self.ik_solver = KukaIKSolver()

    def axes_deg_to_radian(axis_pos):
        new_axes = []
        for axis in axis_pos:
            new_axes.append(dtor(axis))
        return new_axes

    def test_case_FK_2(self):
        robot_axes = [0, -90, 45, 0, 0, 0]
        target_xyz = [1468.736, 0.000, 3235.954]
        target_abc = [0.0, 45.0, 0.0]
        req = self.ik_solver.performFK(axes_deg_to_radian(robot_axes))
        calc_xyz = req.get_xyz_mm_list()
        calc_abc = req.get_abc_deg_list()
        self.assertAlmostEqual(target_xyz[0], calc_xyz[0], delta=0.1)
        self.assertAlmostEqual(target_xyz[1], calc_xyz[1], delta=0.1)
        self.assertAlmostEqual(target_xyz[2], calc_xyz[2], delta=0.1)

        #self.assertAlmostEqual(target_abc[0], calc_abc[0], delta=0.1)
        #self.assertAlmostEqual(target_abc[1], calc_abc[2], delta=0.1)
        #self.assertAlmostEqual(target_abc[2], calc_abc[3], delta=0.1)

    def test_case_FK_3(self):
        robot_axes = [45, -90, 45, 0, 0, 0]
        target_xyz = [1038.553, -1038.553, 3235.954]
        target_abc = [0.0, 45.0, -45.0]
        req = self.ik_solver.performFK(axes_deg_to_radian(robot_axes))
        calc_xyz = req.get_xyz_mm_list()
        self.assertAlmostEqual(target_xyz[0], calc_xyz[0], delta=0.1)
        self.assertAlmostEqual(target_xyz[1], calc_xyz[1], delta=0.1)
        self.assertAlmostEqual(target_xyz[2], calc_xyz[2], delta=0.1)

    def test_case_FK_4(self):
        robot_axes = [45, -90, 90, 0, 0, 0]
        target_xyz = [1283.399, -1283.399, 2290.000]
        target_abc = [45.0, 90.0, 0.0]
        req = self.ik_solver.performFK(axes_deg_to_radian(robot_axes))
        calc_xyz = req.get_xyz_mm_list()
        self.assertAlmostEqual(target_xyz[0], calc_xyz[0], delta=0.1)
        self.assertAlmostEqual(target_xyz[1], calc_xyz[1], delta=0.1)
        self.assertAlmostEqual(target_xyz[2], calc_xyz[2], delta=0.1)

    def test_case_FK_5(self):
        robot_axes = [45, -90, 90, 0, 30, 0]
        target_xyz = [1255.926, -1255.926, 2145.000]
        target_abc = [0.0, 120.0, -45.0]
        req = self.ik_solver.performFK(axes_deg_to_radian(robot_axes))
        calc_xyz = req.get_xyz_mm_list()
        self.assertAlmostEqual(target_xyz[0], calc_xyz[0], delta=0.1)
        self.assertAlmostEqual(target_xyz[1], calc_xyz[1], delta=0.1)
        self.assertAlmostEqual(target_xyz[2], calc_xyz[2], delta=0.1)

    def test_case_FK_6(self):
        robot_axes = [45, -90, 90, 0, 30, 30]
        target_xyz = [1255.926, -1255.926, 2145.000]
        target_abc = [40.893, 131.410, 4.107]
        req = self.ik_solver.performFK(axes_deg_to_radian(robot_axes))
        calc_xyz = req.get_xyz_mm_list()
        self.assertAlmostEqual(target_xyz[0], calc_xyz[0], delta=0.1)
        self.assertAlmostEqual(target_xyz[1], calc_xyz[1], delta=0.1)
        self.assertAlmostEqual(target_xyz[2], calc_xyz[2], delta=0.1)

    def test_case_FK_7(self):
        robot_axes = [45, -90, 90, 30, 30, 30]
        target_xyz = [1204.661, -1307.191, 2164.426]
        target_abc = [61.813, 156.452, 16.813]
        req = self.ik_solver.performFK(axes_deg_to_radian(robot_axes))
        calc_xyz = req.get_xyz_mm_list()
        self.assertAlmostEqual(target_xyz[0], calc_xyz[0], delta=0.1)
        self.assertAlmostEqual(target_xyz[1], calc_xyz[1], delta=0.1)
        self.assertAlmostEqual(target_xyz[2], calc_xyz[2], delta=0.1)

unittest.main()