# Scientific Calculator

A fully-featured scientific calculator with a terminal REPL and a graphical user interface (tkinter), inspired by Windows Calculator scientific mode.

## Features

### Basic arithmetic
Addition, subtraction, multiplication, division, modulo — with full PEMDAS and parentheses support.

### Scientific functions

| Category | Functions |
|---|---|
| **Trigonometry** | `sin`, `cos`, `tan` — works in either degree or radian mode |
| **Inverse trig** | `asin`, `acos`, `atan` — returns angle in current mode |
| **Logarithms** | `log` (base 10), `ln` (natural log) |
| **Exponential** | `exp` (eˣ) |
| **Power / root** | `x^y` via `^` / `**`, `sqrt`, `x²`, `x³`, `10ˣ` |
| **Factorial** | `n!` notation (e.g., `5!` → `120`) |
| **Constants** | `pi` (π), `e` (Euler's number) |
| **Memory** | `ans` stores the last result automatically |

### Angle mode
Toggle between **DEG** (trig functions expect degrees) and **RAD** (trig functions expect radians).

### GUI features
- **Two-line display** — expression shown above, result below
- **Calculation history** — side panel lists all completed calculations
- **Memory functions** — MC (clear), MR (recall), M+ (add), M− (subtract), MS (store)
- **Keyboard support** — digits, operators, `Enter` (=), `Backspace` (⌫), `Escape` (C)
- **Error handling** — displays "Error" for invalid expressions, division by zero, etc.
- **Dark theme** — navy/dark colour scheme with accent buttons

## Usage

### Terminal REPL

```bash
python3 calculator.py
```

```
  Scientific Calculator  (deg/rad toggles mode, exit to quit)
D > sin(45)
= 0.7071067812
D > ans ^ 2
= 0.5
D > rad
Radian mode
R > cos(pi)
= -1
R > 5!
= 120
```

#### REPL Commands

| Command | Action |
|---|---|
| `exit`, `q`, `quit` | Exit the calculator |
| `clear` | Reset stored answer |
| `deg` | Switch to degree mode |
| `rad` | Switch to radian mode |

### GUI

```bash
python3 gui.py
```

```text
┌──────────────────────────────────────────────────────┐
│  DEG [●]  RAD [○]           ┌─ History ──────────────┐
│  MC  MR  M+  M−  MS         │ sin(45) = 0.707...     │
├─────────────────────────    │ 5! = 120               │
│  sin(45)                    │ 2^10 = 1024            │
│  = 0.7071067812             │                        │
├──────────────────────       │                        │
│ (  )  C   ⌫   ÷          
│ sin cos tan ^   ×           │                        │
│ asin acos atan √  −         │                        │
│ ln  log exp  π  +           │                        │
│ x²  x³  10ˣ  n!  =          │                        │
│ 7   8   9   ±  ans          │                        │
│ 4   5   6                   │                        │
│ 1   2   3                   │                        │
│ 0      .                    │                        │
└─────────────────────────────┴────────────────────────┘
```

## Project Structure

```
calculator/
├── calculator.py        # Evaluation engine (+ optional CLI REPL)
├── gui.py               # tkinter GUI
├── test_calculator.py   # Unit tests (79 tests)
└── README.md
```

## Architecture

The application is split into two independent front-ends sharing a common engine:

### `calculator.py` — Engine
- **`evaluate(expression, deg_mode, ans_value)`** — sandboxed expression evaluator using `eval()` with builtins disabled. Only explicitly allowed math functions are exposed in the namespace.
- **`format_result(value)`** — formats floats cleanly (no trailing zeros, integers without decimals, scientific notation for extreme values).
- **`main()`** — optional CLI REPL with commands for mode toggling.

The evaluator preprocesses the expression (symbol conversion, factorial notation, constant substitution), validates characters against a whitelist, then evaluates in a restricted namespace.

### `gui.py` — GUI
Built with tkinter, the `ScientificCalculator` class manages all state (expression, memory, history, angle mode) and delegates computation to `calculator.evaluate()`.

## Running Tests

```bash
python3 -m unittest test_calculator.py -v
```
