from unittest import TestCase

from backtrackingiterator import BacktrackingIterator


class TestBacktrackingIterator(TestCase):

    def test_empty_list_wrapped_works_the_same(self):
        self.assertEqual(
            list(BacktrackingIterator([])),
            [],
        )

    def test_list_wrapped_works_the_same(self):
        self.assertEqual(
            "".join(BacktrackingIterator("abc")),
            "abc"
        )

    def test_can_mark_and_then_continue(self):
        """
        Pull out items, calling mark in between - all
        items should come out.
        """
        it = BacktrackingIterator("abcdefghijkl")
        ret = next(it)
        ret += next(it)
        it.mark()
        ret += next(it)
        it.mark()
        ret += "".join(it)
        self.assertEqual(ret, "abcdefghijkl")

    def test_can_go_back_to_beginning(self):
        it = BacktrackingIterator("abc")
        self.assertEqual(next(it), "a")
        self.assertEqual(next(it), "b")
        it.back()
        self.assertEqual(
            "".join(it),
            "abc"
        )

    def test_can_go_back_to_middle_point(self):
        it = BacktrackingIterator("abcdefghijkl")
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
