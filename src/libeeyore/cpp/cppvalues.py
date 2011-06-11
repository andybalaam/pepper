
from cppbuiltins import *
from libeeyore.builtins import *
from libeeyore.functionvalues import *
from libeeyore.languagevalues import *
from libeeyore.values import *

def render_EeySymbol( env, value ):
	return value.name()

def render_EeyInt( env, value ):
	return str( value.value )

def render_EeyString( env, value ):
	return '"%s"' % value.value

def render_EeyPlus( env, value ):
	return "(%s + %s)" % (
		value.left_value.render( env ), value.right_value.render( env ) )

def render_EeyFunction( env, value ):
	raise Exception( "Don't know how to render a function yet" )

def render_EeyPrint( env, value ):
	return render_EeyFunction( env, value )

def render_EeyDefine( env, value ):
	return ""

def render_EeyPass( env, value ):
	return ""


type2string = {
	EeyInt : "int",
	}

def render_EeyType( env, value ):
	return type2string[value.value]



def render_type_and_name( env, typename ):
	return "%s %s" % ( render_EeyType( env, typename[0] ),
		typename[1].symbol_name )

def render_EeyUserFunction_body( env, func_call ):
	fn = func_call.func.evaluate( env )

	assert( fn.__class__ == EeyUserFunction ) # TODO: handle other types

	ret = fn.ret_type.render( env )
	ret += " "
	ret += func_call.func_name
	ret += "( "
	ret += ", ".join( render_type_and_name( env, typename ) for typename
		in fn.arg_types_and_names )
	ret += " )\n{\n"

	newenv = fn.execution_environment( env, func_call.args, False )

	# TODO: not every statement should be a return
	for body_stmt in fn.body_stmts:
		ret += "\treturn %s;\n" % body_stmt.render( newenv )

	ret += "}\n"

	return ret

def render_EeyFunctionCall( env, value ):

	env.renderer.functions.append( render_EeyUserFunction_body(
		env, value ) )

	return ( value.func_name + "( " +
		", ".join( arg.render( env ) for arg in value.args )
		+ " )" )

def render_EeyReturn( env, value ):
	return "return " + value.value.render( env )


type2renderer = {
	EeyDefine       : render_EeyDefine,
	EeyFunction     : render_EeyFunction,
	EeyFunctionCall : render_EeyFunctionCall,
	EeyInt          : render_EeyInt,
	EeyPass         : render_EeyPass,
	EeyPlus         : render_EeyPlus,
	EeyPrint        : render_EeyPrint,
	EeyReturn       : render_EeyReturn,
	EeyRuntimePrint : render_EeyRuntimePrint,
	EeyString       : render_EeyString,
	EeySymbol       : render_EeySymbol,
	EeyType         : render_EeyType,
	}

