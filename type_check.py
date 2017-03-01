from pltypes.checkabletype import CheckableType


def type_check(type_, var_value, var_name):
    assert isinstance(type_, CheckableType)
    type_.check(var_value, var_name)
