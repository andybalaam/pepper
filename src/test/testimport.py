# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.environment import EeyEnvironment
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import EeyCppRenderer

from eeyasserts import *

def test_import_sys_copyright():
    env = EeyEnvironment( EeyCppRenderer() )

    assert_equal( EeyImport( "sys" ).render( env ), "" )

    cpy = EeySymbol( "sys.copyright" ).render( env )

    assert_contains( cpy, "Copyright" )
    assert_contains( cpy, "Andy Balaam" )


def test_define_module():
    pass

