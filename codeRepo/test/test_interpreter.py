import unittest
from antlr4 import CommonTokenStream, InputStream
from krlLexer import krlLexer
from krlParser import krlParser
from krlinterpreter import KrlInterpreter, VariableName, VariableFactory
from symtables import ScopedSymbolTable
from callstack import Callstack
from iksolver import CustomKukaIKSolver, dh_KR360_R2830


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = KrlInterpreter(ScopedSymbolTable("GLOBAL", 0), Callstack(), VariableFactory(), CustomKukaIKSolver(dh_KR360_R2830))

    def parse(self, test_string):
        text = InputStream(test_string)
        lexer = krlLexer(text)
        stream = CommonTokenStream(lexer)
        return krlParser(stream)

    @unittest.skip("multiple index feature need to be done, callstack need to be mocked")
    def test_visitVariableCall(self):
        test_string = "pos3D[10, 20, 30]"
        parser = self.parse(test_string)
        result = parser.primary().accept(self.interpreter)

        var_name = VariableName(name="pos3D", indices=[10, 20, 30])
        #indices = var_name.indices
        #ar = self._callstack.peek()
        #value = ar[var_name.name][indices[0]] if indices else ar[var_name.name]
        #return value

    def test_visitVariableName_indexed(self):
        test_string = "$IN[125,]"
        parser = self.parse(test_string)
        result = parser.variableName().accept(self.interpreter)
        expected = VariableName(name='$IN', indices=[125])
        self.assertIsInstance(result, VariableName)
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.indices, expected.indices)

    def test_visitVariableName_nonindexed(self):
        test_string = "PDAT_ACT"
        parser = self.parse(test_string)
        result = parser.variableName().accept(self.interpreter)
        expected = VariableName(name="PDAT_ACT", indices=None)
        self.assertIsInstance(result, VariableName)
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.indices, expected.indices)

    def test_visitArrayVariableSuffix_single_index(self):
        test_string = "[125]"
        parser = self.parse(test_string)
        var_suf = parser.arrayVariableSuffix()
        result = var_suf.accept(self.interpreter)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [125])

    def test_visitArrayVariableSuffix_multiple_index(self):
        test_string = "[125, 225, 325]"
        parser = self.parse(test_string)
        var_suf = parser.arrayVariableSuffix()
        result = var_suf.accept(self.interpreter)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [125, 225, 325])

    def test_visitArrayVariableSuffix_char_array(self):
        test_string = "[125, ]"
        parser = self.parse(test_string)
        var_suf = parser.arrayVariableSuffix()
        result = var_suf.accept(self.interpreter)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [125])


