from unittest import TestCase

from pltypeerror import plTypeError
from pltypes.plchar import plChar
from pltypes.pltypeequals import plTypeEquals
from pltypes.value import value


@value
class MyVal:
    pass


@value(
    x1=int,
    ch=plChar()
)
class WithMembers:
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

    def test_value_with_fields_has_constructor(self):
        WithMembers(x1=3, ch="x")

    def test_value_construction_holds_field_values(self):
        obj = WithMembers(x1=3, ch="x")
        self.assertEqual(3, obj.x1)
        self.assertEqual("x", obj.ch)

    def test_type_check_on_value_construction(self):
        with self.assertRaisesRegex(
            plTypeError,
            """"x1" was expected to be <class 'int'> """ +
            """but it is str.  Value: '3'."""
        ):
            WithMembers(x1="3", ch="x")

    def test_value_type_must_be_a_type_or_checkable(self):
        with self.assertRaisesRegex(
            plTypeError,
            """"type_" was expected to be Checkable or type """ +
            """but it is int.  Value: 3."""
        ):
            @value(x=3)
            class MyClass:
                pass
            MyClass(x=3)
