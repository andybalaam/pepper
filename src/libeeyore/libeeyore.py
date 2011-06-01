
class CppEnvironment( dict ):
	pass

class CppRenderer( object ):
	def __init__( self ):
		self.includes = set()
		self.maincode = ""
		self.mainfront = ""
		self.environment = CppEnvironment()
		self.indent = "    "

	def add_maincode( self, cpp ):
		self.maincode += self.indent
		self.maincode += cpp

	def add_mainfront( self, name, cpp ):
		# TODO check whether name is already done
		self.mainfront += cpp

	def add_include( self, header ):
		self.includes.add( header )

	def render( self ):
		ret = "\n".join( "#include <%s>" % h for h in self.includes )
		ret += """

int main( int argc, char* argv[] )
{
%s%s}""" % ( self.mainfront, self.maincode )

		return ret

	def render_var( self, var ):
		if is_known( var ):
			return '"%s"' % var.p_str()
		else:
			return var.var_name()


#class EeySymbol( object ):
#	def __init__( self, symbol_name ):
#		self.symbol_name = symbol_name
#
#
#class EeyInt( object ):
#	def __init__( self, strvalue ):
#		self.value = int( strvalue )
#
#	def p_int( self ):
#		return self.value
#
#	def p_str( self ):
#		return str( self.value )
#
#	def is_known( self ):
#		return True
#
#class EeyString( object ):
#	def __init__( self, strvalue ):
#		self.value = strvalue
#
#	def p_str( self ):
#		return self.value
#
#	def is_known( self ):
#		return True
#
#class EeyQuoted( object ):
#	def __init__( self, strcode ):
#		self.strcode = strcode
#
class CArray( object ):
	def __init__( self, lengthvar, arrayvar ):
		self.lengthvar = lengthvar
		self.arrayvar = arrayvar

	def lookup( self, index ):
		# TODO: check bounds
		return "%s[%s]" % ( arrayvar, index )

	def is_known( self ):
		return False

cpprenderer = CppRenderer()

def main( arg ):
	global cpprenderer
	cpprenderer.add_maincode( "return 0;\n" )

def is_known( var ):
	return var.is_known()

def eprint( value ):
	global cpprenderer
	cpprenderer.add_include( "stdio.h" )
	cpprenderer.add_maincode( 'printf( "%%d\\n", %s );\n' % value.p_str() )
	return None

def add_known( value1, value2 ):
	if is_int( value1 ) and is_int( value2 ):
		return eint( value1.p_int() + value2.p_int() )
	else:
		return estring( value1.p_str() + value2.p_str() )

def add_nonc( value1, value2 ):
	global cpprenderer
	cpprenderer.add_maincode( "eeyore_string_concat( %s, %s );\n" % (
		cpprenderer.render_var( value1 ), cpprenderer.render_var( value2 ) ) )

def add( value1, value2 ):
	if is_known( value1 ) and is_known( value2 ):
		return add_known( value1, value2 )
	else:
		return add_nonc( value1, value2 )

def eint( strvalue ):
	return EeyInt( strvalue )

def estring( strvalue ):
	return EeyString( strvalue )

def earraylookup( array, index ):
	return array.lookup( index )

def var( varname ):
	global cpprenderer
	if varname not in cpprenderer.environment:
		raise Exception( "Name '%s' not found!" % varname )
	return cpprenderer.environment[varname]

def greater_than_or_equal( value1, value2 ):
	global cpprenderer
	cpprenderer.add_maincode( "( %s >= %s )" % (#
		cpprenderer.render_var( value1 ),
		cpprenderer.render_var( value2 ) ) )

def elen( value ):
	return value.length()

def eimport( module_name ):
	execfile( "libeeyore/e%s.parsetree" % module_name )

def defvar( modname, strname, code ):
	global cpprenderer
	cpprenderer.environment[ "%s.%s" % ( modname, strname ) ] = code

def quote( code ):
	return EeyQuoted( code )

def carray( cppname_length, cppname_array ):
	return CArray( cppname_length, cppname_array )

def eif( pred, truevalue ):
	global cpprenderer
	cpprenderer.add_maincode( "if ( %s ) { %s }" % ( pred, truevalue ) )

