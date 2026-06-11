#!/usr/bin/env python3
"""Comprehensive tests for the scientific calculator engine."""

import math
import unittest
from calculator import evaluate, format_result


class TestBasicArithmetic(unittest.TestCase):
    """Core arithmetic operations."""

    def test_addition(self):
        self.assertEqual(evaluate("2 + 3"), 5)

    def test_subtraction(self):
        self.assertEqual(evaluate("10 - 4"), 6)

    def test_multiplication(self):
        self.assertEqual(evaluate("3 * 7"), 21)

    def test_division(self):
        self.assertEqual(evaluate("15 / 3"), 5.0)

    def test_divide_by_zero(self):
        self.assertIsNone(evaluate("1 / 0"))

    def test_modulo(self):
        self.assertEqual(evaluate("10 % 3"), 1)

    def test_pemdas(self):
        self.assertEqual(evaluate("2 + 3 * 4"), 14)

    def test_parentheses(self):
        self.assertEqual(evaluate("(2 + 3) * 4"), 20)

    def test_decimals(self):
        self.assertEqual(evaluate("3.5 + 2.5"), 6.0)

    def test_empty_expr(self):
        self.assertIsNone(evaluate(""))
        self.assertIsNone(evaluate("   "))


class TestExponent(unittest.TestCase):
    """Exponentiation via ^ and **."""

    def test_caret(self):
        self.assertEqual(evaluate("2 ^ 3"), 8)

    def test_double_star(self):
        self.assertEqual(evaluate("2 ** 3"), 8)

    def test_negative_base(self):
        self.assertEqual(evaluate("(-2) ^ 3"), -8)

    def test_fractional(self):
        self.assertEqual(evaluate("9 ^ 0.5"), 3.0)

    def test_zero_exponent(self):
        self.assertEqual(evaluate("5 ^ 0"), 1)

    def test_negative_exponent(self):
        self.assertAlmostEqual(evaluate("2 ^ -1"), 0.5)


class TestSquareRoot(unittest.TestCase):
    """sqrt function."""

    def test_basic(self):
        self.assertEqual(evaluate("sqrt(9)"), 3.0)

    def test_in_expression(self):
        self.assertEqual(evaluate("sqrt(25) + 1"), 6.0)

    def test_of_zero(self):
        self.assertEqual(evaluate("sqrt(0)"), 0.0)

    def test_negative(self):
        self.assertIsNone(evaluate("sqrt(-1)"))


class TestTrigonometry(unittest.TestCase):
    """Trig functions in radian mode (default)."""

    def test_sin_rad(self):
        self.assertAlmostEqual(evaluate("sin(0)"), 0)
        self.assertAlmostEqual(evaluate("sin(pi / 2)"), 1, places=10)

    def test_cos_rad(self):
        self.assertAlmostEqual(evaluate("cos(0)"), 1)
        self.assertAlmostEqual(evaluate("cos(pi)"), -1, places=10)

    def test_tan_rad(self):
        self.assertAlmostEqual(evaluate("tan(0)"), 0)
        self.assertAlmostEqual(evaluate("tan(pi / 4)"), 1, places=10)

    def test_asin_rad(self):
        self.assertAlmostEqual(evaluate("asin(1)"), math.pi / 2, places=10)

    def test_acos_rad(self):
        self.assertAlmostEqual(evaluate("acos(1)"), 0, places=10)

    def test_atan_rad(self):
        self.assertAlmostEqual(evaluate("atan(1)"), math.pi / 4, places=10)

    def test_sin_in_expression(self):
        self.assertAlmostEqual(evaluate("sin(pi / 6) * 2"), 1, places=10)


class TestTrigonometryDeg(unittest.TestCase):
    """Trig functions in degree mode."""

    def test_sin_deg(self):
        self.assertAlmostEqual(evaluate("sin(90)", deg_mode=True), 1)

    def test_cos_deg(self):
        self.assertAlmostEqual(evaluate("cos(0)", deg_mode=True), 1)
        self.assertAlmostEqual(evaluate("cos(60)", deg_mode=True), 0.5, places=10)

    def test_tan_deg(self):
        self.assertAlmostEqual(evaluate("tan(45)", deg_mode=True), 1, places=10)

    def test_asin_deg(self):
        self.assertAlmostEqual(evaluate("asin(1)", deg_mode=True), 90, places=10)

    def test_acos_deg(self):
        self.assertAlmostEqual(evaluate("acos(0)", deg_mode=True), 90, places=10)

    def test_atan_deg(self):
        self.assertAlmostEqual(evaluate("atan(1)", deg_mode=True), 45, places=10)


class TestLogarithms(unittest.TestCase):
    """Log and natural log."""

    def test_log10(self):
        self.assertAlmostEqual(evaluate("log(100)"), 2)

    def test_log10_alt(self):
        self.assertAlmostEqual(evaluate("log10(1000)"), 3)

    def test_ln(self):
        self.assertAlmostEqual(evaluate("ln(euler)"), 1, places=10)

    def test_ln_of_one(self):
        self.assertAlmostEqual(evaluate("ln(1)"), 0)


class TestExponential(unittest.TestCase):
    """exp and related functions."""

    def test_exp_basic(self):
        self.assertAlmostEqual(evaluate("exp(0)"), 1)

    def test_exp(self):
        self.assertAlmostEqual(evaluate("exp(1)"), math.e, places=10)


class TestFactorial(unittest.TestCase):
    """Factorial via ! notation."""

    def test_basic(self):
        self.assertEqual(evaluate("5!"), 120)

    def test_zero(self):
        self.assertEqual(evaluate("0!"), 1)

    def test_one(self):
        self.assertEqual(evaluate("1!"), 1)

    def test_in_expression(self):
        self.assertEqual(evaluate("3! + 2"), 8)

    def test_multiple(self):
        self.assertEqual(evaluate("3! * 2!"), 12)


class TestConstants(unittest.TestCase):
    """pi and Euler's e."""

    def test_pi(self):
        self.assertAlmostEqual(evaluate("pi"), math.pi)

    def test_pi_in_expr(self):
        self.assertAlmostEqual(evaluate("pi * 2"), math.pi * 2)

    def test_euler(self):
        self.assertAlmostEqual(evaluate("e"), math.e)

    def test_e_in_expr(self):
        self.assertAlmostEqual(evaluate("e * 2"), math.e * 2)


class TestAns(unittest.TestCase):
    """The ans (last answer) memory."""

    def test_ans_works(self):
        self.assertEqual(evaluate("ans", ans_value=42), 42)

    def test_ans_in_expr(self):
        self.assertEqual(evaluate("ans + 8", ans_value=10), 18)

    def test_ans_no_value(self):
        self.assertIsNone(evaluate("ans"))

    def test_invalid_chars_with_ans(self):
        self.assertEqual(evaluate("ans", ans_value=5), 5)


class TestDisplaySymbols(unittest.TestCase):
    """Conversion of display symbols (× ÷ − π)."""

    def test_times(self):
        self.assertEqual(evaluate("2 × 3"), 6)

    def test_divide(self):
        self.assertEqual(evaluate("10 ÷ 2"), 5.0)

    def test_minus(self):
        self.assertEqual(evaluate("5 − 3"), 2)

    def test_pi(self):
        self.assertAlmostEqual(evaluate("π"), math.pi)

    def test_pi_in_expr(self):
        self.assertAlmostEqual(evaluate("π * 2"), math.pi * 2)


class TestInputValidation(unittest.TestCase):
    """Safety and validation."""

    def test_invalid_chars(self):
        self.assertIsNone(evaluate("2 + abc"))

    def test_syntax_error(self):
        self.assertIsNone(evaluate("2 +* 3"))

    def test_mismatched_parens(self):
        self.assertIsNone(evaluate("(2 + 3"))

    def test_empty_op(self):
        self.assertIsNone(evaluate("2 + "))

    def test_double_op(self):
        result = evaluate("2 + - 3")
        self.assertIsNotNone(result)

    def test_only_op(self):
        self.assertIsNone(evaluate("+"))


class TestFormatResult(unittest.TestCase):
    """Result formatting."""

    def test_int(self):
        self.assertEqual(format_result(5), "5")

    def test_float(self):
        self.assertEqual(format_result(3.5), "3.5")

    def test_large_int(self):
        self.assertEqual(format_result(10000000000), "10000000000")

    def test_large_float(self):
        self.assertEqual(format_result(12345678901.0), "12345678901")

    def test_small_float(self):
        self.assertEqual(format_result(0.0000000001), "0.0000000001")

    def test_inf(self):
        self.assertEqual(format_result(float("inf")), "Error")

    def test_nan(self):
        self.assertEqual(format_result(float("nan")), "Error")

    def test_float_cleanup(self):
        self.assertEqual(format_result(2.0), "2")


class TestEdgeCases(unittest.TestCase):
    """Edge cases and combinations."""

    def test_complex_expression(self):
        self.assertAlmostEqual(evaluate("sqrt(3 ^ 2 + 4 ^ 2)"), 5)

    def test_nested_parens(self):
        self.assertEqual(evaluate("((2 + 3) * (4 - 1))"), 15)

    def test_negation(self):
        self.assertEqual(evaluate("-5 + 10"), 5)

    def test_multiple_ops(self):
        self.assertEqual(evaluate("2 + 3 + 4 + 5"), 14)

    def test_sqrt_decimal(self):
        self.assertAlmostEqual(evaluate("sqrt(2)"), math.sqrt(2), places=10)

    def test_pi_constant(self):
        self.assertAlmostEqual(evaluate("pi"), math.pi)

    def test_euler_constant(self):
        self.assertAlmostEqual(evaluate("euler"), math.e)

    def test_combined_trig(self):
        self.assertAlmostEqual(
            evaluate("sin(pi / 4) ^ 2 + cos(pi / 4) ^ 2"),
            1, places=10,
        )


if __name__ == "__main__":
    unittest.main()
