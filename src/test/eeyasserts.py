# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


def assert_contains( find_in, to_find ):
    if find_in.find( to_find ) != -1:
        return

    raise AssertionError( "'%s' does not contain '%s'" % (
        find_in, to_find ) )


def assert_multiline_equal( str1, str2 ):
    if str1 == str2:
        return

    msg = "%s\n!=\n%s" % ( str1, str2 )

    line = 1
    char = 1
    l1 = len( str1 )
    l2 = len( str2 )
    for i in range( max( l1, l2 ) ):
        if i >= l1 or i >= l2 or str1[i] != str2[i]:
            break
        if str1[i] == "\n":
            line += 1
            char = 1
        else:
            char += 1

    msg += "\nThey differ at line %d, character %d:\n" % ( line, char )
    msg += "%s\n%s\n" % (
        str1.split("\n")[line-1],
        str2.split("\n")[line-1],
        )
    msg += " " * ( char - 1 ) + "^"

    raise AssertionError( msg )

