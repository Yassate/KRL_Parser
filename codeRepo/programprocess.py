import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + r"\generated")
print(sys.path)
from antlr4 import *
from krlLexer import krlLexer
from krlParser import krlParser
from semanalyzer import SemanticAnalyzer
from krlinterpreter import KrlInterpreter
from iksolver import KukaIKSolver, DummyReq, Position, Orientation, rtod, dtor


import pprint as pp
from symtables import ScopedSymbolTable

def axes_deg_to_radian(axis_pos):
    new_axes = []
    for axis in axis_pos:
        new_axes.append(dtor(axis))
    return new_axes

class ModuleProcessor:
    def __init__(self, src_file_path):
        self._src_tree = None
        self._dat_tree = None
        self._src_file_path = src_file_path
        self._semanalyzer = None
        self._krlinterpreter = None
        self._src_file_to_ast()
        self._symtable = None
        self._module_name = None

    @staticmethod
    def _file_to_ast(file_path):
        text = FileStream(file_path)
        lexer = krlLexer(text)
        stream = CommonTokenStream(lexer)
        parser = krlParser(stream)
        return parser.module()

    def _src_file_to_ast(self):
        dat_file_path = self._src_file_path[:-3] + "dat"
        self._src_tree = self._file_to_ast(self._src_file_path)
        self._dat_tree = self._file_to_ast(dat_file_path)

    def analyze_semantics(self):
        self._semanalyzer = SemanticAnalyzer()
        self._semanalyzer.visit(self._dat_tree)
        self._semanalyzer.visit(self._src_tree)
        self._symtable = self._semanalyzer.get_module_symtable()
        self._module_name = self._semanalyzer.get_module_name()

    def process_module(self):
        self._krlinterpreter = KrlInterpreter(self._symtable)
        self._krlinterpreter.visit(self._dat_tree)
        self._krlinterpreter.visit(self._src_tree)


src_file_path = r"testFiles\exampleKukaPath.src"

current_module = ModuleProcessor(src_file_path)
current_module.analyze_semantics()
current_module.process_module()



#print(pp.pprint(myVisitor.variables))
solver = KukaIKSolver()
req = solver.performFK([0, 0, 0, 0, 0, 0])
IK = solver.handle_calculate_IK2(req)

# TODO >> Test cases, write unit tests for IKSolver; get test cases from Delmia for FK and IK test on random FK params

Positions = []
Positions.append([0, -90, 90, 0, 0, 0])
Positions.append([0, -90, 45, 0, 0, 0])
Positions.append([45, -90, 45, 0, 0, 0])
Positions.append([45, -90, 90, 0, 0, 0])
Positions.append([45, -90, 90, 0, 30, 0])
Positions.append([45, -90, 90, 0, 30, 30])
Positions.append([45, -90, 90, 30, 30, 30])

solved = []

for position in Positions:
    req = solver.performFK(axes_deg_to_radian(position))
    solved.append(req.poses[0].position)

Pos = Position()
Orient = Orientation()
req = DummyReq(Pos.to_list(), Orient.to_list())
#req.set_euler()
print("A")
