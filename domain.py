class Token:
    def __init__(self, tok: str) -> None:
        self.tok = tok

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tok})"


class Num(Token):
    def value(self) -> float:
        return float(self.tok)


class Op(Token):
    _OPS = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: b - a,
        "*": lambda a, b: a * b,
        "/": lambda a, b: b / a,
    }

    def __init__(self, tok: str) -> None:
        if tok not in self._OPS:
            raise ValueError(f"Unknown operator: {tok}")
        super().__init__(tok)

    def apply(self, a: float, b: float) -> float:
        return self._OPS[self.tok](a, b)


class Expression:
    """
    Принимает список токенов в польской (RPN) форме,
    и при итерации создаёт соответствующие объекты Token.
    """

    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens

    def __iter__(self):
        for tok in self.tokens:
            if (
                tok.replace("-", "").replace(".", "").replace("~", "").isdigit()
            ):  # TOOD: refactor
                yield Num(tok.replace("~", "-"))  # TODO: refactor
            elif tok in Op._OPS:
                yield Op(tok)
            else:
                raise SyntaxError(f"Unknown token: {tok}")

    def evaluate(self) -> float:
        stack = []
        for token in self:
            if isinstance(token, Num):
                stack.append(token.value())
            elif isinstance(token, Op):
                a = stack.pop()
                b = stack.pop()
                stack.append(token.apply(a, b))
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return stack[0]
