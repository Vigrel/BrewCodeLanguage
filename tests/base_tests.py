import os
import sys

# Get the absolute path of the current file (test_module1.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory of the current file (tests)
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the sys.path
sys.path.append(parent_dir)

import pytest

from compiler import CoffeeLexer, Parser, RplyParser, Tokenizer

DIRECTORY = "./tests/code/"


@pytest.fixture
def files():
    return [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY)]


@pytest.fixture
def lexer():
    return CoffeeLexer().get_lexer()


@pytest.fixture
def rply_parser():
    pg = RplyParser()
    pg.parse()
    return pg


def test_rply_lexical(lexer, files):
    for file in files:
        try:
            tkns = [t for t in lexer.lex(open(file, "r").read())]
        except:
            raise SyntaxError(f"{file} returned lexical error")


def test_rply_parser(lexer, rply_parser, files):
    for file in files:
        try:
            tkns = lexer.lex(open(file, "r").read())
            rply_parser.get_parser().parse(tkns).evaluate(rply_parser.st)
        except:
            raise SyntaxError(f"{file}")


def test_own_lexical(files):
    for file in files:
        try:
            tknz = Tokenizer(open(file, "r").read())
            while tknz.next.value != "ready":
                tknz.selectNext()
        except:
            raise SyntaxError(f"{file} returned lexical error")


def test_own_parser(files):
    for file in files:
        try:
            Parser.run(open(file, "r").read())
        except:
            raise SyntaxError(f"{file}")
