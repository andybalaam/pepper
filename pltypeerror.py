class plTypeError(Exception):
    """
    Raised if some Pepper2Like code fails to pass
    run-time type checks.

    Usually raised by the type_check() function.
    """
    def __init__(self, var_name, actual_type, expected_type, var_value):
        # No type_check here because type_check uses this
        assert type(var_name) == str
        assert type(actual_type) == str
        assert type(expected_type) == str

        self.var_name = var_name
        self.actual_type = actual_type
        self.expected_type = expected_type
        self.var_value = var_value

    def __str__(self):
        return '"%s" was expected to be %s but it is %s.  Value: %s.' % (
            self.var_name,
            self.expected_type,
            self.actual_type,
            repr(self.var_value)
        )
