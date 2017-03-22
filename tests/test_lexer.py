from unittest import TestCase

import lexing.base_lex
import lexing.lex
from lexing.lexfailure import LexFailure
from pclosebracket import pCloseBracket
from popenbracket import pOpenBracket
from psemicolon import pSemicolon
from pstring import pString
from psymbol import pSymbol
from pltypeerror import plTypeError
from pwhitespace import pWhitespace


def lex(chars):
    return list(lexing.lex.lex(chars))


class TestLexer(TestCase):

    def test_Lexing_plain_characters_yields_a_symbol(self):
        self.assertEqual(
            lex("foo"),
            [pSymbol("foo")],
        )

    def test_Lexing_nonlist_is_an_error(self):
        with self.assertRaisesRegex(
                plTypeError,
                r'"chars" was expected to be Iterable\(CharAtPosType\) ' +
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
        self.assertEqual(
            lex(")"),
            [pCloseBracket()]
        )

    def test_Lexing_a_semicolon_yields_one(self):
        self.assertEqual(
            lex(";"),
            [pSemicolon()]
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
        with self.assertRaisesRegex(
            LexFailure,
            r"<stdin>:2:5 I can't understand '3_foo9a_' \(it is not " +
            "recognised by the lexer\)\."
        ):
            lex("foo\nbar 3_foo9a_")

    def test_noncallable_lex_function_is_an_error(self):
        fn = 3
        with self.assertRaisesRegex(
            plTypeError,
            r'"lex_fns" was expected to be Iterable\(Callable\) but ' +
            r'it is Iterable\(int\).  Value: 3.'
        ):
            list(lexing.base_lex.base_lex("a", [fn]))

    def test_Lexing_a_string(self):
        self.assertEqual(
            lex('"foo"'),
            [pString(value="foo")]
        )

    def test_Strings_may_be_followed_by_other_tokens(self):
        self.assertEqual(
            lex('("foo")'),
            [pOpenBracket(), pString(value="foo"), pCloseBracket()]
        )

    def test_Whitespace_gets_lexed(self):
        self.assertEqual(
            lex(' \n '),
            [pWhitespace(value=" \n ")]
        )

    def test_Symbols_can_be_separated_by_whitespace(self):
        self.assertEqual(
            lex('foo bar'),
            [pSymbol("foo"), pWhitespace(value=" "), pSymbol("bar")]
        )

    def test_Tab_characters_are_errors(self):
        # TODO:
        # """<stdin>:1:3 Error - tab characters are not allowed.
        # 1|xx\ty
        #     ^^^ <-- here
        # """):
        with self.assertRaisesRegex(
                LexFailure,
                """Tab characters are not allowed."""
                ):
            lex("xx\ty")

#    def test_Complete_example(self):
#        # TODO: new lines etc.
#        self.assertEqual(
#            lex('int x = int("4");'),
#            [
#                pSymbol("int"),
#                pWhitespace(" "),
#                pSymbol("x"),
#                pWhitespace(" "),
#                pEqualsSign(),
#                pSymbol("int"),
#                pOpenBracket(),
#                pString(value="4"),
#                pCloseBracket(),
#                pSemiColon(),
#            ]
#        )

    # todo errors with line and column numbers, and file names
