
from nose import SkipTest
from nose.tools import *
from functools import wraps

import textwrap

def skip( t ):
    @wraps( t )
    def wrapper( *args, **kwds ):
        raise SkipTest()
    return wrapper

def _wrap( x ):
    return x

def assert_long_strings_equal( expected, actual ):
    assert_multi_line_equal(
        textwrap.fill( expected ),
        textwrap.fill( actual )
    )

