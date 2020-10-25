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

import pprint as pp
from symtables import ScopedSymbolTable


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
        self._krlinterpreter = KrlInterpreter()
        self._krlinterpreter.visit(self._dat_tree)
        self._krlinterpreter.visit(self._dat_tree)


src_file_path = r"testFiles\exampleKukaPath.src"

current_module = ModuleProcessor(src_file_path)
current_module.analyze_semantics()
current_module.process_module()

print("A")

#print(pp.pprint(myVisitor.variables))
#solver = IKSolver.KukaIKSolver()
#req = solver.performFK([0, 0, 0, 0, 0, 0])
#IK = solver.handle_calculate_IK2(req)
