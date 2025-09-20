OP = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "/": lambda a, b: a // b,
    "*": lambda a, b: a * b,
}


def calc(expr: str) -> list:
    stack = []
    for token in expr.split():
        token = token.replace("~", "-")
        if token.replace("-", "").isdigit():
            stack.append(int(token))
        elif token in OP.keys():
            stack.append(OP[token](stack.pop(), stack.pop()))
    return stack


def main():
    print(calc("3 4 6 + *"))


if __name__ == "__main__":
    main()
