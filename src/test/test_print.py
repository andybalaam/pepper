# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from assert_rendered_cpp_equals import assert_rendered_cpp_equals

def Adding_known_to_unknown_via_real_parser___test():
    assert_rendered_cpp_equals(
        r"""printf( "A%sB\n", argv[1] )""",
        r"""print( "A" + sys.argv[1] + "B" )"""
    )


def Adding_known_to_unknown_numbers___test():
    assert_rendered_cpp_equals(
        r"""printf( "A%dB\n", argc )""",
        r"""print( "A" + len( sys.argv ) + "B" )"""
    )


# TODO: FAILS because print mistakenly breaks up subexpression
#def Adding_known_to_unknown_expression___test():
#    assert_rendered_cpp_equals(
#        r"""printf( "A%d\n", (1 + argc) )""",
#        r"""print( "A" + ( 1 + len( sys.argv ) ) )"""
#    )


# TODO: FAILS to parse because we can't have a subexpression on the
#       left of another expression.
#def Adding_known_to_unknown_expression___test():
#    assert_rendered_cpp_equals(
#        r"""printf( "A%dB\n", (1 + argc) )""",
#        r"""print( "A" + ( 1 + len( sys.argv ) ) + "B" )"""
#    )


