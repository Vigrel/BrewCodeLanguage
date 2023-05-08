from rply import LexerGenerator


class CoffeeLexer:
    def __init__(self):
        self.lg = LexerGenerator()

    def _add_tokens(self):
        self.lg.add("SOF", r"Let's brew a coffee")
        self.lg.add("EOF", r"Your coffee is ready")
        self.lg.add("FUNC_DEC", r"brew")
        self.lg.add("VARIABLE_DEC", r"cup")
        self.lg.add("LOOP", r"percolate")
        self.lg.add("IF", r"sip")
        self.lg.add("ELSE", r"gulp")
        self.lg.add("PRINT", r"serve")
        self.lg.add("RETURN", r"pour")
        self.lg.add("COMMA", r",")
        self.lg.add("SEMICOLON", r";")
        self.lg.add("LPAREN", r"\(")
        self.lg.add("RPAREN", r"\)")
        self.lg.add("LBRACE", r"{")
        self.lg.add("RBRACE", r"}")
        self.lg.add("EQUALS", r"=")
        self.lg.add("PLUS", r"\+")
        self.lg.add("MINUS", r"-")
        self.lg.add("TIMES", r"\*")
        self.lg.add("DIVIDE", r"/")
        self.lg.add("IDENTIFIER", r"[a-zA-Z][a-zA-Z0-9_]*")
        self.lg.add("STRING", r'"(?:\\.|[^"])*"')
        self.lg.add("NUMBER", r"[0-9]+")
        self.lg.ignore(r"\s+")

    def get_lexer(self):
        self._add_tokens()
        return self.lg.build()
