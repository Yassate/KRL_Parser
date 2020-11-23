import transformations.transformations as tf
from mpmath import mp, sqrt
from mpmath import radians as dtor
from mpmath import degrees as rtod
from sympy import symbols, pi, cos, sin, Matrix
import numpy as np
from accessify import private
from iksolver import rot_y, rot_z


def createMatrix(alpha, a, q, d):
    mat = Matrix([[cos(q), -sin(q) * cos(alpha),    sin(q) * sin(alpha), a * cos(q)],
                  [sin(q),  cos(q) * cos(alpha),   -cos(q) * sin(alpha), a * sin(q)],
                  [0,       sin(alpha),             cos(alpha),          d],
                  [0, 0, 0, 1]])

    return mat


def rtod_tuple(rad_tuple):
    return(rtod(rad_tuple[0]), rtod(rad_tuple[1]), rtod(rad_tuple[2]))


class Frame:
    def __init__(self, position=None, orientation=None):
        self.position = position
        self.orientation = orientation
        self._abc = [rtod(angle) for angle in tf.euler_from_quaternion(orientation)]

    @property
    def abc(self):
        return self._abc

    @abc.setter
    def abc(self, value):
        self.orientation = tf.quaternion_from_euler(value[0], value[1], value[2])
        self._abc = value

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def z(self):
        return self.position[2]


class E6Axis:
    def __init__(self, axis_values = None):
        self.axis_values = axis_values
        self.A1, self.A2, self.A3, self.A4, self.A5, self.A6 = axis_values

    def get_in_radians(self):
        axes_radians = [dtor(axis) for axis in self.axis_values]
        return axes_radians

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

#INFO >> PROBABLY INVERSE KINEMATICS FOR ANGLES WILL NOT WORK 100% PROPERLY; rotation point of axis4 and axis5 is different; should lie on WCP
#TODO >> Change DH parameters to move rotation point of axis 4 and axis 5 to WCP
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

        #INVERSE KINEMATICS PART
        #abc and pos from point data
        matrix_pos = Matrix([[1.41967669899836], [-1.11208524918221], [0.852371412169755], [1.0]])
        abc = (dtor(-114.9896598979589), dtor(28.604830501539254), dtor(-93.71709054789805))
        matrix_abc = tf.euler_matrix(abc[0], abc[1], abc[2], axes='sxyz')
        robot_axes = [45, -45, 120, 60, -60, 45]

        dist_to_wc = Matrix([[0], [0], [-abs(self.dh_params[d7])], [1]])
        dif = matrix_abc * dist_to_wc

        pos_wcp = matrix_pos + dif
        len_link2 = abs(self.dh_params[a2])
        len_link3 = abs(self.dh_params[dX])
        dist_hor_a1_a2 = abs(self.dh_params[a1])
        dist_vert_a1_a2 = abs(self.dh_params[d1])
        dist_a3_a4 = abs(self.dh_params[a3])


        #TODO >> Overhead calculation need to be implemented
        axis1 = mp.atan(-pos_wcp[1]/pos_wcp[0])
        axis1_deg = rtod(axis1)

        dist_hor_bf_wcp = mp.sqrt(pos_wcp[0]**2 + pos_wcp[1]**2)
        dist_hor_a2_wcp = dist_hor_bf_wcp - dist_hor_a1_a2
        dist_vert_a2_wcp = pos_wcp[2] - dist_vert_a1_a2

        dist_a2_wcp = mp.sqrt(dist_hor_a2_wcp**2 + dist_vert_a2_wcp**2)
        dist_a3_wcp = mp.sqrt(len_link3**2 + dist_a3_a4**2)

        beta1 = mp.atan(dist_vert_a2_wcp/dist_hor_a2_wcp)
        beta2 = mp.acos((dist_a2_wcp**2 + len_link2**2 - dist_a3_wcp**2)/(2*dist_a2_wcp*len_link2))

        #TODO >> Overhead calculation need to be implemented
        axis2 = -(beta1 + beta2)
        axis2_deg = rtod(axis2)
        #second value of axis2 (no overhead included)
        axis2_2 = -(beta1 - beta2)
        axis2_2_deg = rtod(axis2_2)

        gamma1 = mp.atan(dist_a3_a4/len_link3)
        gamma2 = mp.acos((dist_a3_wcp**2 + len_link2**2 - dist_a2_wcp**2)/(2*dist_a3_wcp*len_link2))

        axis3 = np.pi - (gamma1 + gamma2)
        axis3_deg = rtod(axis3)
        axis3_2 = np.pi - (gamma1 - gamma2)
        axis3_2_deg = rtod(axis3_2)

        #TODO >> ORIENTATION TO REVIEW - DH PARAMETERS CHANGED
        #ORIENTATION

        A1_to_A3 = {qi1: axis1, qi2: dtor(90) + axis2, qi3: -dtor(90) + axis3}
        R_0_3 = self.T0_4.evalf(subs=A1_to_A3)[0:3, 0:3]

        temp_1 = createMatrix(alpha=-np.pi/2, a=0, q=np.pi/2, d=0)[0:3, 0:3]
        temp_2 = createMatrix(alpha=0, a=0, q=np.pi/2, d=0)[0:3, 0:3]

        R_temp = R_0_3 * rot_y(-np.pi/2) * rot_z(np.pi)

        # R_0_3 = R_0_3 * temp_1
        # R_0_3 = R_0_3 * temp_2
        # R_0_3 = R_temp

        R_0_3_inv = R_0_3.inv()
        R_0_6 = matrix_abc[0:3, 0:3]


        R_3_6 = R_0_3_inv * R_0_6
        print(R_3_6)

        #theta_p = {qi4: pi/3, qi5: pi/3, qi6: pi/4}

        #t_c = (self.A4_5 * self.A5_6 * self.A6_F).evalf(subs=theta_p)[0:3, 0:3]
        #t_c = (self.A5_6 * self.A6_F).evalf(subs=theta_p)[0:3, 0:3]
        #R_3_6 = t_c

        axis5_1 = mp.atan2(R_3_6[2, 2], sqrt(1-R_3_6[2, 2] ** 2))
        axis5_2 = mp.atan2(R_3_6[2, 2], -sqrt(1-R_3_6[2, 2] ** 2))
        axis5_3 = mp.atan2(sqrt(R_3_6[0,2]**2+R_3_6[1,2]**2), R_3_6[2,2])
        axis5_4 = mp.acos(R_3_6[2, 2])
        axis5_1_deg = rtod(axis5_1)
        axis5_2_deg = rtod(axis5_2)
        axis5_3_deg = rtod(axis5_3)
        axis5_4_deg = rtod(axis5_4)

        axis4_1 = mp.atan2(R_3_6[0, 2], R_3_6[1, 2])
        axis4_2 = mp.atan2(-R_3_6[0, 2], -R_3_6[1, 2])
        axis4_3 = mp.atan2(R_3_6[1,2], R_3_6[0,2])
        axis4_1_deg = rtod(axis4_1)
        axis4_2_deg = rtod(axis4_2)
        axis4_3_deg = rtod(axis4_3)


        axis6_1 = mp.atan2(-R_3_6[2, 0], R_3_6[2, 1])
        axis6_2 = mp.atan2(R_3_6[2, 0], -R_3_6[2, 1])
        axis6_3 = mp.atan2(R_3_6[2, 1], -R_3_6[2, 0])
        axis6_1_deg = rtod(axis6_1)
        axis6_2_deg = rtod(axis6_2)
        axis6_3_deg = rtod(axis6_3)

        print(1)

    def performFK(self, input_e6_axis, debug_print=False):

        e6_axis_radians = input_e6_axis.get_in_radians()

        axes_radian = {qi1: e6_axis_radians[0],
                       qi2: dtor(90) + e6_axis_radians[1],
                       qi3: -dtor(90) + e6_axis_radians[2],
                       qi4: e6_axis_radians[3],
                       qi5: e6_axis_radians[4],
                       qi6: e6_axis_radians[5]}

        transf_T01_evaluated = self.T0_1.evalf(subs=axes_radian)
        p_01 = transf_T01_evaluated * self.origin
        deg_01 = tf.euler_from_matrix(transf_T01_evaluated.tolist(), 'sxyz')

        transf_T02_evaluated = self.T0_2.evalf(subs=axes_radian)
        p_02 = transf_T02_evaluated * self.origin
        deg_02 = tf.euler_from_matrix(transf_T02_evaluated.tolist(), 'sxyz')

        transf_T03_evaluated = self.T0_3.evalf(subs=axes_radian)
        p_03 = transf_T03_evaluated * self.origin
        deg_03 = tf.euler_from_matrix(transf_T03_evaluated.tolist(), 'sxyz')

        transf_T0X_evaluated = self.T0_X.evalf(subs=axes_radian)
        p_0X = transf_T0X_evaluated * self.origin
        deg_0X = tf.euler_from_matrix(transf_T0X_evaluated.tolist(), 'sxyz')

        transf_T04_evaluated = self.T0_4.evalf(subs=axes_radian)
        p_04 = transf_T04_evaluated * self.origin
        deg_04 = tf.euler_from_matrix(transf_T04_evaluated.tolist(), 'sxyz')

        transf_T05_evaluated = self.T0_5.evalf(subs=axes_radian)
        p_05 = transf_T05_evaluated * self.origin
        deg_05 = tf.euler_from_matrix(transf_T05_evaluated.tolist(), 'sxyz')

        transf_T06_evaluated = self.T0_6.evalf(subs=axes_radian)
        p_06 = transf_T06_evaluated * self.origin
        deg_06 = tf.euler_from_matrix(transf_T06_evaluated.tolist(), 'sxyz')

        transf_T0F_evaluated = self.T0_F.evalf(subs=axes_radian)
        p_0F = transf_T0F_evaluated * self.origin
        deg_0F = tf.euler_from_matrix(transf_T0F_evaluated.tolist(), 'sxyz')

        #TODO >> CHECK IF DEGREES ARE IN CORRECT ORDER (rzyx/sxyz?)
        transf_T0FF_evaluated = self.T0_FF.evalf(subs=axes_radian)
        p_0FF = transf_T0FF_evaluated * self.origin
        deg_0FF = tf.euler_from_matrix(transf_T0FF_evaluated.tolist(), 'sxyz')
        quat_0FF = tf.quaternion_from_matrix(transf_T0F_evaluated.tolist())


        if debug_print:
            print("P01")
            print(p_01)
            print(rtod_tuple(deg_01))
            print("P02")
            print(p_02)
            print(rtod_tuple(deg_02))
            print("P03")
            print(p_03)
            print(rtod_tuple(deg_03))
            print("P0X")
            print(p_0X)
            print(rtod_tuple(deg_0X))
            print("P04")
            print(p_04)
            print(rtod_tuple(deg_04))
            print("P05")
            print(p_05)
            print(rtod_tuple(deg_05))
            print("P06")
            print(p_06)
            print(rtod_tuple(deg_06))
            print("P0F")
            print(p_0F)
            print(rtod_tuple(deg_0F))
            print("P0FF")
            print(p_0FF)
            print(rtod_tuple(deg_0FF))

        return Frame(p_0FF, quat_0FF)

    @private
    def fortestonly(self):
        pass

#test_e6axis = E6Axis([45, 45, 30, 60, -60, 45])

#kuka_solver = CustomKukaIKSolver(dh_KR360_R2830)
#calc_frame = kuka_solver.performFK(test_e6axis, debug_print=True)

#print('\n')
#print(calc_frame.orientation)
#calc_frame.abc = [90, 90, 90]
#print(calc_frame.orientation)


