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



solver = IKSolver.KukaIKSolver()
req = solver.performFK([0, 0, 0, 0, 0, 0])
IK = solver.handle_calculate_IK2(req)
