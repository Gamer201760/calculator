def calc(expr: str) -> list:
    stack = []
    for x in expr.split():
        x = x.replace("~", "-")
        if x.replace("-", "").isdigit():
            stack.append(int(x))
        elif x == "+":
            stack.append(stack.pop() + stack.pop())
        elif x == "-":
            stack.append(stack.pop() - stack.pop())
        elif x == "*":
            stack.append(stack.pop() * stack.pop())
        elif x == "/":
            stack.append(stack.pop() // stack.pop())
    return stack


def main():
    print(calc("~3 4 6 + *"))


if __name__ == "__main__":
    main()
