
class CppEnvironment( object ):
	pass

class CppRenderer( object ):
	def __init__( self ):
		self.includes = set()
		self.maincode = ""
		self.environment = CppEnvironment()
		self.indent = "    "

	def add_maincode( self, cpp ):
		self.maincode += self.indent
		self.maincode += cpp

	def add_include( self, header ):
		self.includes.add( header )

	def render( self ):
		ret = "\n".join( "#include <%s>" % h for h in self.includes )
		ret += """

int main( int argc, char* argv[] )
{
%s}""" % self.maincode

		return ret

class EeyInt( object ):
	def __init__( self, strvalue ):
		self.value = int( strvalue )

	def p_int( self ):
		return self.value

	def p_str( self ):
		return str( self.value )


cpprenderer = CppRenderer()

def main( arg ):
	global cpprenderer
	cpprenderer.add_maincode( "return 0;\n" )

def eprint( value ):
	global cpprenderer
	cpprenderer.add_include( "stdio.h" )
	cpprenderer.add_maincode( 'printf( "%%d\\n", %s );\n' % value.p_str() )
	return None

def add( value1, value2 ):
	return eint( value1.p_int() + value2.p_int() )

def eint( strvalue ):
	return EeyInt( strvalue )


