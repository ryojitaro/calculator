import re
import tkinter as tk
from itertools import product
from tkinter import ttk
from typing import Callable

from rpn_calc import run


class Button:
    def __init__(self, text: str, func: Callable, colspan=1):
        self.text = text
        self.func = func
        self.colspan = colspan


class Calclator:
    def __init__(self):
        root = tk.Tk()
        root.title("電卓")
        root.geometry("240x360")
        root.minsize(width=240, height=360)

        self.formula_var = tk.StringVar(root)
        self.formula_var.trace_add("write", lambda s1, s2, s3: self.calc())
        self.result = tk.StringVar(root)

        input_label = ttk.Label(root, font="Meiryo 12", text="計算式")
        input_label.pack(padx=4, pady=4, anchor=tk.E)
        self.input_entry = ttk.Entry(
            root, font="Calibri 16", justify=tk.RIGHT, textvariable=self.formula_var
        )
        self.input_entry.pack(padx=4, fill=tk.BOTH)

        output_label = ttk.Label(root, font="Meiryo 12", text="結果")
        output_label.pack(padx=4, anchor=tk.E)
        output_entry = ttk.Entry(
            root,
            font="Calibri 16",
            justify=tk.RIGHT,
            state="readonly",
            textvariable=self.result,
        )
        output_entry.pack(padx=4, pady=4, fill=tk.BOTH)

        frm = tk.Frame(root)
        frm.pack(fill="both", expand=1)
        frm.rowconfigure((0, 1, 2, 3, 4), weight=1)
        frm.columnconfigure((0, 1, 2, 3), weight=1)

        button_rayout: list[list[Button | None]] = [
            [
                Button(text="AC", func=self.all_clear_handler),
                Button(text="()", func=self.bracket_handler),
                Button(text="%", func=self.input_formula_handler("%")),
                Button(text="BS", func=self.back_space_handler),
            ],
            [
                Button(text="7", func=self.input_formula_handler("7")),
                Button(text="8", func=self.input_formula_handler("8")),
                Button(text="9", func=self.input_formula_handler("9")),
                Button(text="/", func=self.input_formula_handler("/")),
            ],
            [
                Button(text="4", func=self.input_formula_handler("4")),
                Button(text="5", func=self.input_formula_handler("5")),
                Button(text="6", func=self.input_formula_handler("6")),
                Button(text="*", func=self.input_formula_handler("*")),
            ],
            [
                Button(text="1", func=self.input_formula_handler("1")),
                Button(text="2", func=self.input_formula_handler("2")),
                Button(text="3", func=self.input_formula_handler("3")),
                Button(text="-", func=self.input_formula_handler("-")),
            ],
            [
                Button(text="0", func=self.input_formula_handler("0"), colspan=2),
                None,
                Button(text=".", func=self.input_formula_handler(".")),
                Button(text="+", func=self.input_formula_handler("+")),
            ],
        ]

        ttk.Style().configure("TButton", font=("Calibri", 16))
        for row, col in product(range(len(button_rayout)), range(4)):
            button_elem = button_rayout[row][col]
            if button_elem is None:
                continue
            button = ttk.Button(frm, text=button_elem.text, command=button_elem.func)
            button.grid(
                row=row,
                column=col,
                columnspan=button_elem.colspan,
                sticky="nsew",
            )

        self.input_entry.focus_set()
        root.mainloop()

    def input_formula_handler(self, char: str):
        def set_var():
            formula = self.formula_var.get()
            cursor = self.input_entry.index(tk.INSERT)
            self.formula_var.set(formula[:cursor] + char + formula[cursor:])
            self.input_entry.icursor(cursor + 1)
            self.input_entry.focus_set()

        return set_var

    def all_clear_handler(self):
        self.formula_var.set("")
        self.result.set("")
        self.input_entry.focus_set()

    def back_space_handler(self):
        formula = self.formula_var.get()
        cursor = self.input_entry.index(tk.INSERT)
        if cursor > 0:
            self.formula_var.set(formula[: cursor - 1] + formula[cursor:])
            self.input_entry.icursor(max(0, cursor - 1))
        self.input_entry.focus_set()

    def bracket_handler(self):
        formula_var = self.formula_var.get()
        open_brackets = 0

        open_brackets += formula_var.count("(")
        open_brackets -= formula_var.count(")")

        # 閉じられていない括弧があるとき
        if open_brackets > 0:
            last_open_bracket = formula_var.rindex("(")
            # 最右の開き括弧の後になにか情報があるとき
            if len(formula_var[last_open_bracket + 1 :].replace(")", "").strip()) == 0:
                bracket = "("
            else:
                bracket = ")"
        else:
            bracket = "("

        self.input_formula_handler(bracket)()

    def calc(self):
        out = ""
        formula = self.formula_var.get()
        if formula == "":
            self.result.set("")
            return None
        try:
            if (
                len(re.findall(r"\d+", formula)) == 0
                or re.search(r"\.\d\.|[^\d%)]$", formula) is not None
            ):
                raise ValueError("不正文字列")
            out = run(formula)
        except (ValueError, ZeroDivisionError) as e:
            out = "( ˘ω˘ ) ?"
            print(e)
        else:
            out = "" if out is None else str(out)
        finally:
            self.result.set(out)


Calclator()
