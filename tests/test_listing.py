from unittest import TestCase
import textwrap


from listing import listing


class Testlisting(TestCase):

    def test_Empty_before_prints_nothing(self):
        self.assertEqual(
            listing("", "", (1, 1)),
            """  ^^^ <--- here\n"""
        )

    def test_Single_line_prints_it(self):
        self.assertEqual(
            listing("foo", "", (1, 1)),
            textwrap.dedent(
                """
                1|foo
                  ^^^ <--- here
                """
            ).lstrip(),
        )

    def test_Multiple_lines_near_top_are_printed(self):
        self.assertEqual(
            listing("foo\nbar\n", "", (1, 2)),
            textwrap.dedent(
                """
                1|foo
                2|bar
                  ^^^ <--- here
                """
            ).lstrip(),
        )

    def test_Multiple_lines_near_further_down_are_printed(self):
        self.assertEqual(
            listing("bar\nbaz\nqux\n", "", (1, 4)),
            textwrap.dedent(
                """
                2|bar
                3|baz
                4|qux
                  ^^^ <--- here
                """
            ).lstrip(),
        )

    def test_Trailing_characters_in_after(self):
        self.assertEqual(
            listing("foo ", "bar\n", (1, 1)),
            textwrap.dedent(
                """
                1|foo bar
                  ^^^ <--- here
                """
            ).lstrip(),
        )

    def test_More_lines_in_after(self):
        self.assertEqual(
            listing("foo ", "bar\nbaz\nqux", (1, 1)),
            textwrap.dedent(
                """
                1|foo bar
                  ^^^ <--- here
                2|baz
                3|qux
                """
            ).lstrip(),
        )

    def test_Several_full_lines_before_and_after(self):
        self.assertEqual(
            listing(
                "foo bar\nbaz\nqux\n",
                "quux\nwat\nbob\n",
                (1, 7)
            ),
            textwrap.dedent(
                """
                 5|foo bar
                 6|baz
                 7|qux
                   ^^^ <--- here
                 8|quux
                 9|wat
                10|bob
                """
            )[1:]
        )

    def test_Relevant_symbol_not_at_start(self):
        self.assertEqual(
            listing(
                "foo bar\nbaz\nqux (",
                " summat\nquux\nwat\nbob\n",
                (5, 101)
            ),
            textwrap.dedent(
                """
                 99|foo bar
                100|baz
                101|qux ( summat
                        ^^^ <--- here
                102|quux
                103|wat
                104|bob
                """
            )[1:]
        )
