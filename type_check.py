from pltypes.hasmethod import hasmethod
from pltypes.pltypeequals import plTypeEquals
from pltypeerror import plTypeError


def type_check(type_, var_value, var_name):
    assert type(var_name) == str
    if type(type_) == type:
        type_check(plTypeEquals(type_), var_value, var_name)
    elif hasmethod(type_, "check"):
        type_.check(var_value, var_name)
    else:
        raise plTypeError(
            "type_",
            type(type_).__name__,
            "Checkable or type",
            type_
        )
