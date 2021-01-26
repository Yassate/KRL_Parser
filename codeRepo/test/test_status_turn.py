from unittest import TestCase
from kuka_datatypes import Status, Turn


class TestStatus(TestCase):
    def setUp(self):
        self.status_all_true = Status(0b0111)
        self.status_all_false = Status(0b0000)

    def test_in_oh_area(self):
        result = self.status_all_true.in_OH_area
        self.assertEqual(result, 1)

    def test_a3_in_pos_area(self):
        result = self.status_all_true.a3_in_pos_area
        self.assertEqual(result, 1)

    def test_a5_on_plus(self):
        result = self.status_all_true.a5_on_plus
        self.assertEqual(result, 1)

    def test_not_in_oh_area(self):
        result = self.status_all_false.in_OH_area
        self.assertEqual(result, 0)

    def test_not_a3_in_pos_area(self):
        result = self.status_all_false.a3_in_pos_area
        self.assertEqual(result, 0)

    def test_not_a5_on_plus(self):
        result = self.status_all_false.a5_on_plus
        self.assertEqual(result, 0)


class TestTurn(TestCase):
    def setUp(self):
        self.turn_all_true = Turn(0b111111)
        self.turn_all_false = Turn(0b000000)

    def test_a1_on_plus_or_zero(self):
        result = self.turn_all_true.a1_on_plus_or_zero
        self.assertEqual(result, 1)

    def test_a2_on_plus_or_zero(self):
        result = self.turn_all_true.a1_on_plus_or_zero
        self.assertEqual(result, 1)

    def test_a3_on_plus_or_zero(self):
        result = self.turn_all_true.a1_on_plus_or_zero
        self.assertEqual(result, 1)

    def test_a4_on_plus_or_zero(self):
        result = self.turn_all_true.a1_on_plus_or_zero
        self.assertEqual(result, 1)

    def test_a5_on_plus_or_zero(self):
        result = self.turn_all_true.a1_on_plus_or_zero
        self.assertEqual(result, 1)

    def test_a6_on_plus_or_zero(self):
        result = self.turn_all_true.a1_on_plus_or_zero
        self.assertEqual(result, 1)

    def test_a1_not_on_plus_or_zero(self):
        result = self.turn_all_false.a1_on_plus_or_zero
        self.assertEqual(result, 0)

    def test_a2_not_on_plus_or_zero(self):
        result = self.turn_all_false.a2_on_plus_or_zero
        self.assertEqual(result, 0)

    def test_a3_not_on_plus_or_zero(self):
        result = self.turn_all_false.a3_on_plus_or_zero
        self.assertEqual(result, 0)

    def test_a4_not_on_plus_or_zero(self):
        result = self.turn_all_false.a4_on_plus_or_zero
        self.assertEqual(result, 0)

    def test_a5_not_on_plus_or_zero(self):
        result = self.turn_all_false.a5_on_plus_or_zero
        self.assertEqual(result, 0)

    def test_a6_not_on_plus_or_zero(self):
        result = self.turn_all_false.a6_on_plus_or_zero
        self.assertEqual(result, 0)
