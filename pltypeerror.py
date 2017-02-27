def _check_has_property(var_name, var_value, property_name):
    if property_name not in var_value:
        raise AssertionError(
            "'%s' has no property '%s' - it is '%s'." % (
                var_name, property_name, str(var_value)
            )
        )


class plTypeError(Exception):
    """
    Raised if some Pepper2Like code fails to pass
    run-time type checks.

    Usually raised by the type_check() function.
    """
    def __init__(self, var_name, var_value, expected_type):
        assert var_name.__class__ == str

        self.var_name = var_name
        self.var_value = var_value
        self.expected_type = expected_type

    def __str__(self):
        return '"%s" was expected to be %s but it is %s.  Value: %s.' % (
            self.var_name,
            str(self.expected_type),
            str(type(self.var_value).__name__),
            str(self.var_value)
        )
