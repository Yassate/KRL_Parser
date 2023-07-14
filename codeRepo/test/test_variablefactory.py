import unittest
from krlinterpreter import VariableFactory
from kuka_datatypes import E6Pos


class TestVariableFactory(unittest.TestCase):
    def setUp(self):
        self._var_factory = VariableFactory()

    def test_var_by_discover_E6Pos(self):
        input_data = {'X': 125.9, 'Y': 125.9, 'Z': 81.0,
                      'A': -45.0, 'B': 120.0, 'C': 30.0,
                      'S': 18, 'T': 2,
                      'E1': 0.0, 'E2': 0.0, 'E3': 0.0, 'E4': 0.0, 'E5': 0.0, 'E6': 0.0}
        result = self._var_factory.get_var_by_discover(input_data)
        expected = E6Pos.from_tuples(xyz=(125.9, 125.9, 81.0), abc=(-45, 120.0, 30.0), S=18, T=2)
        self.assertIsInstance(result, E6Pos)
        self.assertEqual(expected, result)

    def test_var_by_discover_struct(self):
        input_data = {'TOOL_NO': 64, 'BASE_NO': 64, 'IPO_FRAME': 'test', 'POINT2[]': " "}
        result = self._var_factory.get_var_by_discover(input_data)
        expected = {'TOOL_NO': 64, 'BASE_NO': 64, 'IPO_FRAME': 'test', 'POINT2[]': " "}
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)
