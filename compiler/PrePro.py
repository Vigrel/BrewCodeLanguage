OPS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "TIMES",
    "/": "DIVIDED",
    "(": "PARENO",
    ")": "PARENC",
    "!": "NOT",
    ",": "COMMA",
    "=": "EQUALS",
    ";": "SEMICOLON",
    "{": "LBRACE",
    "}": "RBRACE",
    "\n": "LN",
}
RES_WRDS = {
    "brew": "FUNC_DEC",
    "cup": "INT",
    "lungo": "STR",
    "percolate": "LOOP",
    "sip": "IF",
    "gulp": "ELSE",
    "serve": "PRINT",
    "pour": "RETURN",
    "stronger": "GT",
    "weaker": "LT",
    "same": "EQT",
    "also": "AND",
    "maybe": "OR",
}


class Token:
    def __init__(self, type: str, value: int) -> None:
        self.type: str = type
        self.value: int = value


class Tokenizer:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.position: int = 0
        self.next: Token = Token("", 0)
        self.length = len(self.source)

        self.selectNext()

    def selectNext(self):
        while self.position < self.length:
            letter = self.source[self.position]
            self.position += 1

            if letter == " ":
                continue

            elif letter in OPS:
                self.next = Token(OPS[letter], letter)

            elif letter == '"':
                string = ""
                while self.source[self.position] != '"':
                    string += self.source[self.position]
                    self.position += 1
                self.position += 1
                self.next = Token("STRING", string)

            elif letter.isdecimal():
                num = letter
                while (
                    self.position < self.length
                    and self.source[self.position].isdecimal()
                ):
                    num += self.source[self.position]
                    self.position += 1
                self.next = Token("NUMBER", num)

            elif letter.isalpha() or letter == "_":
                idtf = letter
                while self.position < self.length and (
                    self.source[self.position].isalnum()
                    or self.source[self.position] == "_"
                ):
                    idtf += self.source[self.position]
                    self.position += 1

                if idtf in RES_WRDS:
                    self.next = Token(RES_WRDS[idtf], idtf)
                else:
                    self.next = Token("IDENTIFIER", idtf)

            else:
                raise SyntaxError(f"invalid syntax - {self.source[self.position]}")
            return
