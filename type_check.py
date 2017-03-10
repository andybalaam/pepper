def type_check(type_, var_value, var_name):
    assert hasattr(type_, "check")
    assert type(var_name) == str
    type_.check(var_value, var_name)
