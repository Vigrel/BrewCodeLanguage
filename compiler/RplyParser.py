from rply import ParserGenerator
from .Node import *
from .SymbolTable import SymbolTable


class RplyParser:
    def __init__(self):
        self.st = SymbolTable()
        self.pg = ParserGenerator(
            [
                "SOF",
                "EOF",
                "FUNC_DEC",
                "INT",
                "STR",
                "LOOP",
                "IF",
                "ELSE",
                "PRINT",
                "RETURN",
                "GT",
                "LT",
                "EQT",
                "AND",
                "OR",
                "COMMA",
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

        @self.pg.production("statement : condition")
        @self.pg.production("statement : loop")
        @self.pg.production("statement : function_declaration")
        @self.pg.production("statement : rel_expression SEMICOLON")
        @self.pg.production("statement : print_statement SEMICOLON")
        @self.pg.production("statement : variable_declaration SEMICOLON")
        @self.pg.production("statement : variable_assignment SEMICOLON")
        @self.pg.production("statement : return_statement SEMICOLON")
        def statement(p):
            return p[0]

        ##########  FUNCTIONS
        @self.pg.production(
            "function_declaration : FUNC_DEC INT IDENTIFIER LPAREN param_list RPAREN LBRACE statements RBRACE"
        )
        @self.pg.production(
            "function_declaration : FUNC_DEC STR IDENTIFIER LPAREN param_list RPAREN LBRACE statements RBRACE"
        )
        def function_declaration(p):
            return FuncDec(p[1].name, [p[2].value, p[4], Block(p[7])])

        @self.pg.production("param_list : ")
        @self.pg.production("param_list : variable_declaration")
        @self.pg.production("param_list : param_list COMMA variable_declaration")
        def param_list(p):
            if len(p) == 0:
                return []
            if len(p) == 1:
                return [[p[0].value, p[0].children]]
            p[0].append([p[2].value, p[2].children])
            return p[0]

        @self.pg.production("function_call : IDENTIFIER LPAREN  param_list_call RPAREN")
        def function_call(p):
            return FuncCall(p[0].value, p[2])

        @self.pg.production("param_list_call : ")
        @self.pg.production("param_list_call : rel_expression")
        @self.pg.production("param_list_call : param_list_call COMMA rel_expression")
        def param_list_call(p):
            if len(p) == 0:
                return []
            if len(p) == 1:
                return [p[0]]
            p[0].append(p[2])
            return p[0]

        @self.pg.production("return_statement : RETURN rel_expression")
        def return_statement(p):
            return Return([p[1]])

        ##########  CONDITIONAL
        @self.pg.production(
            "condition : IF rel_expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE"
        )
        @self.pg.production("condition : IF rel_expression LBRACE statements RBRACE")
        def condition_statement(p):
            if len(p) > 5:
                return If([p[1], Block(p[3]), Block(p[7])])
            return If([p[1], Block(p[3])])

        ##########  LOOP_STATEM
        @self.pg.production("loop : LOOP rel_expression LBRACE statements RBRACE")
        def loop_statement(p):
            return While([p[1], Block(p[3])])

        ##########  VARIABLES
        @self.pg.production("variable_declaration : INT IDENTIFIER")
        @self.pg.production("variable_declaration : STR IDENTIFIER")
        def variable_declaration(p):
            return VarDec(p[1].value, p[0].name)

        @self.pg.production("variable_assignment : IDENTIFIER EQUALS rel_expression")
        def variable_assignment(p):
            return Assignment(p[0].value, [p[2]])

        ##########  PRINT_STATEM
        @self.pg.production("print_statement : PRINT rel_expression")
        def print_statement(p):
            return Print([p[1]])

        ##########  EXPRESSSIONS
        @self.pg.production("rel_expression : expression")
        @self.pg.production("rel_expression : rel_expression EQT expression")
        @self.pg.production("rel_expression : rel_expression GT expression")
        @self.pg.production("rel_expression : rel_expression LT expression")
        def rel_expression(p):
            if len(p) == 1:
                return p[0]
            return BinOp(p[1].gettokentype(), [p[0], p[2]])

        @self.pg.production("expression : term")
        @self.pg.production("expression : expression PLUS term")
        @self.pg.production("expression : expression MINUS term")
        @self.pg.production("expression : expression OR term")
        def expression(p):
            if len(p) == 1:
                return p[0]
            return BinOp(p[1].gettokentype(), [p[0], p[2]])

        @self.pg.production("term : factor")
        @self.pg.production("term : term TIMES factor")
        @self.pg.production("term : term DIVIDE factor")
        @self.pg.production("term : term AND factor")
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

        @self.pg.production("factor : LPAREN rel_expression RPAREN")
        def factor_rel_expression(p):
            return p[1]

        @self.pg.production("factor : function_call")
        def factor_rel_expression(p):
            return p[0]

    def get_parser(self):
        return self.pg.build()
