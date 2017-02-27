from unittest import TestCase

import base_lexer
from psymbol import pSymbol
from pltypeerror import plTypeError


def lex(chars):
    return list(base_lexer.lex(chars))


class TestBaseLexer(TestCase):

    def test_Lexing_plain_characters_yields_a_symbol(self):
        self.assertEqual(
            lex("foo"),
            [pSymbol("foo")],
        )

    def test_Lexing_nonchars_is_an_error(self):
        with self.assertRaisesRegex(
                plTypeError,
                ""
        ):
            lex(3)
