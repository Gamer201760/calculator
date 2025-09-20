def calc(expr: str) -> list:
    stack = []
    for x in expr.split():
        if x.isdigit():
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
    print(calc("2 2 2 + /"))


if __name__ == "__main__":
    main()
