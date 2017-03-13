from unittest import TestCase

from pltypes.hasmethod import hasmethod


class MyBase:
    def exists_in_base(self):
        pass


class MyVal(MyBase):
    def __init__(self):
        self.fld = 3

    def existing(self):
        pass

    nm = 3


class TestValue(TestCase):

    def test_true_if_method_exists(self):
        self.assertTrue(hasmethod(MyVal(), "existing"))

    def test_true_if_exists_in_base(self):
        self.assertTrue(hasmethod(MyVal(), "exists_in_base"))

    def test_false_if_does_not_exist(self):
        self.assertFalse(hasmethod(MyVal(), "notexists"))

    def test_false_if_is_a_member_variable(self):
        self.assertFalse(hasmethod(MyVal(), "fld"))

    def test_false_if_is_a_class_variable(self):
        self.assertFalse(hasmethod(MyVal(), "nm"))
