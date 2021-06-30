import sys
from antlr4 import FileStream, CommonTokenStream
from krlLexer import krlLexer
from krlParser import krlParser
from semanalyzer import SemanticAnalyzer, ScopeStack
from krlinterpreter import KrlInterpreter, VariableFactory
from iksolver import CustomKukaIKSolver, dh_KR360_R2830
from mpmath import radians as dtor
from callstack import Callstack
import os
from symtables import *

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + r"\generated")
print(sys.path)


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
        self._semanalyzer = SemanticAnalyzer(global_symtable=ScopedSymbolTable(scope_name="GLOBAL", scope_level=1))
        self._semanalyzer.visit(self._dat_tree)
        self._semanalyzer.visit(self._src_tree)
        self._symtable = self._semanalyzer.get_module_symtable()
        self._module_name = self._semanalyzer.get_module_name()

    def process_module(self):
        self._krlinterpreter = KrlInterpreter(self._symtable, Callstack(), VariableFactory(), CustomKukaIKSolver(dh_KR360_R2830))
        self._krlinterpreter.visit(self._dat_tree)
        self._krlinterpreter.visit(self._src_tree)


def main():
    file_paths = sorted([r"testFiles\cfg_test.dat", r"testFiles\exampleKukaPath.src", r"testFiles\exampleKukaPath.dat"])

    #current_module = ModuleProcessor(src_file_path)
    #current_module.analyze_semantics()
    #current_module.process_module()

    global_symtable = ScopedSymbolTable(scope_name="GLOBAL", scope_level=1)
    temp_semanalyzer = SemanticAnalyzer(ScopeStack())

    for file_path in file_paths:
        text = FileStream(file_path)
        lexer = krlLexer(text)
        stream = CommonTokenStream(lexer)
        parser = krlParser(stream)
        temp_semanalyzer.visit(parser.module())
        pass

    pass



main()
