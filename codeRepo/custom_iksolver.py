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
d1, d2, d3, d4, d5, d6 = symbols('d1:7')  # link_offset_i
a1, a2, a3, a4, a5, a6 = symbols('a1:7')  # link_length_i
alpha1, alpha2, alpha3, alpha4, alpha5, alpha6 = symbols('alpha1:7')  # link_twist_i

# # Joint angle symbols
q1, q2, q3, q4, q5, q6, q7 = symbols('q1:8')  # theta_i

# ### Kuka KR360_R2830 ###
# # DH Parameters
dh_params = {alpha1: -pi/2, a1: 0.50,  d1: 1.045,  q1: q1,
             alpha2: 0,     a2: 1.30,  d2: 0,      q2: q2-pi/2}

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

        # # Define Modified DH Transformation matrix
        # #### Homogeneous Transforms
        # return

        origin = Matrix([[0], [0], [0], [1]])


        self.A1 = createMatrix(alpha1, a1, q1, d1)
        print(self.A1)
        self.A1 = self.A1.subs(dh_params)
        print(self.A1)
        print("\n")

        self.A2 = createMatrix(alpha2, a2, q2, d2)
        print(self.A2)
        self.A2 = self.A2.subs(dh_params)
        print(self.A2)
        print("\n")

        self.T0_1 = self.A1


        self.T0_2 = self.A1 * self.A2
        print(self.T0_2)

        self.T0_2 = simplify(self.A1 * self.A2)
        print(self.T0_2)

        theta_s = {q1: 0, q2: 0}

        transf_evaluated = self.T0_2.evalf(subs=theta_s)
        pFinal = transf_evaluated * origin
        rpyFinal = tf.transformations.euler_from_matrix(transf_evaluated.tolist())

        print(pFinal)
        print(rpyFinal)

        # #self.T0_1 = createMatrix(alpha0, a0, q1, d1)
        # self.T0_1 = self.T0_1.subs(s)
        #
        # self.T1_2 = createMatrix(alpha1, a1, q2, d2)
        # self.T1_2 = self.T1_2.subs(s)
        #
        # self.T2_3 = createMatrix(alpha2, a2, q3, d3)
        # self.T2_3 = self.T2_3.subs(s)
        #
        # self.T3_4 = createMatrix(alpha3, a3, q4, d4)
        # self.T3_4 = self.T3_4.subs(s)
        #
        # self.T4_5 = createMatrix(alpha4, a4, q5, d5)
        # self.T4_5 = self.T4_5.subs(s)
        #
        # self.T5_6 = createMatrix(alpha5, a5, q6, d6)
        # self.T5_6 = self.T5_6.subs(s)
        #
        # self.T6_G = createMatrix(alpha6, a6, q7, d7)
        # self.T6_G = self.T6_G.subs(s)

        # # Composition of Homogenous Transforms
        #self.T0_2 = simplify(self.T0_1 * self.T1_2)  # base_link to link 2
        #self.T0_3 = simplify(self.T0_2 * self.T2_3)  # base_link to link 3
        #self.T0_4 = simplify(self.T0_3 * self.T3_4)  # base_link to link 3
        #self.T0_5 = simplify(self.T0_4 * self.T4_5)  # base_link to link 3
        #self.T0_6 = simplify(self.T0_5 * self.T5_6)  # base_link to link 3
        #self.T0_G = simplify(self.T0_6 * self.T6_G)  # base_link to link 3

        # INFO temporary deleted "simplify" because is terribly slow
        # self.T0_2 = self.T0_1 * self.T1_2  # base_link to link 2
        # self.T0_3 = self.T0_2 * self.T2_3  # base_link to link 3
        # self.T0_4 = self.T0_3 * self.T3_4  # base_link to link 4
        # self.T0_5 = self.T0_4 * self.T4_5  # base_link to link 5
        # self.T0_6 = self.T0_5 * self.T5_6  # base_link to link 6
        # self.T0_G = self.T0_6 * self.T6_G  # base_link to link G

    # INFO >> My modifications of input angles according to KUKA robot rotation signs
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


