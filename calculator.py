#!/usr/bin/env python3
"""Scientific calculator engine — supports trig, log, exp, factorial, and more."""

import math
import re
import sys
from typing import Optional

# Expression evaluation
# Tokens safe to strip during character validation (longest first to avoid
# partial matches like "sin" inside "asin")
_SAFE_TOKENS = (
    "factorial", "log10", "sqrt", "asin", "acos", "atan",
    "sin", "cos", "tan", "log", "ln", "exp",
    "euler", "ans", "pi", "**",
)

# Characters allowed in raw expression input
_ALLOWED_CHARS = set("0123456789.+-*/%() ")


def evaluate(
    expression: str,
    deg_mode: bool = False,
    ans_value: Optional[float] = None,
) -> Optional[float]:
    """Evaluate a mathematical expression safely.

    Parameters
    ----------
    expression : str
        The expression string to evaluate.
    deg_mode : bool
        If True, trig functions expect degrees; inverse trig return degrees.
    ans_value : float or None
        The value to substitute for ``ans``. If ``None`` and the expression
        contains ``ans``, the evaluation fails.

    Returns
    -------
    float or None
        The computed result, or ``None`` on error.
    """
    if not expression or not expression.strip():
        return None

    expr = expression.strip()

    #  Preprocessing

    # Display symbols → Python operators
    expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
    expr = expr.replace("π", "pi")

    # Caret → Python exponent
    expr = expr.replace("^", "**")

    # Factorial notation:  5!  →  factorial(5)
    expr = re.sub(r"(\d+)!", lambda m: f"factorial({m.group(1)})", expr)

    # Standalone e → Euler's number constant  (not inside words like "exp")
    expr = re.sub(r"(?<!\w)e(?!\w)", "euler", expr)

    # Substitute ans with the stored previous answer
    if "ans" in expr:
        if ans_value is None:
            return None
        expr = re.sub(r"\bans\b", str(ans_value), expr)

    # Character validation 

    cleaned = expr
    for tok in _SAFE_TOKENS:
        cleaned = cleaned.replace(tok, "")
    if not all(c in _ALLOWED_CHARS for c in cleaned):
        return None

    #  Build namespace 

    ns: dict = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "log10": math.log10,
        "log": math.log10,
        "ln": math.log,
        "exp": math.exp,
        "factorial": math.factorial,
        "pi": math.pi,
        "euler": math.e,
    }

    if deg_mode:
        ns["sin"] = lambda x: math.sin(math.radians(x))
        ns["cos"] = lambda x: math.cos(math.radians(x))
        ns["tan"] = lambda x: math.tan(math.radians(x))
        ns["asin"] = lambda x: math.degrees(math.asin(x))
        ns["acos"] = lambda x: math.degrees(math.acos(x))
        ns["atan"] = lambda x: math.degrees(math.atan(x))

    #  Evaluation 

    try:
        result = eval(expr, {"__builtins__": {}}, ns)
        if isinstance(result, (int, float)):
            return float(result)
        return None
    except (SyntaxError, ZeroDivisionError, TypeError, OverflowError, ValueError):
        return None


# Result formatting
def format_result(value: float) -> str:
    """Format a numeric result for display."""
    if math.isinf(value) or math.isnan(value):
        return "Error"
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    if abs(value) > 1e10 or (abs(value) < 1e-10 and value != 0):
        return f"{value:.10e}"
    return f"{value:.10f}".rstrip("0").rstrip(".")


# CLI REPL
def main():
    """Interactive REPL for the scientific calculator."""
    print("=" * 52)
    print("  Scientific Calculator  (deg/rad toggles mode, exit to quit)")
    print("=" * 52)

    ans_value: Optional[float] = None
    deg_mode = True

    while True:
        try:
            prompt = f"{'D' if deg_mode else 'R'} ans = " if ans_value is not None else f"{'D' if deg_mode else 'R'} > "
            expr = input(prompt).strip()

            if expr.lower() in ("exit", "q", "quit"):
                print("Goodbye!")
                sys.exit(0)

            if expr.lower() == "clear":
                ans_value = None
                print("Cleared.")
                continue

            if expr.lower() == "deg":
                deg_mode = True
                print("Degree mode")
                continue

            if expr.lower() == "rad":
                deg_mode = False
                print("Radian mode")
                continue

            if not expr:
                continue

            result = evaluate(expr, deg_mode=deg_mode, ans_value=ans_value)
            if result is None:
                print("Error")
                continue

            ans_value = result
            print(f"= {format_result(result)}")

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
