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

file_path = r"testFiles\testKRC.src"

text = FileStream(file_path)
lexer = krlLexer(text)        
stream = CommonTokenStream(lexer)        
parser = krlParser(stream)
tree = parser.module()
myVisitor = krlVisitor()

solver = IKSolver.KukaIKSolver()
req = solver.performFK([0, 0, 0, 0, 0, 0])
IK = solver.handle_calculate_IK2(req)

