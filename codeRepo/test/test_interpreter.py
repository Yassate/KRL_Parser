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

    @unittest.skip("visitVariableName not ready yet")
    def test_visitVariableName(self):
        test_string = "$IN[125]"
        parser = self.parse(test_string)
        a = parser.variableName().accept(self.interpreter)

        #self.assertIsInstance(a, VariableName)

    @unittest.skip("visitVariableName not ready yet")
    def test_visitArrayVariableSuffix(self):
        test_string = "[125]"
        parser = self.parse(test_string)
        a = parser.arrayVariableSuffix().accept(self.interpreter)
        pass

