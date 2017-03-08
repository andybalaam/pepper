from unittest import TestCase


from pltypeerror import plTypeError
from pltypes.anytype import AnyType
from pltypes.notype import NoType
from windowediterator import WindowedIterator


class TestWindowedIterator(TestCase):

    def test_empty_list_wrapped_works_the_same(self):
        self.assertEqual(
            list(WindowedIterator([], AnyType(), "x")),
            [],
        )

    def test_list_wrapped_works_the_same(self):
        self.assertEqual(
            "".join(WindowedIterator("abc", AnyType(), "x")),
            "abc"
        )

    def test_can_mark_and_then_continue(self):
        """
        Pull out items, calling mark in between - all
        items should come out.
        """
        it = WindowedIterator("abcdefghijkl", AnyType(), "x")
        ret = next(it)
        ret += next(it)
        it.mark()
        ret += next(it)
        it.mark()
        ret += "".join(it)
        self.assertEqual(ret, "abcdefghijkl")

    def test_can_go_back_to_beginning(self):
        it = WindowedIterator("abc", AnyType(), "x")
        self.assertEqual(next(it), "a")
        self.assertEqual(next(it), "b")
        it.back()
        self.assertEqual(
            "".join(it),
            "abc"
        )

    def test_can_go_back_to_middle_point(self):
        it = WindowedIterator("abcdefghijkl", AnyType(), "x")
        self.assertEqual(next(it), "a")
        self.assertEqual(next(it), "b")
        it.back()
        self.assertEqual(next(it), "a")
        it.mark()
        self.assertEqual(next(it), "b")
        self.assertEqual(next(it), "c")
        self.assertEqual(next(it), "d")
        it.back()
        self.assertEqual(next(it), "b")
        self.assertEqual(next(it), "c")
        it.mark()
        self.assertEqual(next(it), "d")
        it.back()
        self.assertEqual("".join(it), "defghijkl")

    def test_peek_returns_next_character(self):
        it = WindowedIterator("abc", AnyType(), "x")
        self.assertEqual(it.peek(), "a")
        self.assertEqual(it.peek(), "a")
        next(it)
        self.assertEqual(it.peek(), "b")
        self.assertEqual(it.peek(), "b")

    def test_peek_works_after_back(self):
        it = WindowedIterator("abc", AnyType(), "x")
        next(it)
        it.mark()
        next(it)
        it.back()
        self.assertEqual(it.peek(), "b")
        self.assertEqual(it.peek(), "b")
        next(it)
        self.assertEqual(it.peek(), "c")
        self.assertEqual(it.peek(), "c")

    def test_type_check_throws_if_wrong_type(self):
        it = WindowedIterator("abc", NoType(), "name")
        with self.assertRaisesRegex(
            plTypeError,
            r'"name" was expected to be'
        ):
            next(it)
