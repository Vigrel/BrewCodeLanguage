from CoffeeLexer import CoffeeLexer
from CoffeeParser import CoffeeParser


text_input = """
Let's brew a coffee
  cup blackCoffee = 10;
  cup americanCoffee = 0;
  cup water = 1;
  percolate(blackCoffee stronger than americanCoffee) {
    sip (blackCoffee weaker than 5) {
      sip(blackCoffee weaker than 2) {
        serve "No sugar added";
      } gulp {
        serve "Adding sugar";
      }
    }
    blackCoffee = blackCoffee - water;
  }
Your coffee is ready
"""
lexer = CoffeeLexer().get_lexer()
tokens = lexer.lex(text_input)

pg = CoffeeParser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).evaluate()
