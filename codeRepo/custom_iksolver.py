import transformations as tf
from mpmath import *
from sympy import *

import numpy as np
import time

printLogs = False

# Rotation Matrix about X
def rot_x(q):
    R_x = Matrix([[1, 0, 0],
                  [0, cos(q), -sin(q)],
                  [0, sin(q),  cos(q)]])
    return R_x

# Rotation Matrix about Y
def rot_y(q):
    R_y = Matrix([[cos(q),  0, sin(q)],
                  [0, 1, 0],
                  [-sin(q), 0, cos(q)]])
    return R_y

# Rotation Matrix about Z
def rot_z(q):
    R_z = Matrix([[cos(q), -sin(q), 0],
                  [sin(q),  cos(q), 0],
                  [0, 0, 1]])
    return R_z


# Create transformation matrix between two links
# according to Modified DH convention with given parameters
def createMatrix(alpha, a, q, d):
    mat = Matrix([[cos(q), -sin(q) * cos(alpha),    sin(q) * sin(alpha), a * cos(q)],
                  [sin(q),  cos(q) * cos(alpha),   -cos(q) * sin(alpha), a * sin(q)],
                  [0,       sin(alpha),             cos(alpha),          d],
                  [0, 0, 0, 1]])

    return mat

def rtod_tuple(rad_tuple):
    return(rtod(rad_tuple[0]), rtod(rad_tuple[1]), rtod(rad_tuple[2]))

# Radians to Degree
def rtod(q):
    return q * 180.0 / np.pi

# Degree to Radians
def dtor(q):
    return q * np.pi / 180.0

class Position:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def to_list(self):
        return [self.x, self.y, self.z]

class Orientation:
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def to_list(self):
        return [self.x, self.y, self.z, self.w]

class Euler:
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c

    def getABC_deg(self):
        return [rtod(self.a), rtod(self.b), rtod(self.c)]

class Pose:
    def __init__(self):
        self.position = Position()
        self.orientation = Orientation()
        self.euler = Euler()

# # Define DH param symbols
d0, d1, d2, d3, d4, d5, d6 = symbols('d0:7')  # link_offset_i
a0, a1, a2, a3, a4, a5, a6 = symbols('a0:7')  # link_length_i
alpha0, alpha1, alpha2, alpha3, alpha4, alpha5, alpha6 = symbols('alpha0:7')  # link_twist_i

# # Joint angle symbols (q0 is additional because of Z direction (to the ground) of first joint rotation axis)
q0, q1, q2, q3, q4, q5, q6, q7 = symbols('q0:8')  # theta_i
qi0, qi1, qi2, qi3, qi4, qi5, qi6, qi7 = symbols('qi0:8')

# ### Kuka KR360_R2830 ###
# # DH Parameters;
dh_params = {alpha0: pi,    a0: 0,      d0: 0,       q0: 0,
             alpha1: pi/2,  a1: 0.50,   d1: -1.045,  q1: qi1,
             alpha2: 0,     a2: 1.30,   d2: 0,       q2: qi2-pi/2,
             alpha3: -pi/2, a3: 0.055,  d3: 0,       q3: qi3+pi,
             alpha4: pi/2,  a4: 0,      d4: -1.025,  q4: qi4,
             alpha5: -pi/2, a5: 0,      d5: 0,       q5: qi5,
             alpha6: pi,    a6: 0,      d6: -0.29,   q6: qi6}


class DummyReq:
    # poses = [Pose()]
    def __init__(self, pos, orient, euler):
        self.poses = [Pose()]
        self.poses[0].position.x = pos[0]
        self.poses[0].position.y = pos[1]
        self.poses[0].position.z = pos[2]
        self.poses[0].orientation.x = orient[0]
        self.poses[0].orientation.y = orient[1]
        self.poses[0].orientation.z = orient[2]
        self.poses[0].orientation.w = orient[3]
        self.poses[0].euler.a = euler[0]
        self.poses[0].euler.b = euler[1]
        self.poses[0].euler.c = euler[2]

    def printReq(self):
        print("Pos : ", self.poses[0].position)
        print("Orient : ", self.poses[0].orientation)

    def set_euler(self, A, B, C):
        quat = tf.quaternion_from_euler(A, B, C)
        self.poses[0].position.x = quat[0]
        self.poses[1].position.x = quat[1]
        self.poses[2].position.x = quat[2]
        self.poses[3].position.x = quat[3]

    def get_euler(self):
        tf.transformations.euler_from_quaternion(self.orientation)

    def get_xyz_mm_list(self):
        return [self.poses[0].position.x*1000, self.poses[0].position.y*1000, self.poses[0].position.z*1000]

    def get_abc_deg_list(self):
        return self.poses[0].euler.getABC_deg()

class CustomKukaIKSolver:

    def __init__(self):

        origin = Matrix([[0], [0], [0], [1]])

        print("A0_1")
        self.A0_1 = createMatrix(alpha0, a0, q0, d0)
        print(self.A0_1)
        self.A0_1 = self.A0_1.subs(dh_params)
        print(self.A0_1)
        print("\n")

        print("A1_2")
        self.A1_2 = createMatrix(alpha1, a1, q1, d1)
        print(self.A1_2)
        self.A1_2 = self.A1_2.subs(dh_params)
        print(self.A1_2)
        print("\n")

        print("A2_3")
        self.A2_3 = createMatrix(alpha2, a2, q2, d2)
        print(self.A2_3)
        self.A2_3 = self.A2_3.subs(dh_params)
        print(self.A2_3)
        print("\n")

        print("A3_4")
        self.A3_4 = createMatrix(alpha3, a3, q3, d3)
        print(self.A3_4)
        self.A3_4 = self.A3_4.subs(dh_params)
        print(self.A3_4)
        print("\n")

        print("A4_5")
        self.A4_5 = createMatrix(alpha4, a4, q4, d4)
        print(self.A4_5)
        self.A4_5 = self.A4_5.subs(dh_params)
        print(self.A4_5)
        print("\n")

        print("A5_6")
        self.A5_6 = createMatrix(alpha5, a5, q5, d5)
        print(self.A5_6)
        self.A5_6 = self.A5_6.subs(dh_params)
        print(self.A5_6)
        print("\n")

        print("A6_F")
        self.A6_F = createMatrix(alpha6, a6, q6, d6)
        print(self.A6_F)
        self.A6_F = self.A6_F.subs(dh_params)
        print(self.A6_F)
        print("\n")

        self.T0_1 = self.A0_1
        self.T0_2 = self.T0_1 * self.A1_2
        self.T0_3 = self.T0_2 * self.A2_3
        self.T0_4 = self.T0_3 * self.A3_4
        self.T0_5 = self.T0_4 * self.A4_5
        self.T0_6 = self.T0_5 * self.A5_6
        self.T0_F = self.T0_6 * self.A6_F

        theta_s = {qi1: pi/4, qi2: pi/4, qi3: pi/6, qi4: pi/3, qi5: -pi/3, qi6: pi/4}

        transf_T01_evaluated = self.T0_1.evalf(subs=theta_s)
        p_01 = transf_T01_evaluated * origin
        deg_01 = tf.transformations.euler_from_matrix(transf_T01_evaluated.tolist(), 'sxyz')

        transf_T02_evaluated = self.T0_2.evalf(subs=theta_s)
        p_02 = transf_T02_evaluated * origin
        deg_02 = tf.transformations.euler_from_matrix(transf_T02_evaluated.tolist(), 'sxyz')

        transf_T03_evaluated = self.T0_3.evalf(subs=theta_s)
        p_03 = transf_T03_evaluated * origin
        deg_03 = tf.transformations.euler_from_matrix(transf_T03_evaluated.tolist(), 'sxyz')

        transf_T04_evaluated = self.T0_4.evalf(subs=theta_s)
        p_04 = transf_T04_evaluated * origin
        deg_04 = tf.transformations.euler_from_matrix(transf_T04_evaluated.tolist(), 'sxyz')

        transf_T05_evaluated = self.T0_5.evalf(subs=theta_s)
        p_05 = transf_T05_evaluated * origin
        deg_05 = tf.transformations.euler_from_matrix(transf_T05_evaluated.tolist(), 'sxyz')

        transf_T06_evaluated = self.T0_6.evalf(subs=theta_s)
        p_06 = transf_T06_evaluated * origin
        deg_06 = tf.transformations.euler_from_matrix(transf_T06_evaluated.tolist(), 'sxyz')

        transf_T0F_evaluated = self.T0_F.evalf(subs=theta_s)
        p_0F = transf_T0F_evaluated * origin
        deg_0F = tf.transformations.euler_from_matrix(transf_T0F_evaluated.tolist(), 'sxyz')

        #INVERSE KINEMATICS PART
        #abc and pos from point data
        matrix_pos = Matrix([[1.41967669899836], [-1.11208524918221], [0.852371412169755], [1.0]])
        abc = (dtor(-114.9896598979589), dtor(28.604830501539254), dtor(-93.71709054789805))
        matrix_abc = tf.transformations.euler_matrix(abc[0], abc[1], abc[2])

        dist_to_wc = Matrix([[0], [0], [dh_params[d6]], [1]])
        dif = matrix_abc * dist_to_wc

        pos_wcp = matrix_pos + dif
        len_link2 = abs(dh_params[a2])
        len_link3 = abs(dh_params[d4])
        dist_hor_a1_a2 = abs(dh_params[a1])
        dist_vert_a1_a2 = abs(dh_params[d1])
        dist_a3_a4 = abs(dh_params[a3])

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
        axis2 = beta1 + beta2
        axis2_deg = rtod(axis2)
        #second value of axis2 (no overhead included)
        axis2_2 = beta1 - beta2
        axis2_2_deg = rtod(axis2_2)


        gamma1 = mp.atan(dist_a3_a4/len_link3)
        gamma2 = mp.acos((dist_a3_wcp**2 + len_link2**2 - dist_a2_wcp**2)/(2*dist_a3_wcp*len_link2))

        axis3 = np.pi/2 - (gamma1 + gamma2)
        axis3_deg = rtod(axis3)
        axis3_2 = np.pi/2 - (gamma1 - gamma2)
        axis3_2_deg = rtod(axis3_2)

        #ORIENTATION

        #A1_to_A3 = {q1: }
        #transf_T04_evaluated = self.T0_4.evalf(subs=theta_s)


        print("P01")
        print(p_01)
        print(rtod_tuple(deg_01))
        print("P02")
        print(p_02)
        print(rtod_tuple(deg_02))
        print("P03")
        print(p_03)
        print(rtod_tuple(deg_03))
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


    def performFK(self, theta_t):
        # theta_t[0] = -theta_t[0]
        # theta_t[1] = theta_t[1] + dtor(90)
        # theta_t[2] = theta_t[2] - dtor(90)
        # theta_t[3] = -theta_t[3]
        # theta_t[5] = theta_t[5]


        theta_s = {q1: theta_t[0], q2: theta_t[1], q3: theta_t[2], q4: theta_t[3], q5: theta_t[4], q6: theta_t[5]}
        origin = Matrix([[0], [0], [0], [1]])

        T0_2_prime = self.T0_2.evalf(subs=theta_s)
        p2 = T0_2_prime * origin
        rpy2 = tf.transformations.euler_from_matrix(T0_2_prime.tolist())
        quat2 = tf.transformations.quaternion_from_matrix(T0_2_prime.tolist())
        debugLog("Link 2 position : {}".format(p2.tolist()))

        T0_3_prime = self.T0_3.evalf(subs=theta_s)
        p3 = T0_3_prime * origin
        rpy3 = tf.transformations.euler_from_matrix(T0_3_prime.tolist())
        quat3 = tf.transformations.quaternion_from_matrix(T0_3_prime.tolist())
        debugLog("Link 3 position : {}".format(p3.tolist()))

        T0_5_prime = self.T0_5.evalf(subs=theta_s)
        p5 = T0_5_prime * origin
        rpy5 = tf.transformations.euler_from_matrix(T0_5_prime.tolist())
        quat5 = tf.transformations.quaternion_from_matrix(T0_5_prime.tolist())
        debugLog("Link 5/Wrist Center position : {}".format(p5.tolist()))

        T0_6_prime = self.T0_6.evalf(subs=theta_s)
        p6 = T0_6_prime * origin
        rpy6 = tf.transformations.euler_from_matrix(T0_6_prime.tolist())
        quat6 = tf.transformations.quaternion_from_matrix(T0_6_prime.tolist())

        T0_G_prime = self.T0_G.evalf(subs=theta_s)
        pG = T0_G_prime * origin
        rpyG = tf.transformations.euler_from_matrix(T0_G_prime.tolist())
        quatG = tf.transformations.quaternion_from_matrix(T0_G_prime.tolist())
        debugLog("Gripper/End Effector position : {}".format(pG.tolist()))

        self.T0_6.evalf(subs=theta_s)

        T_total_prime = self.T_total.evalf(subs=theta_s)
        pFinal = T_total_prime * origin


        rpyFinal = tf.transformations.euler_from_matrix(T_total_prime.tolist())
        quatFinal = tf.transformations.quaternion_from_matrix(T_total_prime.tolist())

        rpysxyz = tf.transformations.euler_from_matrix(T_total_prime.tolist(), 'sxyz')
        rpyszyx = tf.transformations.euler_from_matrix(T_total_prime.tolist(), 'szyx')
        rpyrxyz = tf.transformations.euler_from_matrix(T_total_prime.tolist(), 'rxyz')
        rpyrzyx = tf.transformations.euler_from_matrix(T_total_prime.tolist(), 'rzyx')

        rpysxyz = (round(rtod(rpysxyz[0]), 5), round(rtod(rpysxyz[1]), 5), round(rtod(rpysxyz[2]), 5))
        rpyszyx = (round(rtod(rpyszyx[0]), 5), round(rtod(rpyszyx[1]), 5), round(rtod(rpyszyx[2]), 5))
        rpyrxyz = (round(rtod(rpyrxyz[0]), 5), round(rtod(rpyrxyz[1]), 5), round(rtod(rpyrxyz[2]), 5))
        rpyrzyx = (round(rtod(rpyrzyx[0]), 5), round(rtod(rpyrzyx[1]), 5), round(rtod(rpyrzyx[2]), 5))

        return DummyReq(pFinal, quatFinal, rpyFinal)


kukasolver = CustomKukaIKSolver()