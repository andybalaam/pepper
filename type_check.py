from pltypes.hasmethod import hasmethod
from pltypeerror import plTypeError


def type_check(type_, var_value, var_name):
    if not hasmethod(type_, "check"):
        raise plTypeError(
            "type_",
            type(type_).__name__,
            "Checkable or type",
            type_
        )
    assert type(var_name) == str
    type_.check(var_value, var_name)
