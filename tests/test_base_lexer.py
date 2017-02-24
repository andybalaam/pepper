from unittest import TestCase

from base_lexer import lex
from symbol import Symbol

class TestBaseLexer(TestCase):
    def test_lex_symbol(self):
        self.assertEqual(
            Symbol("foo"),
            lex("foo")
        )
