import numpy as np
import transformations.transformations as tf
import matplotlib.pyplot as plt
import pytransform3d.rotations as py3drot

from enum import IntEnum
from mpmath import mp, sqrt
from mpmath import radians as dtor
from mpmath import degrees as rtod
from sympy import symbols, pi, cos, sin, Matrix
from kuka_datatypes import E6Axis, E6Pos
from math import copysign


def createMatrix(alpha, a, q, d):
    mat = Matrix([[cos(q), -sin(q) * cos(alpha),    sin(q) * sin(alpha), a * cos(q)],
                  [sin(q),  cos(q) * cos(alpha),   -cos(q) * sin(alpha), a * sin(q)],
                  [0,       sin(alpha),             cos(alpha),          d],
                  [0, 0, 0, 1]])

    return mat


# # Define DH param symbols
d0, d1, d2, d3, d4, d5, d6, d7 = symbols('d0:8')  # link_offset_i
a0, a1, a2, a3, a4, a5, a6, a7 = symbols('a0:8')  # link_length_i
alpha0, alpha1, alpha2, alpha3, alpha4, alpha5, alpha6, alpha7 = symbols('alpha0:8')  # link_twist_i
alphaX = symbols('alphaX')
aX = symbols('aX')
dX = symbols('dX')
qX = symbols('qX')

# # Joint angle symbols (q0 is additional because of Z direction (to the ground) of first joint rotation axis)
q0, q1, q2, q3, q4, q5, q6, q7 = symbols('q0:8')  # theta_i
qi0, qi1, qi2, qi3, qi4, qi5, qi6, qi7 = symbols('qi0:8')

dh_KR360_R2830 = {alpha0: pi,    a0: 0,      d0: 0,       q0: 0,
                  alpha1: pi/2,  a1: 0.50,   d1: -1.045,  q1: qi1,
                  alpha2: 0,     a2: 1.30,   d2: 0,       q2: qi2-pi/2,
                  alpha3: -pi/2, a3: 0.055,  d3: 0,       q3: qi3+pi,
                  alpha4: pi/2,  a4: 0,      d4: -1.025,  q4: qi4,
                  alpha5: -pi/2, a5: 0,      d5: 0,       q5: qi5,
                  alpha6: pi,    a6: 0,      d6: -0.29,   q6: qi6}

dh_KR360_R2830 = {alpha0: pi,    a0: 0,      d0: 0,       q0: 0,
                  alpha1: pi/2,  a1: 0.50,   d1: -1.045,  q1: qi1,
                  alpha2: 0,     a2: 1.30,   d2: 0,       q2: qi2-pi/2,
                  alpha3: -pi/2, a3: 0.055,  d3: 0,       q3: qi3+pi,
                  alphaX: 0,     aX: 0,      dX: -1.025,  qX: 0,
                  alpha4: pi/2,  a4: 0,      d4: 0,       q4: qi4,
                  alpha5: -pi/2, a5: 0,      d5: 0,       q5: qi5,
                  alpha6: pi,    a6: 0,      d6: -0.29,   q6: qi6}

dh_KR360_R2830 = {alpha0: pi,    a0: 0,      d0: 0,       q0: 0,
                  alpha1: pi/2,  a1: 0.50,   d1: -1.045,  q1: qi1,
                  alpha2: 0,     a2: 1.30,   d2: 0,       q2: qi2-pi/2,
                  alpha3: -pi/2, a3: 0.055,  d3: 0,       q3: qi3+pi,
                  alphaX: 0,     aX: 0,      dX: -1.025,  qX: 0,
                  alpha4: pi/2,  a4: 0,      d4: 0,       q4: qi4,
                  alpha5: -pi/2, a5: 0,      d5: 0,       q5: qi5,
                  alpha6: pi,    a6: 0,      d6: 0,       q6: qi6,
                  alpha7: 0,     a7: 0,      d7: 0.29,    q7: 0}


class Coord(IntEnum):
    X = 0
    Y = 1
    Z = 2


class CustomKukaIKSolver:

    def __init__(self, dh_params):

        self.dh_params = dh_params
        self.origin = Matrix([[0], [0], [0], [1]])

        self.A0_1 = createMatrix(alpha0, a0, q0, d0).subs(self.dh_params)
        self.A1_2 = createMatrix(alpha1, a1, q1, d1).subs(self.dh_params)
        self.A2_3 = createMatrix(alpha2, a2, q2, d2).subs(self.dh_params)
        self.A3_X = createMatrix(alpha3, a3, q3, d3).subs(self.dh_params)
        self.AX_4 = createMatrix(alphaX, aX, qX, dX).subs(self.dh_params)
        self.A4_5 = createMatrix(alpha4, a4, q4, d4).subs(self.dh_params)
        self.A5_6 = createMatrix(alpha5, a5, q5, d5).subs(self.dh_params)
        self.A6_F = createMatrix(alpha6, a6, q6, d6).subs(self.dh_params)
        self.F_FF = createMatrix(alpha7, a7, q7, d7).subs(self.dh_params)

        self.T0_1 = self.A0_1
        self.T0_2 = self.T0_1 * self.A1_2
        self.T0_3 = self.T0_2 * self.A2_3
        self.T0_X = self.T0_3 * self.A3_X
        self.T0_4 = self.T0_X * self.AX_4
        self.T0_5 = self.T0_4 * self.A4_5
        self.T0_6 = self.T0_5 * self.A5_6
        self.T0_F = self.T0_6 * self.A6_F
        self.T0_FF = self.T0_F * self.F_FF

        self.axis3d = py3drot.plot_basis(R=np.eye(3), ax_s=4)


    def test_plot(self):
        pos = np.array([1.0, 1.0, 1.0])
        pos2 = np.array([1.0, 1.0, 3.0])
        rot = py3drot.matrix_from_euler_xyz([np.pi/2, 0, 0])
        self.add_frame(rot, pos)
        self.add_frame(rot, pos2)

        plt.show()

    def add_frame(self, rot, pos):
        py3drot.plot_basis(self.axis3d, R=rot, p=pos)

    @staticmethod
    def calc_hor_dist(pos1, pos2=Matrix([0, 0, 0, 0])):
        return mp.sqrt((pos2[Coord.X] - pos1[Coord.X])**2 + (pos2[Coord.Y] - pos1[Coord.Y])**2)

    @staticmethod
    def calc_vert_dist(pos1, pos2=Matrix([0, 0, 0, 0])):
        return abs(pos2[Coord.Z] - pos1[Coord.Z])

    def calc_dist(self, pos1, pos2=Matrix([0, 0, 0, 0])):
        hor_dist = self.calc_hor_dist(pos1, pos2)
        vert_dist = self.calc_vert_dist(pos1, pos2)
        return mp.sqrt(hor_dist ** 2 + vert_dist ** 2)

    @staticmethod
    def calc_A1(pos_wcp, S, T, l_limit, h_limit):
        A1 = mp.atan2(-pos_wcp[Coord.Y], pos_wcp[Coord.X])
        A1 = round(A1, 5)
        const_pi = round(mp.pi, 5)

        if S.in_OH_area:
            A1 = A1 + copysign(const_pi, -A1)

        sign_nok = (A1 < 0) != T.a1_on_minus

        if sign_nok:
            A1 = A1 + copysign(2*const_pi, -A1)

        if dtor(l_limit) <= A1 <= dtor(h_limit):
            return A1
        else:
            # TODO >> In this case error should be raised or return value should be intepreted in main calculation
            #raiseError
            return None

    def calc_A2(self, pos_wcp, S, T, l_limit, h_limit, axis1):
        # TODO >> Limits not taken into consideration, tests don't cover all possibilities
        pos_wcp_rot_back = Matrix([0, 0, 0, 1])
        pos_wcp_rot_back[Coord.X] = pos_wcp[Coord.X] * mp.cos(axis1) - pos_wcp[Coord.Y] * mp.sin(axis1)
        pos_wcp_rot_back[Coord.Y] = pos_wcp[Coord.X] * mp.sin(axis1) + pos_wcp[Coord.Y] * mp.cos(axis1)
        pos_wcp_rot_back[Coord.Z] = pos_wcp[Coord.Z]

        pos_a2_rot_back = Matrix([abs(dh_KR360_R2830[a1]), 0, abs(dh_KR360_R2830[d1]), 0])
        pos_a2_ref_wcp_rot_back = pos_wcp_rot_back - pos_a2_rot_back

        len_link2 = abs(self.dh_params[a2])
        len_link3 = abs(self.dh_params[dX])
        dist_a3_a4 = abs(self.dh_params[a3])
        dist_a3_wcp = mp.sqrt(len_link3 ** 2 + dist_a3_a4 ** 2)
        dist_a2_wcp = self.calc_dist(pos_a2_rot_back, pos_wcp_rot_back)

        beta1 = mp.atan2(pos_a2_ref_wcp_rot_back[Coord.Z], pos_a2_ref_wcp_rot_back[Coord.X])
        beta2 = mp.acos((dist_a2_wcp ** 2 + len_link2 ** 2 - dist_a3_wcp ** 2) / (2 * dist_a2_wcp * len_link2))

        if not S.elbow_up:
            beta2 = -beta2

        A2 = beta1 + beta2

        sign_nok = (A2 < 0) != T.a2_on_minus

        return -A2 if sign_nok else A2

    def calc_A3(self, pos_wcp, S, T, l_limit, h_limit, axis1):
        dist_a3_a4 = abs(self.dh_params[a3])
        len_link2 = abs(self.dh_params[a2])
        len_link3 = abs(self.dh_params[dX])
        dist_a3_wcp = mp.sqrt(len_link3 ** 2 + dist_a3_a4 ** 2)
        pos_A2_rot_axis = self.T0_2.evalf(subs={qi1: axis1})[0:4, 3:4]
        dist_a2_wcp = self.calc_dist(pos_A2_rot_axis, pos_wcp)

        gamma1 = mp.atan(dist_a3_a4 / len_link3)
        gamma2 = mp.acos((dist_a3_wcp ** 2 + len_link2 ** 2 - dist_a2_wcp ** 2) / (2 * dist_a3_wcp * len_link2))

        if not S.elbow_up:
            gamma1 = -gamma1

        A3 = np.pi - (gamma1 + gamma2)

        sign_nok = (A3 < 0) != T.a3_on_minus
        return -A3 if sign_nok else A3

    @staticmethod
    def calc_A5(R_3_6, T, l_limit, h_limit):
        A5 = mp.acos(-R_3_6[2, 2])
        sign_nok = (A5 < 0) != T.a5_on_minus

        return -A5 if sign_nok else A5

    @staticmethod
    def calc_A4(R_3_6, T, l_limit, h_limit, axis5, prev_axis4=0):
        if round(axis5, 5) == 0:
            return dtor(prev_axis4)

        cos_A4 = R_3_6[0, 2] / mp.sin(axis5)
        sin_A4 = R_3_6[1, 2] / mp.sin(axis5)
        A4 = mp.atan2(sin_A4, cos_A4) % (2*mp.pi)
        sign_nok = (A4 < 0) != T.a4_on_minus

        if sign_nok or A4 < dtor(l_limit) or A4 > dtor(h_limit):
            A4 = A4 + copysign(2*mp.pi, -A4)

        return A4

    @staticmethod
    def calc_A6(R_3_6, T, l_limit, h_limit, axis5, prev_axis6):
        if round(axis5, 5) == 0:
            return dtor(prev_axis6)

        cos_A6 = R_3_6[2, 0] / mp.sin(axis5)
        sin_A6 = R_3_6[2, 1] / mp.sin(axis5)
        A6 = mp.atan2(sin_A6, cos_A6) % (2*mp.pi)
        sign_nok = (A6 < 0) != T.a6_on_minus

        if sign_nok or A6 < dtor(l_limit) or A6 > dtor(h_limit):
            A6 = A6 + copysign(2*mp.pi, -A6)

        return A6

    def perform_ik(self, input_e6pos, prev_e6_axis):

        input_xyz = [input_e6pos.X / 1000, input_e6pos.Y / 1000, input_e6pos.Z / 1000]
        input_abc = [dtor(input_e6pos.A), dtor(input_e6pos.B), dtor(input_e6pos.C)]

        # abc and pos from point data
        matrix_xyz_abc = tf.euler_matrix(input_abc[0], input_abc[1], input_abc[2], axes='rzyx')
        matrix_xyz_abc[0, 3] = input_xyz[0]
        matrix_xyz_abc[1, 3] = input_xyz[1]
        matrix_xyz_abc[2, 3] = input_xyz[2]

        dist_to_wcp = Matrix([[0], [0], [-abs(self.dh_params[d7])], [1]])
        pos_wcp = matrix_xyz_abc * dist_to_wcp

        # TODO >> limits should be taken from robot geometry configuration
        axis1 = self.calc_A1(pos_wcp, S=input_e6pos.S, T=input_e6pos.T, l_limit=-185, h_limit=185)
        axis2 = self.calc_A2(pos_wcp, S=input_e6pos.S, T=input_e6pos.T, l_limit=-120, h_limit=20, axis1=axis1)
        axis3 = self.calc_A3(pos_wcp, S=input_e6pos.S, T=input_e6pos.T, l_limit=-100, h_limit=144, axis1=axis1)

        A1_to_A3 = {qi1: axis1, qi2: dtor(90) + axis2, qi3: -dtor(90) + axis3}

        R_0_3 = self.T0_4.evalf(subs=A1_to_A3)[0:3, 0:3]
        R_0_6 = matrix_xyz_abc[0:3, 0:3]
        R_3_6 = R_0_3.inv() * R_0_6

        axis5 = self.calc_A5(R_3_6=R_3_6, T=input_e6pos.T, l_limit=-120, h_limit=120)

        axis4 = self.calc_A4(R_3_6, input_e6pos.T, l_limit=-350, h_limit=350, axis5=axis5, prev_axis4=prev_e6_axis.A4)
        axis6 = self.calc_A6(R_3_6, input_e6pos.T, l_limit=-350, h_limit=350, axis5=axis5, prev_axis6=prev_e6_axis.A6)

        axis1_deg = rtod(axis1)
        axis2_deg = rtod(axis2)
        axis3_deg = rtod(axis3)
        axis4_deg = rtod(axis4)
        axis5_deg = rtod(axis5)
        axis6_deg = rtod(axis6)


        axes = [rtod(rad) for rad in [axis1, axis2, axis3, axis4, axis5, axis6]]
        return E6Axis(axes)

    def perform_fk(self, input_e6_axis, debug_print=False):
        e6_axis_radians = input_e6_axis.get_in_radians()

        axes_radian = {qi1: e6_axis_radians[0],
                       qi2: dtor(90) + e6_axis_radians[1],
                       qi3: -dtor(90) + e6_axis_radians[2],
                       qi4: e6_axis_radians[3],
                       qi5: e6_axis_radians[4],
                       qi6: e6_axis_radians[5]}

        test = self.A4_5 * self.A5_6 * self.A6_F


        transf_T01_evaluated = self.T0_1.evalf(subs=axes_radian)
        p_01 = transf_T01_evaluated * self.origin
        rad_01 = tf.euler_from_matrix(transf_T01_evaluated.tolist(), 'rzyx')

        transf_T02_evaluated = self.T0_2.evalf(subs=axes_radian)
        p_02 = transf_T02_evaluated * self.origin
        rad_02 = tf.euler_from_matrix(transf_T02_evaluated.tolist(), 'rzyx')

        transf_T03_evaluated = self.T0_3.evalf(subs=axes_radian)
        p_03 = transf_T03_evaluated * self.origin
        rad_03 = tf.euler_from_matrix(transf_T03_evaluated.tolist(), 'rzyx')

        transf_T0X_evaluated = self.T0_X.evalf(subs=axes_radian)
        p_0X = transf_T0X_evaluated * self.origin
        rad_0X = tf.euler_from_matrix(transf_T0X_evaluated.tolist(), 'rzyx')

        transf_T04_evaluated = self.T0_4.evalf(subs=axes_radian)
        p_04 = transf_T04_evaluated * self.origin
        rad_04 = tf.euler_from_matrix(transf_T04_evaluated.tolist(), 'rzyx')

        transf_T05_evaluated = self.T0_5.evalf(subs=axes_radian)
        p_05 = transf_T05_evaluated * self.origin
        rad_05 = tf.euler_from_matrix(transf_T05_evaluated.tolist(), 'rzyx')

        transf_T06_evaluated = self.T0_6.evalf(subs=axes_radian)
        p_06 = transf_T06_evaluated * self.origin
        rad_06 = tf.euler_from_matrix(transf_T06_evaluated.tolist(), 'rzyx')

        transf_T0F_evaluated = self.T0_F.evalf(subs=axes_radian)
        p_0F = transf_T0F_evaluated * self.origin
        rad_0F = tf.euler_from_matrix(transf_T0F_evaluated.tolist(), 'rzyx')

        transf_T0FF_evaluated = self.T0_FF.evalf(subs=axes_radian)
        p_0FF = transf_T0FF_evaluated * self.origin
        rad_0FF = tf.euler_from_matrix(transf_T0FF_evaluated.tolist(), 'rzyx')
        quat_0FF = tf.quaternion_from_matrix(transf_T0F_evaluated.tolist())

        p_mm_0FF = [m*1000 for m in p_0FF]
        deg_0FF = [rtod(rad) for rad in rad_0FF]

        # TODO >> Implement Status and Turn; for now S=0, T=0
        return E6Pos.from_tuples(p_mm_0FF, deg_0FF, S=0, T=0)




kuka_solver = CustomKukaIKSolver(dh_KR360_R2830)
#calc_frame = kuka_solver.performFK(test_e6axis, debug_print=True)

#print('\n')
#print(calc_frame.orientation)
#calc_frame.abc = [90, 90, 90]
#print(calc_frame.orientation)


