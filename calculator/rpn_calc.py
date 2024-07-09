import re
from collections.abc import Iterator
from operator import add, mul, sub, truediv


def extract(formula: str):
    pattern = (
        r"^-(\d+\.|\.|)\d+",
        r"(?<=[-+*/(])-(\d+\.|\.|)\d+",
        r"(\d+\.|\.|)\d+",
        r"[-+*/%()]",
    )
    finditer = re.finditer("|".join(pattern), formula)
    return finditer


def str_or_float_convert(string: str):
    token: float | str
    try:
        token = float(string)
        if token.is_integer():
            token = int(token)
    except ValueError:
        token = string
    return token


def to_postfix(tokens: Iterator[re.Match[str]]):
    priority = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 3}
    bracket_multiply_stack: list[bool] = []
    stack = []
    queue: list[float | str] = []
    prev_token = None
    for token in tokens:
        token = str_or_float_convert(token.group())
        # 演算記号のとき
        if token in priority:
            while (
                stack
                and stack[-1] not in ("(", ")")
                and priority[stack[-1]] >= priority[token]
            ):
                queue.append(stack.pop())
            stack.append(token)
        # 括弧のとき
        elif token == "(":
            stack.append(token)
            # 隠し掛け算を考慮する 2(-3)など
            if queue and (prev_token == ")" or isinstance(prev_token, (float, int))):
                bracket_multiply_stack.append(True)
            else:
                bracket_multiply_stack.append(False)
        elif token == ")":
            while stack[-1] != "(":
                queue.append(stack.pop())
            stack.pop()
            if bracket_multiply_stack[-1]:
                queue.append("*")
            bracket_multiply_stack.pop()
        # 数字のとき
        else:
            queue.append(token)
        prev_token = token
    # 残っている記号をqueueに追加
    if stack:
        for token in stack[::-1]:
            # 閉じられていない括弧がある場合
            if token == "(":
                if bracket_multiply_stack[-1]:
                    queue.append("*")
                bracket_multiply_stack.pop()
            else:
                queue.append(token)
    return queue


def postfix_calc(tokens: list[float | str]):
    operator = {
        "+": add,
        "-": sub,
        "*": mul,
        "/": truediv,
    }
    output: list[float] = []
    for i, token in enumerate(tokens):
        # 記号のとき
        if isinstance(token, str):
            if token == "%":
                if len(output) >= 2:
                    num1, num2 = output[-2:]
                    result = num2 / 100
                    if tokens[i + 1] in ("+", "-"):
                        result *= num1
                    output[-1] = result
                else:
                    num = output[-1]
                    result = num / 100
                    output[-1] = result
            else:
                num1, num2 = output[-2:]
                result = operator[token](num1, num2)
                output[-2:] = [result]
        # 数字のとき
        else:
            output.append(token)
    if len(output) != 1:
        raise ValueError(f"答えが定まっていない: {output}")
    return output[0]


def run(formula: str):
    out = extract(formula=formula)
    out = to_postfix(tokens=out)
    if len(out) == 0:
        return None
    out = postfix_calc(tokens=out)
    return out
