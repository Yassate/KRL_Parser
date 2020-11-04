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


class VisitLiteralTest(VisitorTester):
    def _result_from_string(self, test_string):
        parser = self.parser_from_string(test_string)
        literal_node = parser.literal()
        return literal_node.accept(self.sem_analyzer)

    def test_visit_float_literal_returns_float(self):
        test_string = "2.38765"
        result = self._result_from_string(test_string)

        self.assertIsInstance(result, float)
        self.assertEqual(result, 2.38765)

    def test_visit_int_literal_returns_int(self):
        test_string = "3867564"
        result = self._result_from_string(test_string)

        self.assertIsInstance(result, int)
        self.assertEqual(result, 3867564)

    def test_visit_bool_literal_returns_bool(self):
        test_string = "tRUe"
        result = self._result_from_string(test_string)

        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)

    def test_visit_string_returns_string(self):
        test_string = '"test_string"'
        result = self._result_from_string(test_string)


        self.assertIsInstance(result, str)
        self.assertEqual(result, "test_string")

    def test_visit_char_returns_string_of_length_1(self):
        test_string = "'t'"
        result = self._result_from_string(test_string)

        self.assertIsInstance(result, str)
        self.assertEqual(result, "t")
