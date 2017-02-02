# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.environment import PepEnvironment
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import PepCppRenderer

from pepasserts import *

def test_import_sys_copyright():
    env = PepEnvironment( PepCppRenderer() )

    assert_equal( PepImport( "sys" ).render( env ), "" )

    cpy = PepSymbol( "sys.copyright" ).render( env )

    assert_contains( cpy, "Copyright" )
    assert_contains( cpy, "Andy Balaam" )


def test_define_module():
    pass

