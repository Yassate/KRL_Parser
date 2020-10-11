import os
import tkinter
import inspect
from antlr4 import *
from krlLexer import krlLexer
from krlParser import krlParser
from krlVisitor import krlVisitor
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import matplotlib.pyplot
import numpy as np
import IKSolver

class myKrlVisitor(krlVisitor):
    pass

def openfile(file_path):
    root = tkinter.Tk()
    #archives_dir = tkinter.filedialog.askopenfilename()
    #file_path = "\testFiles\SWP223_050_01_040R2.src"
    lines = []
    fileName, ext = os.path.splitext(file_path)
    newDir = os.path.splitext(file_path)[0]
    if ext == ".src":
        with open(r"E:\!TRANSFER\Python\testFiles\SWP223_050_01_040R2.src", 'r') as fh:
            return(fh.read().splitlines())

file_path = r"testFiles\testKRC.src"

text = FileStream(file_path)
lexer = krlLexer(text)        
stream = CommonTokenStream(lexer)        
parser = krlParser(stream)
tree = parser.module()
myVisitor = krlVisitor()
#myVisitor.visit(tree)
#print(tree.toStringTree())


KUKA_KR360R2830 = Chain(name='KUKA_KR210', links=[
    OriginLink(),
    URDFLink(
      name="axis1",
      translation_vector=[0, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 0, -1],
    ),
    URDFLink(
      name="axis2",
      translation_vector=[0.5, 0, 1.045],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="axis3",
      translation_vector=[0, 0, 1.3],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="axis4",
      translation_vector=[1.025, 0, -0.055],
      orientation=[0, 0, 0],
      rotation=[-1, 0, 0],
    ),
    URDFLink(
      name="axis5",
      translation_vector=[0, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="axis6",
      translation_vector=[0, 0, 0],
      orientation=[0, 0, 0],
      rotation=[-1, 0, 0],
    ),
    URDFLink(
      name="toolframe",
      translation_vector=[0.29, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 0, 0],
    )
])


ax1 = matplotlib.pyplot

ax = ax1.figure().add_subplot(111, projection='3d', adjustable='box')

ax.set_xlim3d([0, 2.5])
ax.set_ylim3d([0, 2.5])
ax.set_zlim3d([0, 2.5])

pistol_x = 1.815
pistol_y = 0
pistol_z = 2.345
x_offset = 0
y_offset = 0
z_offset = 0
x_pos = pistol_x + x_offset
y_pos = pistol_y + y_offset
z_pos = pistol_z + z_offset

#ax1.axis('equal')
#ax1.tight_layout()

FK = KUKA_KR360R2830.forward_kinematics([0,90,90,0,0,0,0,0])
#KUKA_KR210.plot(KUKA_KR210.forward_kinematics(list[0,90,90,0,0]), ax)
#inv_kin = KUKA_KR360R2830.inverse_kinematics([x_pos, y_pos, z_pos])
#KUKA_KR360R2830.plot(inv_kin, ax)

print(inspect.signature(KUKA_KR360R2830.inverse_kinematics))

for z in range(-15, 3):
    break
    inv_kin = KUKA_KR360R2830.inverse_kinematics([x_pos, y_pos, z_pos + z*0.2], [np.deg2rad(0), np.deg2rad(-90), np.deg2rad(90)])
    KUKA_KR360R2830.plot(inv_kin, ax)
    KUKA_KR360R2830.plot(inv_kin, ax)
    for x, val in enumerate(inv_kin):
        if x == 1 and False:
            print(-90 + np.rad2deg(val))
        #elif x == 2:
            #print(90 + np.rad2deg(val))
        else:
            print(np.rad2deg(val))
    print("NEXT")


solver = IKSolver.KukaIKSolver()
req = solver.performFK([0, 0, 0, 0, 0, 0])
IK = solver.handle_calculate_IK2(req)
matplotlib.pyplot.show()
