import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + r"\generated")
print(sys.path)
from antlr4 import *
from krlLexer import krlLexer
from krlParser import krlParser
from semanalyzer import SemanticAnalyzer
import pprint as pp

def file_to_ast(file_path):
    text = FileStream(file_path)#
    lexer = krlLexer(text)
    stream = CommonTokenStream(lexer)
    parser = krlParser(stream)
    return parser.module()

file_path = r"testFiles\exampleKukaPath.src"

def src_file_to_ast(src_file_path):
    dat_file_path = src_file_path[:-3] + "dat"
    src_tree = file_to_ast(src_file_path)
    dat_tree = file_to_ast(dat_file_path)
    return src_tree, dat_tree


src_tree, dat_tree = src_file_to_ast(file_path)

myVisitor = SemanticAnalyzer()
myVisitor.visit(dat_tree)
myVisitor.visit(src_tree)


print(pp.pprint(myVisitor.variables))
#solver = IKSolver.KukaIKSolver()
#req = solver.performFK([0, 0, 0, 0, 0, 0])
#IK = solver.handle_calculate_IK2(req)
