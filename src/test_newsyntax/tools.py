
from nose import SkipTest
from nose.tools import *
from functools import wraps

def skip( t ):
    @wraps( t )
    def wrapper( *args, **kwds ):
        raise SkipTest()
    return wrapper

