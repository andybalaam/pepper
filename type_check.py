from pltypes.hasmethod import hasmethod


def type_check(type_, var_value, var_name):
    assert hasmethod(type_, "check")
    assert type(var_name) == str
    type_.check(var_value, var_name)
