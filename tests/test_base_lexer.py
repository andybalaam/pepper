from unittest import TestCase

import base_lexer
from symbol import Symbol


def lex(chars):
    return list(base_lexer.lex(chars))


class TestBaseLexer(TestCase):
    def test_Lexing_plain_characters_yields_a_symbol(self):
        self.assertEqual(
            lex("foo"),
            [Symbol("foo")],
        )
