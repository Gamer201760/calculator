from domain import Expression


OP = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: b - a,
    "/": lambda a, b: b / a,
    "*": lambda a, b: a * b,
}


def calc(expr: str) -> list:
    stack = []
    for token in expr.split():
        token = token.replace("~", "-")
        if token.replace("-", "").isdigit():
            stack.append(float(token))
        elif token in OP.keys():
            stack.append(OP[token](stack.pop(), stack.pop()))
        else:
            raise SyntaxError("Unknown operatioan")
    return stack


def main():
    expr = "~3 4 6 + *"
    print(calc(expr))
    new_expr = Expression(expr.split())
    print(new_expr.evaluate())


if __name__ == "__main__":
    main()
