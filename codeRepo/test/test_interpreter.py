import unittest
from unittest.mock import Mock
from antlr4 import CommonTokenStream, InputStream
from krlLexer import krlLexer
from krlParser import krlParser
from krlinterpreter import KrlInterpreter, VariableName

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        pass

    def parse(self, test_string):
        text = InputStream(test_string)
        lexer = krlLexer(text)
        stream = CommonTokenStream(lexer)
        return krlParser(stream)

    def test_visitVariableCall_unindexed(self):
        peek_return_value = {'position': 55}
        mock_callstack = Mock()
        mock_callstack.peek.return_value = peek_return_value
        interpreter = KrlInterpreter(symtable=None, callstack=mock_callstack, var_factory=None, ik_solver=None)
        test_string = "position"
        parser = self.parse(test_string)
        result = parser.primary().accept(interpreter)
        self.assertEqual(result, 55)

    def test_visitVariableCall_indexed(self):
        peek_return_value = {'position': [31, 55]}
        mock_callstack = Mock()
        mock_callstack.peek.return_value = peek_return_value
        interpreter = KrlInterpreter(symtable=None, callstack=mock_callstack, var_factory=None, ik_solver=None)
        test_string = "position[0]"
        parser = self.parse(test_string)
        result = parser.primary().accept(interpreter)
        self.assertEqual(result, 31)

    def test_visitVariableCall_3D_array(self):
        peek_return_value = {'pos3D': [
                                      [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
                                      [[20, 21, 22], [23, 24, 25], [26, 27, 28]],
                                      [[30, 31, 32], [33, 34, 35], [36, 37, 38]],
                                      ]}
        mock_callstack = Mock()
        mock_callstack.peek.return_value = peek_return_value
        test_string = "pos3D[2, 0, 1]"
        interpreter = KrlInterpreter(symtable=None, callstack=mock_callstack, var_factory=None, ik_solver=None)
        parser = self.parse(test_string)
        result = parser.primary().accept(interpreter)
        self.assertEqual(result, 31)

    def test_visitVariableName_unindexed(self):
        test_string = "PDAT_ACT"
        parser = self.parse(test_string)
        interpreter = KrlInterpreter(None, None, None, None)
        result = parser.variableName().accept(interpreter)
        expected = VariableName(name="PDAT_ACT", indices=None)
        self.assertIsInstance(result, VariableName)
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.indices, expected.indices)

    def test_visitVariableName_indexed(self):
        test_string = "$IN[125,]"
        parser = self.parse(test_string)
        interpreter = KrlInterpreter(None, None, None, None)
        result = parser.variableName().accept(interpreter)
        expected = VariableName(name='$IN', indices=[125])
        self.assertIsInstance(result, VariableName)
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.indices, expected.indices)

    def test_visitArrayVariableSuffix_single_index(self):
        test_string = "[125]"
        parser = self.parse(test_string)
        interpreter = KrlInterpreter(None, None, None, None)
        var_suf = parser.arrayVariableSuffix()
        result = var_suf.accept(interpreter)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [125])

    def test_visitArrayVariableSuffix_multiple_index(self):
        test_string = "[125, 225, 325]"
        parser = self.parse(test_string)
        interpreter = KrlInterpreter(None, None, None, None)
        var_suf = parser.arrayVariableSuffix()
        result = var_suf.accept(interpreter)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [125, 225, 325])

    def test_visitArrayVariableSuffix_char_array(self):
        test_string = "[125, ]"
        parser = self.parse(test_string)
        interpreter = KrlInterpreter(None, None, None, None)
        var_suf = parser.arrayVariableSuffix()
        result = var_suf.accept(interpreter)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [125])


