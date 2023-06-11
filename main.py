from CoffeeLexer import CoffeeLexer
from CoffeeParser import CoffeeParser


text_input = """
Let's brew a coffee

Your coffee is ready
"""
lexer = CoffeeLexer().get_lexer()
tokens = lexer.lex(text_input)

pg = CoffeeParser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).evaluate(pg.st)
