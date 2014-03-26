# Copyright (C) 2014 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Ants are creatures of little strength,
#    yet they store up their food in the summer;
# Proverbs 30 v25

from nose.tools import *

from run_snippet import run_snippet


def Run_snippet_runs_single_line__test():
    assert_equal(
        "6",
        run_snippet( """
3*2
        """)
    )


def Run_snippet_can_use_variable__test():
    assert_equal(
        "12",
        run_snippet( """
int x = 3
x*4
        """)
    )


def Run_snippet_can_call_a_function__test():
    assert_equal(
        "24",
        run_snippet( """
def int myfn( int x ):
    return x + 1
6 * myfn( 3 )
        """)
    )

