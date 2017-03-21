from unittest import TestCase


from pltypes.iterable import Iterable
from pltypes.plchar import plChar
from positionedcharacters import PositionedCharacters
from type_check import type_check


def _join_chars(it):
    type_check(Iterable(plChar()), it, "it")
    return "".join(str(v) for v in iter(it))


class TestPositionedCharacters(TestCase):

    def test_empty_list_wrapped_works_the_same(self):
        self.assertEqual(
            list(PositionedCharacters("", "foo")),
            [],
        )

    def test_single_line_tracks_column(self):
        ans = list(PositionedCharacters("123", "foo"))
        self.assertEqual(
            _join_chars(ans),
            "123",
        )
        self.assertEqual(
            list(i.pos for i in ans),
            [(1, 1), (2, 1), (3, 1)],
        )

    def test_next_line_tracks_row_and_column(self):
        ans = list(PositionedCharacters("12\n34", "foo"))
        self.assertEqual(
            _join_chars(ans),
            "12\n34",
        )
        self.assertEqual(
            list(i.pos for i in ans),
            [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2)],
        )
