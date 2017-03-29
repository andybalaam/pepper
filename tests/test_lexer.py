from unittest import TestCase
import textwrap

import lexing.base_lex
import lexing.lex
from lexing.lexfailure import LexFailure
from pclosebracket import pCloseBracket
from pequalssign import pEqualsSign
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
        with self.assertRaises(LexFailure) as msg:
            lex("foo\nbar 3_foo9a_")

        self.assertEqual(
            str(msg.exception),
            textwrap.dedent(
                """
                <stdin>:2:5 I can't understand '3_foo9a_'
                (it is not recognised by the lexer).

                1|foo
                2|bar 3_foo9a_
                      ^^^ <--- here
                """
            )[1:]
        )

    def test_LexFailure_prints_leading_and_trailing_lines(self):
        with self.assertRaises(LexFailure) as msg:
            lex(
                "a1\na2\na3\na4\na5\na6\na7\na8\na9\n" +
                "a10  6a\na11\na12\na13\na14\n"
            )

        self.assertEqual(
            str(msg.exception),
            textwrap.dedent(
                """
                <stdin>:10:6 I can't understand '6a'
                (it is not recognised by the lexer).

                 7|a7
                 8|a8
                 9|a9
                10|a10  6a
                        ^^^ <--- here
                11|a11
                12|a12
                13|a13
                14|a14
                """
            )[1:]
        )

    def test_LexFailure_with_later_chars_prints_lines(self):
        with self.assertRaises(LexFailure) as msg:
            lex(
                "a1\na2\na3\na4\na5\na6\na7\na8\na9\n" +
                "a10  6a b\na11\na12\na13\na14\n"
            )

        self.assertEqual(
            str(msg.exception),
            textwrap.dedent(
                """
                <stdin>:10:6 I can't understand '6a'
                (it is not recognised by the lexer).

                 6|a6
                 7|a7
                 8|a8
                 9|a9
                10|a10  6a b
                        ^^^ <--- here
                11|a11
                12|a12
                13|a13
                """
            )[1:]
        )

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
        with self.assertRaises(LexFailure) as e:
            lex("xx\ty")

        self.assertEqual(
            str(e.exception),
            textwrap.dedent(
                """
                <stdin>:1:3 Tab characters are not allowed.

                1|xx\ty
                    ^^^ <--- here
                """
            )[1:]
        )

    def test_Complete_example(self):
        # TODO: new lines etc.
        self.assertEqual(
            lex('int x = int("4");'),
            [
                pSymbol("int"),
                pWhitespace(value=" "),
                pSymbol("x"),
                pWhitespace(value=" "),
                pEqualsSign(),
                pWhitespace(value=" "),
                pSymbol("int"),
                pOpenBracket(),
                pString(value="4"),
                pCloseBracket(),
                pSemicolon(),
            ]
        )
