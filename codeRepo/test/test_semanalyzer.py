from unittest import TestCase
from semanalyzer import SemanticAnalyzer
from krlLexer import krlLexer
from krlParser import krlParser
from antlr4 import *


class VisitorTester(TestCase):
    def setUp(self):
        self.sem_analyzer = SemanticAnalyzer()

    @staticmethod
    def parser_from_string(test_str):
        test_string = InputStream(test_str)
        lexer = krlLexer(test_string)
        stream = CommonTokenStream(lexer)
        return krlParser(stream)