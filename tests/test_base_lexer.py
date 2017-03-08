from unittest import TestCase

import base_lexer
from lexfailure import LexFailure
from pclosebracket import pCloseBracket
from popenbracket import pOpenBracket
from psymbol import pSymbol
from pltypeerror import plTypeError
from windowediterator import WindowedIterator


def lex(chars):
    return list(base_lexer.lex(chars))


class TestBaseLexer(TestCase):

    def test_Lexing_plain_characters_yields_a_symbol(self):
        self.assertEqual(
            lex("foo"),
            [pSymbol("foo")],
        )

    def test_Lexing_nonlist_is_an_error(self):
        with self.assertRaisesRegex(
                plTypeError,
                r'"chars" was expected to be Iterable\(plChar\) ' +
                r'but it is int\.  Value: 3\.'
        ):
            lex(3)

    def test_Lexing_list_of_nonchar_is_an_error(self):
        with self.assertRaisesRegex(
                plTypeError,
                r'"chars" was expected to be Iterable\(plChar\) ' +
                r'but it is Iterable\(int\)\.  Value: 3\.'
        ):
            lex([3, 4])

    def test_Lexing_list_of_nonshort_strings_is_an_error(self):
        with self.assertRaisesRegex(
                plTypeError,
                r'"chars" was expected to be Iterable\(plChar\) ' +
                r"but it is Iterable\(str\)\.  Value: 'yz'\."
        ):
            lex(["x", "yz"])

    def test_Lexing_a_bracket_yields_a_bracket(self):
        self.assertEqual(
            lex("("),
            [pOpenBracket()]
        )

    def test_Lexing_symbol_bracket_yields_that(self):
        self.assertEqual(
            lex("foo()"),
            [pSymbol("foo"), pOpenBracket(), pCloseBracket()]
        )

    def test_Symbols_may_contain_numbers_and_underscores(self):
        self.assertEqual(
            lex("foo9a_"),
            [pSymbol("foo9a_")]
        )

    def test_Symbols_may_start_with_underscores(self):
        self.assertEqual(
            lex("_foo9a_"),
            [pSymbol("_foo9a_")]
        )

    def test_Symbols_may_not_start_with_numbers(self):
        with self.assertRaises(LexFailure):
            lex("3_foo9a_")
