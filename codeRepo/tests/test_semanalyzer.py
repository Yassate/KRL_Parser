from unittest import TestCase
from semanalyzer import SemanticAnalyzer
from krlLexer import krlLexer
from krlParser import krlParser
from antlr4 import *

class TestSemanticAnalyzer(TestCase):
    def setUp(self):
        self.sem_analyzer = SemanticAnalyzer()

    @staticmethod
    def parser_from_string(test_str):
        test_string = InputStream(test_str)
        lexer = krlLexer(test_string)
        stream = CommonTokenStream(lexer)
        return krlParser(stream)

    def test_visit_literal(self):
        test_string = "2.3"
        parser = self.parser_from_string(test_string)
        literal_node = parser.literal()

        result = literal_node.accept(self.sem_analyzer)
        self.assertEqual(result, 2.3)


