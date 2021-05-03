import unittest
from unittest.mock import Mock
from antlr4 import CommonTokenStream, InputStream
from krlLexer import krlLexer
from krlParser import krlParser
from krlinterpreter import KrlInterpreter, VariableName, VariableFactory
from kuka_datatypes import E6Axis, E6Pos
from callstack import ActivationRecord
import logging

logging.disable(logging.CRITICAL)

class TestInterpreter(unittest.TestCase):
    @staticmethod
    def parser_from_string(test_string):
        text = InputStream(test_string)
        lexer = krlLexer(text)
        stream = CommonTokenStream(lexer)
        return krlParser(stream)

    @staticmethod
    def interpret_var_decl_in_data_list(test_string, peek_return_value):
        parser = TestInterpreter.parser_from_string(test_string)
        mock_callstack = Mock(**{'peek.return_value': peek_return_value})
        interpreter = KrlInterpreter(callstack=mock_callstack, var_factory=VariableFactory())
        context = parser.variableDeclarationInDataList()
        context.accept(interpreter)

    @staticmethod
    def interpret_ptp_movement(test_string, peek_return_value, perform_ik_return_value):
        parser = TestInterpreter.parser_from_string(test_string)
        mock_callstack = Mock(**{'peek.return_value': peek_return_value})
        mock_ik_solver = Mock(**{'perform_ik.return_value': perform_ik_return_value})
        interpreter = KrlInterpreter(callstack=mock_callstack, ik_solver=mock_ik_solver, var_factory=VariableFactory())
        context = parser.statement()
        context.accept(interpreter)

    @staticmethod
    def interpret_assignment_expr(test_string, peek_return_value):
        parser = TestInterpreter.parser_from_string(test_string)
        mock_callstack = Mock(**{'peek.return_value': peek_return_value})
        interpreter = KrlInterpreter(callstack=mock_callstack)
        context = parser.assignmentExpression()
        context.accept(interpreter)

    @staticmethod
    def get_variable_call_result(test_string, peek_return_value):
        parser = TestInterpreter.parser_from_string(test_string)
        mock_callstack = Mock(**{'peek.return_value': peek_return_value})
        interpreter = KrlInterpreter(callstack=mock_callstack)
        context = parser.primary()
        return context.accept(interpreter)

    @staticmethod
    def get_variable_name_result(test_string):
        parser = TestInterpreter.parser_from_string(test_string)
        interpreter = KrlInterpreter()
        context = parser.variableName()
        return context.accept(interpreter)

    @staticmethod
    def get_array_var_suffix_result(test_string):
        parser = TestInterpreter.parser_from_string(test_string)
        interpreter = KrlInterpreter()
        context = parser.arrayVariableSuffix()
        return context.accept(interpreter)

    @staticmethod
    def get_unary_plus_minux_result(test_string):
        parser = TestInterpreter.parser_from_string(test_string)
        interpreter = KrlInterpreter()
        context = parser.unaryPlusMinuxExpression()
        return context.accept(interpreter)


class TestUnaryPlusMinuxExpressionInterpreter(unittest.TestCase):
    def test_visitUnaryPlusMinuxExpression_plus(self):
        unaryplusminux_test_string = "+1"
        result = TestInterpreter.get_unary_plus_minux_result(unaryplusminux_test_string)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

    def test_visitUnaryPlusMinuxExpression_minus(self):
        unaryplusminux_test_string = "-1"
        result = TestInterpreter.get_unary_plus_minux_result(unaryplusminux_test_string)
        self.assertIsInstance(result, int)
        self.assertEqual(result, -1)


class TestPtpMoveInterpreter(unittest.TestCase):
    def test_visitPtpMove_basic(self):
        ptpmove_test_string = "PTP {X 1468.736,Y 0.0,Z 3235.954,A 0.0,B 45.0,C 0.0,S 18,T 2,E1 0,E2 0,E3 0,E4 0,E5 0," \
                              "E6 0} C_DIS "
        pos_act_test_string = "$POS_ACT"
        axis_act_test_string = "$AXIS_ACT"
        peek_return_value = {"$AXIS_ACT": None, "$POS_ACT": None}
        perform_ik_return_value = E6Axis((0, 0, 0, 0, 0, 0))
        TestInterpreter.interpret_ptp_movement(ptpmove_test_string, peek_return_value, perform_ik_return_value)
        pos_act = TestInterpreter.get_variable_call_result(pos_act_test_string, peek_return_value)
        axis_act = TestInterpreter.get_variable_call_result(axis_act_test_string, peek_return_value)
        self.assertIsInstance(pos_act, E6Pos)
        self.assertIsInstance(axis_act, E6Axis)


# TODO >> MORE TESTS NEEDED, more variable types
class TestVariableDeclarationInDataListInterpreter(unittest.TestCase):
    def test_visitVariableDeclarationInDataList_E6POS(self):
        var_decl_test_string = "DECL E6POS XHP005={X 1468.736,Y 0.0,Z 3235.954,A 0.0,B 45.0,C 0.0,S 18,T 2,E1 0.0," \
                               "E2 0.0,E3 0.0,E4 0.0,E5 0.0,E6 0.0} "
        created_var_test_string = "XHP005"
        peek_return_value = ActivationRecord()
        TestInterpreter.interpret_var_decl_in_data_list(var_decl_test_string, peek_return_value)
        created_var_value = TestInterpreter.get_variable_call_result(created_var_test_string, peek_return_value)
        self.assertIsInstance(created_var_value, E6Pos)

class TestAssignmentExprInterpreter(unittest.TestCase):
    def test_visitAssignmentExpression_unindexed(self):
        assignment_test_string = "position=33"
        var_test_string = "position"
        preset_ar = ActivationRecord()
        preset_ar.initialize_var(var_name='position', value=55)
        TestInterpreter.interpret_assignment_expr(assignment_test_string, peek_return_value=preset_ar)
        var_from_ar_after_change = TestInterpreter.get_variable_call_result(var_test_string, peek_return_value=preset_ar)
        self.assertEqual(var_from_ar_after_change, 33)

    def test_visitAssignmentExpression_indexed(self):
        assignment_test_string = "position[0]=44"
        var_test_string = "position[0]"
        preset_ar = ActivationRecord()
        preset_ar.initialize_var(var_name='position', value=[31, 55])
        TestInterpreter.interpret_assignment_expr(assignment_test_string, peek_return_value=preset_ar)
        var_from_ar_after_change = TestInterpreter.get_variable_call_result(var_test_string, peek_return_value=preset_ar)
        self.assertEqual(var_from_ar_after_change, 44)

    def test_visitAssignmentExpression_3D_array(self):
        assignment_test_string = "pos3D[2, 0, 1]=44"
        var_test_string = "pos3D[2, 0, 1]"
        preset_ar = ActivationRecord()
        preset_ar.initialize_var(var_name='pos3D', value=[
                                                         [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
                                                         [[20, 21, 22], [23, 24, 25], [26, 27, 28]],
                                                         [[30, 31, 32], [33, 34, 35], [36, 37, 38]],
                                                         ])

        TestInterpreter.interpret_assignment_expr(assignment_test_string, peek_return_value=preset_ar)
        var_from_ar_after_change = TestInterpreter.get_variable_call_result(var_test_string, peek_return_value=preset_ar)
        self.assertEqual(var_from_ar_after_change, 44)


class TestVariableCallInterpreter(unittest.TestCase):
    def test_visitVariableCall_unindexed(self):
        test_string = "position"
        preset_ar = ActivationRecord()
        preset_ar.initialize_var(var_name='position', value=55)
        result = TestInterpreter.get_variable_call_result(test_string, peek_return_value=preset_ar)
        self.assertEqual(result, 55)

    def test_visitVariableCall_indexed(self):
        test_string = "position[0]"
        preset_ar = ActivationRecord()
        preset_ar.initialize_var(var_name='position', value=[31, 55])
        result = TestInterpreter.get_variable_call_result(test_string, peek_return_value=preset_ar)
        self.assertEqual(result, 31)

    def test_visitVariableCall_3D_array(self):
        test_string = "pos3D[2, 0, 1]"
        preset_ar = ActivationRecord()
        preset_ar.initialize_var(var_name='pos3D', value=[
                                                         [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
                                                         [[20, 21, 22], [23, 24, 25], [26, 27, 28]],
                                                         [[30, 31, 32], [33, 34, 35], [36, 37, 38]],
                                                         ])
        result = TestInterpreter.get_variable_call_result(test_string, peek_return_value=preset_ar)
        self.assertEqual(result, 31)
#TODO >> RESULT SHOULD BE SECOND PARAMETER OF ASSERT


class TestVariableNameInterpreter(unittest.TestCase):
    def test_visitVariableName_unindexed(self):
        test_string = "PDAT_ACT"
        result = TestInterpreter.get_variable_name_result(test_string)
        self.assertIsInstance(result, str)
        self.assertEqual("PDAT_ACT", result)

    def test_visitVariableName_indexed(self):
        test_string = "$IN[125, ]"
        result = TestInterpreter.get_variable_name_result(test_string)
        self.assertIsInstance(result, str)
        self.assertEqual("$IN[125,]", result)


class TestArrayVariableSuffixInterpreter(unittest.TestCase):
    def test_visitArrayVariableSuffix_single_index(self):
        test_string = "[125]"
        result = TestInterpreter.get_array_var_suffix_result(test_string)
        self.assertIsInstance(result, str)
        self.assertEqual("[125]", result)

    def test_visitArrayVariableSuffix_multiple_index(self):
        test_string = "[125, 225, 325]"
        result = TestInterpreter.get_array_var_suffix_result(test_string)
        self.assertIsInstance(result, str)
        self.assertEqual("[125,225,325]", result)

    def test_visitArrayVariableSuffix_char_array(self):
        test_string = "[125, ]"
        result = TestInterpreter.get_array_var_suffix_result(test_string)
        self.assertIsInstance(result, str)
        self.assertEqual("[125,]", result)
