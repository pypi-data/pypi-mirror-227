import os

import pygments
from pygments.token import _TokenType
from tsx.tsx import TypeScriptXLexer, patch_pygments


def test_lexer_on_Blank():
    tsx_lexer = TypeScriptXLexer()
    parent = os.path.dirname(__file__)
    file_path = os.path.join(parent, 'Blank.tsx')
    with open(file_path) as f:
        txt = f.read()
        tokens = pygments.lex(txt, lexer=tsx_lexer)
        tokens = list(tokens)
        for idx, token in enumerate(tokens):
            print(idx)
            print(token)
        assert tokens[27][1] == 'div'
        assert isinstance(tokens[27][0], _TokenType)


def test_patch_pygments():
    patch_pygments()
    assert True
