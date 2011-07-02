
def assert_contains( find_in, to_find ):
    if find_in.find( to_find ) != -1:
        return

    raise AssertionError( "'%s' does not contain '%s'" % (
        find_in, to_find ) )
