#!/usr/bin/env python3
"""Scientific calculator GUI — inspired by Windows Calculator scientific mode."""

import tkinter as tk
from tkinter import font as tkfont
from calculator import evaluate, format_result


# Colour palette 
class Theme:
    BG = "#1a1a2e"
    DISPLAY_BG = "#0f1626"
    BTN = "#16213e"
    BTN_HOVER = "#1c2a4f"
    BTN_NUM = "#0f3460"
    BTN_NUM_HOVER = "#144a7a"
    BTN_OP = "#533483"
    BTN_OP_HOVER = "#6a42a0"
    BTN_FN = "#1a3a5c"
    BTN_FN_HOVER = "#22507a"
    BTN_EQ = "#e94560"
    BTN_EQ_HOVER = "#ff5a75"
    BTN_MEM = "#2d1b4e"
    BTN_MEM_HOVER = "#3d2570"
    FG = "#eaeaea"
    FG_SECONDARY = "#8a9bb5"
    FG_ACCENT = "#ffffff"
    HISTORY_BG = "#12122a"
    HISTORY_BORDER = "#2a2a4a"
    ACTIVE = "#e94560"


class ScientificCalculator:
    """Full scientific calculator with history and memory."""

    TITLE = "Scientific Calculator"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(self.TITLE)
        self.root.resizable(False, False)
        self.root.configure(bg=Theme.BG)

        #  State 
        self.expression = ""
        self.new_number = True
        self.just_calculated = False
        self.deg_mode = True
        self.memory: float = 0.0
        self.has_memory = False
        self.ans_value: float | None = None
        self.last_expression = ""
        self.history: list[tuple[str, str]] = []
        self._skip_next_display_update = False

        self._build_styles()
        self._build_layout()
        self._bind_keys()

    # Styles 
    def _build_styles(self):
        self.font_expr = tkfont.Font(family="Segoe UI", size=13)
        self.font_result = tkfont.Font(family="Segoe UI", size=30, weight="bold")
        self.font_btn = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.font_fn = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.font_mem = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.font_history = tkfont.Font(family="Segoe UI", size=10)

    #Layout 
    def _build_layout(self):
        container = tk.Frame(self.root, bg=Theme.BG)
        container.pack(fill="both", expand=True)

        # Left: display + buttons
        left = tk.Frame(container, bg=Theme.BG)
        left.pack(side="left", fill="both")

        # Right: history panel
        right = tk.Frame(container, bg=Theme.HISTORY_BG, width=200)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self._build_display(left)
        self._build_memory_row(left)
        self._build_angle_row(left)
        self._build_buttons(left)
        self._build_history(right)

    # Display 
    def _build_display(self, parent):
        frame = tk.Frame(parent, bg=Theme.DISPLAY_BG, height=100)
        frame.pack(fill="x", padx=4, pady=(4, 0))
        frame.pack_propagate(False)

        self.expr_var = tk.StringVar(value="")
        tk.Label(
            frame,
            textvariable=self.expr_var,
            font=self.font_expr,
            bg=Theme.DISPLAY_BG,
            fg=Theme.FG_SECONDARY,
            anchor="e",
        ).pack(fill="x", padx=16, pady=(8, 0))

        self.result_var = tk.StringVar(value="0")
        tk.Label(
            frame,
            textvariable=self.result_var,
            font=self.font_result,
            bg=Theme.DISPLAY_BG,
            fg=Theme.FG,
            anchor="e",
        ).pack(fill="x", padx=16, pady=(0, 8))

    # ── Memory row ───────────────────────────────────────────────────────
    def _build_memory_row(self, parent):
        frame = tk.Frame(parent, bg=Theme.BG)
        frame.pack(fill="x", padx=4, pady=(4, 0))

        mem_actions = [
            ("MC", self._mem_clear),
            ("MR", self._mem_recall),
            ("M+", self._mem_add),
            ("M−", self._mem_sub),
            ("MS", self._mem_store),
        ]
        for text, cmd in mem_actions:
            self._make_btn(frame, text, cmd, Theme.BTN_MEM, self.font_mem,
                           width=4, side="left", padx=1)

    # Angle row 
    def _build_angle_row(self, parent):
        frame = tk.Frame(parent, bg=Theme.BG)
        frame.pack(fill="x", padx=4, pady=(2, 0))

        self.deg_btn = self._make_btn(
            frame, "DEG", self._toggle_deg, Theme.ACTIVE, self.font_mem,
            width=4, side="left", padx=1,
        )
        self.rad_btn = self._make_btn(
            frame, "RAD", self._toggle_rad, Theme.BTN_MEM, self.font_mem,
            width=4, side="left", padx=1,
        )

    #  Buttons 
    def _make_btn(self, parent, text, cmd, bg, fnt,
                  width=None, side=None, padx=0, expand=False, row=None, col=None,
                  colspan=1, rowspan=1):
        btn = tk.Button(
            parent,
            text=text,
            font=fnt,
            bg=bg,
            fg=Theme.FG,
            activebackground=bg,
            activeforeground=Theme.FG,
            relief="flat",
            bd=0,
            padx=6,
            pady=4,
            cursor="hand2",
            command=cmd,
            width=width,
        )
        if side:
            btn.pack(side=side, padx=padx, expand=expand, fill="x")
        if row is not None:
            btn.grid(
                row=row, column=col, columnspan=colspan, rowspan=rowspan,
                sticky="nsew", padx=1, pady=1,
            )
        return btn

    def _build_buttons(self, parent):
        grid = tk.Frame(parent, bg=Theme.BG)
        grid.pack(padx=4, pady=(2, 4))

        # 5 columns, equal weight
        for c in range(5):
            grid.columnconfigure(c, weight=1)

        # Button definitions: (text, row, col, bg_style, cmd, colspan)
        buttons: list[tuple] = []

        def fn(text, r, c, cmd=None, colsp=1):
            return (text, r, c, "fn", cmd, colsp)

        def op(text, r, c, cmd=None, colsp=1):
            return (text, r, c, "op", cmd, colsp)

        def num(text, r, c, cmd=None, colsp=1):
            return (text, r, c, "num", cmd, colsp)

        def eq(text, r, c, cmd=None, colsp=1):
            return (text, r, c, "eq", cmd, colsp)

        def sp(text, r, c, cmd=None, colsp=1):
            return (text, r, c, "sp", cmd, colsp)

        # Row 0: (  )  C  ⌫  ÷
        buttons += [
            sp("(", 0, 0, lambda: self._insert("(")),
            sp(")", 0, 1, lambda: self._insert(")")),
            sp("C", 0, 2, self.clear, colsp=1),
            sp("⌫", 0, 3, self.backspace),
            op("÷", 0, 4, lambda: self._insert_op("/")),
        ]

        # Row 1: sin  cos  tan  ^  ×
        buttons += [
            fn("sin", 1, 0, lambda: self._insert_fn("sin(")),
            fn("cos", 1, 1, lambda: self._insert_fn("cos(")),
            fn("tan", 1, 2, lambda: self._insert_fn("tan(")),
            op("^", 1, 3, lambda: self._insert_op("^")),
            op("×", 1, 4, lambda: self._insert_op("*")),
        ]

        # Row 2: asin  acos  atan  √  −
        buttons += [
            fn("asin", 2, 0, lambda: self._insert_fn("asin(")),
            fn("acos", 2, 1, lambda: self._insert_fn("acos(")),
            fn("atan", 2, 2, lambda: self._insert_fn("atan(")),
            fn("√", 2, 3, lambda: self._insert_fn("sqrt(")),
            op("−", 2, 4, lambda: self._insert_op("-")),
        ]

        # Row 3: ln  log  exp  π  +
        buttons += [
            fn("ln", 3, 0, lambda: self._insert_fn("ln(")),
            fn("log", 3, 1, lambda: self._insert_fn("log(")),
            fn("exp", 3, 2, lambda: self._insert_fn("exp(")),
            fn("π", 3, 3, lambda: self._insert("π")),
            op("+", 3, 4, lambda: self._insert_op("+")),
        ]

        # Row 4: x²  x³  10ˣ  n!  =
        buttons += [
            fn("x²", 4, 0, lambda: self._insert_op("^2")),
            fn("x³", 4, 1, lambda: self._insert_op("^3")),
            fn("10ˣ", 4, 2, lambda: self._insert_fn("10^")),
            fn("n!", 4, 3, lambda: self._insert("!")),
            eq("=", 4, 4, self._calculate),
        ]

        # Row 5: 7  8  9  ± ans
        buttons += [
            num("7", 5, 0, lambda: self._press_num("7")),
            num("8", 5, 1, lambda: self._press_num("8")),
            num("9", 5, 2, lambda: self._press_num("9")),
            fn("±", 5, 3, self._negate),
            fn("ans", 5, 4, lambda: self._insert("ans")),
        ]

        # Row 6: 4  5  6
        buttons += [
            num("4", 6, 0, lambda: self._press_num("4")),
            num("5", 6, 1, lambda: self._press_num("5")),
            num("6", 6, 2, lambda: self._press_num("6")),
        ]

        # Row 7: 1  2  3
        buttons += [
            num("1", 7, 0, lambda: self._press_num("1")),
            num("2", 7, 1, lambda: self._press_num("2")),
            num("3", 7, 2, lambda: self._press_num("3")),
        ]

        # Row 8: 0 (span2)  .
        buttons += [
            num("0", 8, 0, lambda: self._press_num("0"), 2),
            num(".", 8, 2, self._press_dot),
        ]

        # Map bg styles to actual colours
        bg_map = {
            "fn": (Theme.BTN_FN, Theme.BTN_FN_HOVER),
            "op": (Theme.BTN_OP, Theme.BTN_OP_HOVER),
            "num": (Theme.BTN_NUM, Theme.BTN_NUM_HOVER),
            "eq": (Theme.BTN_EQ, Theme.BTN_EQ_HOVER),
            "sp": (Theme.BTN, Theme.BTN_HOVER),
        }

        for text, r, c, style, cmd, colsp in buttons:
            bg, _ = bg_map[style]
            fnt = self.font_fn if style == "fn" else (
                self.font_mem if style == "sp" else self.font_btn)
            self._make_btn(grid, text, cmd, bg, fnt,
                           row=r, col=c, colspan=colsp)

    #  History panel 
    def _build_history(self, parent):
        tk.Label(
            parent, text="History", font=self.font_mem,
            bg=Theme.HISTORY_BG, fg=Theme.FG_SECONDARY,
            anchor="w", padx=10, pady=6,
        ).pack(fill="x")

        frame = tk.Frame(parent, bg=Theme.HISTORY_BG)
        frame.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        self.history_listbox = tk.Listbox(
            frame,
            font=self.font_history,
            bg=Theme.HISTORY_BG,
            fg=Theme.FG_SECONDARY,
            selectbackground=Theme.BTN,
            selectforeground=Theme.FG,
            relief="flat",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            activestyle="none",
        )
        scrollbar.config(command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.pack(side="left", fill="both", expand=True)

        tk.Button(
            parent, text="Clear History", font=self.font_mem,
            bg=Theme.BTN, fg=Theme.FG_SECONDARY,
            activebackground=Theme.BTN_HOVER, activeforeground=Theme.FG,
            relief="flat", bd=0, padx=6, pady=4, cursor="hand2",
            command=self._clear_history,
        ).pack(fill="x", padx=4, pady=(0, 4))

    # Input handlers 
    def _press_num(self, digit: str):
        if self.just_calculated:
            self.expression = ""
            self.just_calculated = False
            self.new_number = True
        if self.new_number:
            self.expression = ""
            self.new_number = False
        self.expression += digit
        self._update_display()

    def _press_dot(self):
        if self.just_calculated:
            self.expression = "0"
            self.just_calculated = False
            self.new_number = False
            self._update_display()
            return
        if self.new_number:
            self.expression = "0"
            self.new_number = False
        self.expression += "."
        self._update_display()

    def _insert(self, text: str):
        """Insert text directly into the expression."""
        if self.just_calculated:
            self.expression = ""
            self.just_calculated = False
        self.new_number = False
        self.expression += text
        self._update_display()

    def _insert_op(self, op: str):
        """Insert an operator."""
        if self.just_calculated and op in ("^2", "^3"):
            self.expression += op
            self.just_calculated = False
            self.new_number = False
            self._update_display()
            return
        if self.just_calculated:
            self.just_calculated = False
            self.new_number = False
        self.expression += op
        self.new_number = False
        self._update_display()

    def _insert_fn(self, fn: str):
        """Insert a function name (starts a new number after)."""
        if self.just_calculated:
            self.expression = ""
            self.just_calculated = False
        self.expression += fn
        self.new_number = False
        self._update_display()

    def _negate(self):
        if not self.expression or self.expression == "0":
            self.expression = "-"
            self._update_display()
            return
        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        else:
            self.expression = f"-({self.expression})"
        self._update_display()

    def backspace(self):
        if self.just_calculated:
            return
        self.expression = self.expression[:-1]
        if not self.expression:
            self.expression = ""
            self.new_number = True
        self._update_display()

    def clear(self):
        self.expression = ""
        self.new_number = True
        self.just_calculated = False
        self._update_display()

    def _calculate(self):
        if not self.expression:
            return
        raw_expr = self.expression
        try:
            result = evaluate(self.expression, deg_mode=self.deg_mode,
                              ans_value=self.ans_value)
            if result is None:
                self.result_var.set("Error")
                self.expression = ""
                self.new_number = True
                self.just_calculated = True
            else:
                formatted = format_result(result)
                self.result_var.set(formatted)
                self.ans_value = result
                self.just_calculated = True
                self.new_number = True
                self._add_history(raw_expr, formatted)
        except Exception:
            self.result_var.set("Error")
            self.expression = ""
            self.new_number = True
            self.just_calculated = True

    # Display helper 
    def _display_text(self, expr: str) -> str:
        """Convert internal expression to display-friendly text."""
        text = expr
        text = text.replace("**", "^")
        text = text.replace("*", "×")
        text = text.replace("/", "÷")
        text = text.replace("-", "−")
        text = text.replace("pi", "π")
        text = text.replace("sqrt(", "√(")
        return text

    def _update_display(self):
        if self._skip_next_display_update:
            self._skip_next_display_update = False
            return
        if self.just_calculated:
            self.expr_var.set(self._display_text(self.last_expression))
        else:
            self.expr_var.set(self._display_text(self.expression))
            self.result_var.set(self.expression if self.expression else "0")

    # Angle toggle 
    def _toggle_deg(self):
        self.deg_mode = True
        self.deg_btn.configure(bg=Theme.ACTIVE)
        self.rad_btn.configure(bg=Theme.BTN_MEM)

    def _toggle_rad(self):
        self.deg_mode = False
        self.rad_btn.configure(bg=Theme.ACTIVE)
        self.deg_btn.configure(bg=Theme.BTN_MEM)

    # Memory functions 
    def _evaluate_current(self) -> float | None:
        """Evaluate the current expression and return the result."""
        if not self.expression:
            return None
        try:
            return evaluate(self.expression, deg_mode=self.deg_mode,
                            ans_value=self.ans_value)
        except Exception:
            return None

    def _mem_clear(self):
        self.memory = 0.0
        self.has_memory = False

    def _mem_recall(self):
        if self.has_memory:
            self._insert(str(self.memory))

    def _mem_add(self):
        val = self._evaluate_current()
        if val is not None:
            self.memory += val
            self.has_memory = True

    def _mem_sub(self):
        val = self._evaluate_current()
        if val is not None:
            self.memory -= val
            self.has_memory = True

    def _mem_store(self):
        val = self._evaluate_current()
        if val is not None:
            self.memory = val
            self.has_memory = True

    # History
    def _add_history(self, expression: str, result: str):
        display = self._display_text(expression)
        self.history.append((display, result))
        self.history_listbox.insert(tk.END, f"{display} = {result}")
        self.history_listbox.see(tk.END)
        # Store the expression for the display
        self.last_expression = expression
        self._update_display()

    def _clear_history(self):
        self.history.clear()
        self.history_listbox.delete(0, tk.END)

    #  Keyboard bindings 
    def _bind_keys(self):
        self.root.bind("<Key>", self._key_press)
        self.root.bind("<Return>", lambda _: self._calculate())
        self.root.bind("<BackSpace>", lambda _: self.backspace())
        self.root.bind("<Escape>", lambda _: self.clear())

    def _key_press(self, event):
        ch = event.char
        if ch.isdigit():
            self._press_num(ch)
        elif ch == ".":
            self._press_dot()
        elif ch in "+-*/%":
            op_map = {"+": "+", "-": "-", "*": "*", "/": "/", "%": "%"}
            self._insert_op(op_map[ch])
        elif ch == "^":
            self._insert_op("^")
        elif ch == "(" or ch == ")":
            self._insert(ch)
        elif ch.lower() == "c":
            self.clear()

    #  Entry point 
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ScientificCalculator().run()
