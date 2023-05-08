from CoffeeLexer import CoffeeLexer
from CoffeeParser import CoffeeParser


text_input = """
Let's brew a coffee
  cup small;
  cup big;
  small = 0;
  big = 5;
  sip (small){
      serve  small;
  } gulp{
      serve  big;
  }
Your coffee is ready
"""
lexer = CoffeeLexer().get_lexer()
tokens = lexer.lex(text_input)

pg = CoffeeParser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).evaluate()
