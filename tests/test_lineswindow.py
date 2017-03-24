from unittest import TestCase
from itertools import islice


from lineswindow import LinesWindow
from type_check import type_check


def _join_chars(it):
    type_check(Iterable(plChar), it, "it")
    return "".join(v for v in iter(it))


class TestLinesWindow(TestCase):

    def test_empty_string_has_empty_window(self):
        it = iter(LinesWindow("", "it"))
        self.assertEqual(
            "".join(it),
            "",
        )
        self.assertEqual(it.before(), "")
        self.assertEqual(it.after(), "")

    def test_at_beginning_before_is_empty(self):
        it = iter(LinesWindow("abc\ndef\n", "it"))
        self.assertEqual(it.before(), "")

    def test_at_beginning_end_is_current_plus_three_more_lines(self):
        it = iter(LinesWindow("ab\ncd\nef\ngh\nij\n", "it"))
        self.assertEqual(it.after(), "ab\ncd\nef\ngh\n")

    def test_at_end_after_is_empty(self):
        it = iter(LinesWindow("ab\n", "it"))
        list(islice(it, 3))
        self.assertEqual(it.after(), "")

    def test_near_end_after_is_all(self):
        it = iter(LinesWindow("ab\ncd\nef", "it"))
        list(islice(it, 3))
        self.assertEqual(it.after(), "cd\nef")

    def test_at_beginning_before_is_empty(self):
        it = iter(LinesWindow("abc\ndef\n", "it"))
        self.assertEqual(it.before(), "")

    def test_first_line_is_in_before(self):
        it = iter(LinesWindow("abc\ndef\n", "it"))
        list(islice(it, 2))
        self.assertEqual(it.before(), "ab")

    def test_after_one_line_it_is_in_before(self):
        it = iter(LinesWindow("abc\ndef\n", "it"))
        list(islice(it, 5))
        self.assertEqual(it.before(), "abc\nd")

    def test_after_many_lines_four_are_in_before(self):
        it = iter(LinesWindow("\n".join("abcdef"), "it"))
        list(islice(it, 10))
        self.assertEqual(it.before(), "b\nc\nd\ne\n")

    def test_current_is_in_before_even_after_lines(self):
        it = iter(LinesWindow("z\na\nb\nc\nd\nefghu", "it"))
        list(islice(it, 12))
        self.assertEqual(it.before(), "a\nb\nc\nd\nef")

    def test_rest_of_current_line_is_in_after(self):
        it = iter(LinesWindow("ab\ncd\nef\ngh\nij\nkl\nmn\n", "it"))
        list(islice(it, 4))
        self.assertEqual(it.after(), "d\nef\ngh\nij\n")
