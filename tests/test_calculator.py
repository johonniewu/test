import unittest

from calculator import EvaluationError, calculate


class CalculatorTests(unittest.TestCase):
    def test_addition(self) -> None:
        self.assertEqual(calculate("2 + 2"), 4)

    def test_operator_precedence(self) -> None:
        self.assertEqual(calculate("2 + 3 * 4"), 14)

    def test_parentheses(self) -> None:
        self.assertEqual(calculate("(2 + 3) * 4"), 20)

    def test_unary_minus(self) -> None:
        self.assertEqual(calculate("-5 + 10"), 5)

    def test_division_by_zero(self) -> None:
        with self.assertRaises(EvaluationError):
            calculate("10 / 0")

    def test_invalid_expression(self) -> None:
        with self.assertRaises(EvaluationError):
            calculate("2 + unknown")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
