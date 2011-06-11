
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

from eeyasserts import *

def test_import_sys_copyright():
	env = EeyEnvironment( EeyCppRenderer() )

	assert_equal( EeyImport( "sys" ).render( env ), "" )

	cpy = EeySymbol( "sys.copyright" ).render( env )

	assert_contains( cpy, "Copyright" )
	assert_contains( cpy, "Andy Balaam" )


def test_define_module():
	pass

