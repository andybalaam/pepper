# Copyright (C) 2014 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# I praise you, Father, Lord of heaven and earth, because you have hidden
# these things from the wise and learned, and revealed them to little children.
# Luke 10 v21

from nose.tools import *

from run_snippet import run_snippet

def len_argv_can_be_stored_in_a_variable__test():
    """
    At one point, the length of sys.argv could not be stored in a variable.
    Correct behaviour is to render the name of the variable, since the
    value is not known at compile time.
    """

    assert_equal(
        'num_args',
        run_snippet( """
import sys
int num_args = len( sys.argv )
num_args
        """)
    )

