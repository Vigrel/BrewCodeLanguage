from rply import ParserGenerator
from AST import *


class CoffeeParser:
    def __init__(self):
        self.pg = ParserGenerator(
            [
                "SOF",
                "EOF",
                "FUNC_DEC",
                "VARIABLE_DEC",
                "LOOP",
                "IF",
                "ELSE",
                "PRINT",
                "RETURN",
                "SEMICOLON",
                "LPAREN",
                "RPAREN",
                "LBRACE",
                "RBRACE",
                "EQUALS",
                "PLUS",
                "MINUS",
                "TIMES",
                "DIVIDE",
                "IDENTIFIER",
                "STRING",
                "NUMBER",
            ],
            precedence=[
                ("left", ["PLUS", "MINUS"]),
                ("left", ["TIMES", "DIVIDE"]),
            ],
        )

    def parse(self):
        @self.pg.production("program : SOF statements EOF")
        def program(p):
            return Block(p[1])

        @self.pg.production("statements : ")
        @self.pg.production("statements : statement")
        @self.pg.production("statements : statements statement")
        def statements(p):
            if len(p) == 0:
                return [NoOp()]
            if len(p) == 1:
                return [p[0]]
            p[0].append(p[1])
            return p[0]

        @self.pg.production("statement : expression SEMICOLON")
        @self.pg.production("statement : serve_statement")
        @self.pg.production("statement : condition")
        @self.pg.production("statement : loop")
        @self.pg.production("statement : variable_declaration")
        @self.pg.production("statement : assignment")
        def statement(p):
            return p[0]

        @self.pg.production("serve_statement : PRINT expression SEMICOLON")
        def serve_statement(p):
            return Print([p[1]])

        ## Conditional
        @self.pg.production(
            "condition : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE"
        )
        @self.pg.production(
            "condition : IF LPAREN expression RPAREN LBRACE statements RBRACE"
        )
        def condition_statement(p):
            if len(p) > 7:
                return If([p[2], Block(p[5]), Block(p[9])])
            return If([p[2], Block(p[5])])

        @self.pg.production(
            "loop : LOOP LPAREN expression RPAREN LBRACE statements RBRACE"
        )
        def loop_statement(p):
            return While([p[2], Block(p[5])])

        ## Variables
        @self.pg.production("variable_declaration : VARIABLE_DEC IDENTIFIER SEMICOLON")
        @self.pg.production(
            "variable_declaration : VARIABLE_DEC IDENTIFIER EQUALS expression SEMICOLON"
        )
        def variable_declaration(p):
            if len(p) > 3:
                VarDec(p[1].value).evaluate()
                return Assignment(p[1].value, [p[3]])
            return VarDec(p[1].value)

        @self.pg.production("assignment : IDENTIFIER EQUALS expression SEMICOLON")
        def assignment(p):
            return Assignment(p[0].value, [p[2]])

        ## Body
        @self.pg.production("expression : term")
        @self.pg.production("expression : expression PLUS term")
        @self.pg.production("expression : expression MINUS term")
        def expression(p):
            if len(p) == 1:
                return p[0]
            return BinOp(p[1].gettokentype(), [p[0], p[2]])

        @self.pg.production("term : factor")
        @self.pg.production("term : term TIMES factor")
        @self.pg.production("term : term DIVIDE factor")
        def term(p):
            if len(p) == 1:
                return p[0]
            return BinOp(p[1].gettokentype(), [p[0], p[2]])

        @self.pg.production("factor : NUMBER")
        def factor_number(p):
            return IntVal(p[0].value)

        @self.pg.production("factor : STRING")
        def factor_number(p):
            return StrVal(p[0].value[1:-1])

        @self.pg.production("factor : IDENTIFIER")
        def factor_identifier(p):
            return Identifier(p[0].value)

        @self.pg.production("factor : LPAREN expression RPAREN")
        def factor_expression(p):
            return p[1]

    def get_parser(self):
        return self.pg.build()
