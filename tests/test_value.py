from unittest import TestCase

from pltypes.value import value


@value
class MyVal:
    pass


class TestValue(TestCase):

    def test_value_class_has_repr(self):
        self.assertEqual(
            repr(MyVal()),
            "MyVal()"
        )

    def test_value_class_has_str(self):
        self.assertEqual(
            str(MyVal()),
            "MyVal()"
        )
