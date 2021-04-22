import unittest
from antlr4 import CommonTokenStream, InputStream
from krlLexer import krlLexer
from krlParser import krlParser
from krlinterpreter import KrlInterpreter, VariableName
from symtables import ScopedSymbolTable


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = KrlInterpreter(ScopedSymbolTable("GLOBAL", 0))


    def parse(self, test_string):
        text = InputStream(test_string)
        lexer = krlLexer(text)
        stream = CommonTokenStream(lexer)
        return krlParser(stream)

    def test_visitVariableName(self):
        test_string = "$IN[125]"
        parser = self.parse(test_string)
        a = parser.variableName().accept(self.interpreter)

        self.assertIsInstance(a, VariableName)

    def test_visitArrayVariableSuffix_1(self):
        test_string = "[125]"
        parser = self.parse(test_string)
        var_suf = parser.arrayVariableSuffix()
        result = var_suf.accept(self.interpreter)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [125])

    def test_visitArrayVariableSuffix_2(self):
        test_string = "[125, ]"
        parser = self.parse(test_string)
        var_suf = parser.arrayVariableSuffix()
        result = var_suf.accept(self.interpreter)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [125])

    def test_visitArrayVariableSuffix_3(self):
        test_string = "[125, 225, 325]"
        parser = self.parse(test_string)
        var_suf = parser.arrayVariableSuffix()
        result = var_suf.accept(self.interpreter)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [125, 225, 325])


