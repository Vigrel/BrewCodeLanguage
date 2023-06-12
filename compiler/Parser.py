from .Node import *
from .PrePro import Tokenizer


class Parser:
    tknz = Tokenizer("")
    symbol_table = SymbolTable()

    @staticmethod
    def parseBlock() -> Node:
        children = []
        if Parser.tknz.next.value != "Lets":
            raise SyntaxError
        Parser.tknz.selectNext()
        if Parser.tknz.next.value != "brew":
            raise SyntaxError
        Parser.tknz.selectNext()
        if Parser.tknz.next.value != "a":
            raise SyntaxError
        Parser.tknz.selectNext()
        if Parser.tknz.next.value != "coffee":
            raise SyntaxError
        Parser.tknz.selectNext()

        while Parser.tknz.next.value != "Your":
            children.append(Parser.parseStatement())

        Parser.tknz.selectNext()
        if Parser.tknz.next.value != "coffee":
            raise SyntaxError
        Parser.tknz.selectNext()
        if Parser.tknz.next.value != "is":
            raise SyntaxError
        Parser.tknz.selectNext()
        if Parser.tknz.next.value != "ready":
            raise SyntaxError

        return Block(children)

    @staticmethod
    def parseStatement() -> Node:
        node = NoOp()
        while Parser.tknz.next.value not in ["\n", "Your"]:
            if Parser.tknz.next.type == "PRINT":
                Parser.tknz.selectNext()
                node = Print([Parser.parseRealExpression()])
                if Parser.tknz.next.type == "SEMICOLON":
                    Parser.tknz.selectNext()
                    continue

            if Parser.tknz.next.type == "RETURN":
                Parser.tknz.selectNext()
                node = Return([Parser.parseRealExpression()])
                if Parser.tknz.next.type == "SEMICOLON":
                    Parser.tknz.selectNext()
                    continue

            if Parser.tknz.next.type in ["INT", "STR"]:
                typ = Parser.tknz.next.type
                Parser.tknz.selectNext()
                node = VarDec(Parser.tknz.next.value, typ)
                Parser.tknz.selectNext()
                if Parser.tknz.next.type == "SEMICOLON":
                    Parser.tknz.selectNext()
                    continue

            if Parser.tknz.next.type == "IDENTIFIER":
                idtf = Parser.tknz.next.value
                Parser.tknz.selectNext()
                if Parser.tknz.next.type == "EQUALS":
                    Parser.tknz.selectNext()
                    node = Assignment(idtf, [Parser.parseRealExpression()])
                    if Parser.tknz.next.type == "SEMICOLON":
                        Parser.tknz.selectNext()
                        continue

            if Parser.tknz.next.type == "LOOP":
                Parser.tknz.selectNext()
                while_exp = Parser.parseRealExpression()
                if Parser.tknz.next.type == "LBRACE":
                    Parser.tknz.selectNext()
                    children = []
                    while Parser.tknz.next.type != "RBRACE":
                        children.append(Parser.parseStatement())
                        if Parser.tknz.next.value == "Your":
                            raise SyntaxError
                    Parser.tknz.selectNext()
                    node = While([while_exp, Block(children)])
                    continue

            if Parser.tknz.next.type == "IF":
                childs = []
                Parser.tknz.selectNext()
                childs.append(Parser.parseRealExpression())
                if Parser.tknz.next.type == "LBRACE":
                    Parser.tknz.selectNext()
                    children_if = []
                    while Parser.tknz.next.type != "RBRACE":
                        children_if.append(Parser.parseStatement())
                        if Parser.tknz.next.value == "Your":
                            raise SyntaxError
                    Parser.tknz.selectNext()
                    childs.append(Block(children_if))
                    if Parser.tknz.next.type == "ELSE":
                        Parser.tknz.selectNext()
                        if Parser.tknz.next.type == "LBRACE":
                            Parser.tknz.selectNext()
                            children_else = []
                            while Parser.tknz.next.type != "RBRACE":
                                children_else.append(Parser.parseStatement())
                                if Parser.tknz.next.value == "Your":
                                    raise SyntaxError(f"end not used")
                            Parser.tknz.selectNext()
                            childs.append(Block(children_else))
                    node = If(childs)
                    continue

            if Parser.tknz.next.type == "FUNC_DEC":
                Parser.tknz.selectNext()
                if Parser.tknz.next.type in ["INT", "STR"]:
                    typ = Parser.tknz.next.type
                    Parser.tknz.selectNext()
                    if Parser.tknz.next.type == "IDENTIFIER":
                        idtf = Parser.tknz.next.value
                        Parser.tknz.selectNext()
                        if Parser.tknz.next.type == "PARENO":
                            var_dec = []
                            Parser.tknz.selectNext()
                            while Parser.tknz.next.type != "PARENC":
                                if Parser.tknz.next.value == "Your":
                                    raise SyntaxError
                                if Parser.tknz.next.type in ["INT", "STR"]:
                                    var_typ = Parser.tknz.next.type
                                    Parser.tknz.selectNext()
                                    if Parser.tknz.next.type == "IDENTIFIER":
                                        var_idtf = Parser.tknz.next.value
                                        var_dec.append([var_idtf, var_typ])
                                        Parser.tknz.selectNext()
                                        if Parser.tknz.next.type == "COMMA":
                                            Parser.tknz.selectNext()
                                            continue
                            Parser.tknz.selectNext()
                            if Parser.tknz.next.type == "LBRACE":
                                Parser.tknz.selectNext()
                                func_block = []
                                while Parser.tknz.next.type != "RBRACE":
                                    func_block.append(Parser.parseStatement())
                                    if Parser.tknz.next.value == "Your":
                                        raise SyntaxError(f"end not used")
                                Parser.tknz.selectNext()
                                node = FuncDec(typ, [idtf, var_dec, Block(func_block)])
                                continue

                Parser.tknz.selectNext()

            raise SyntaxError(f"ivalid syntax - {Parser.tknz.next.value}")
        Parser.tknz.selectNext()
        return node

    @staticmethod
    def parseRealExpression() -> Node:
        node = Parser.parseExpression()

        while Parser.tknz.next.type in ["EQT", "GT", "LT"]:
            op = Parser.tknz.next.type
            Parser.tknz.selectNext()

            node = BinOp(
                op,
                [node, Parser.parseExpression()],
            )

        return node

    @staticmethod
    def parseExpression() -> Node:
        node = Parser.parseTerm()

        while Parser.tknz.next.type in ["PLUS", "MINUS", "OR", "CONC"]:
            op = Parser.tknz.next.type
            Parser.tknz.selectNext()

            if Parser.tknz.next.type in ["DIVIDED", "TIMES"]:
                raise SyntaxError(f"ivalid syntax - {op}{Parser.tknz.next.value}")

            node = BinOp(
                op,
                [node, Parser.parseTerm()],
            )

        if Parser.tknz.next.type == "IDENTIFIER":
            raise SyntaxError(f"ivalid syntax - {Parser.tknz.next.value}")

        return node

    @staticmethod
    def parseTerm() -> Node:
        node = Parser.parseFactor()

        while Parser.tknz.next.type in ["DIVIDED", "TIMES", "AND"]:
            op = Parser.tknz.next.type
            Parser.tknz.selectNext()

            if Parser.tknz.next.type in ["DIVIDED", "TIMES"]:
                raise SyntaxError(f"ivalid syntax - {op}{Parser.tknz.next.value}")

            node = BinOp(
                op,
                [node, Parser.parseFactor()],
            )

        return node

    @staticmethod
    def parseFactor() -> Node:
        tkn = Parser.tknz.next
        Parser.tknz.selectNext()

        if tkn.type == "STRING":
            return StrVal(tkn.value)

        if tkn.type == "NUMBER":
            return IntVal(tkn.value)

        if tkn.type == "IDENTIFIER":
            if Parser.tknz.next.type == "PARENO":
                func_agrs = []
                while True:
                    Parser.tknz.selectNext()
                    if Parser.tknz.next.type == "PARENC":
                        break
                    func_agrs.append(Parser.parseRealExpression())
                    if Parser.tknz.next.type == "COMMA":
                        continue
                    break
                if Parser.tknz.next.type == "PARENC":
                    Parser.tknz.selectNext()
                    return FuncCall(tkn.value, func_agrs)
                raise SyntaxError

            return Identifier(tkn.value)

        if tkn.type in ["PLUS", "MINUS", "NOT"]:
            if Parser.tknz.next.type in ["DIVIDED", "TIMES"]:
                raise SyntaxError(
                    f"ivalid syntax - {tkn.value}{Parser.tknz.next.value}"
                )

            return UnOp(tkn.value, [Parser.parseFactor()])

        if tkn.type == "PARENO":
            node = Parser.parseRealExpression()
            if Parser.tknz.next.type == "PARENC":
                Parser.tknz.selectNext()
                return node
            raise SyntaxError("'(' was never closed")

    @staticmethod
    def run(code: str) -> any:
        Parser.tknz.__init__(code)
        return Parser.parseBlock().evaluate(Parser.symbol_table)
