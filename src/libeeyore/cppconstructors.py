from cppvalues import *

def esymbol( env, symbol_name ):
	return EeyCppSymbol( env, symbol_name )


def eint( env, strint ):
	return EeyCppInt( env, int( strint ) )



def estring( env, strvalue ):
	return EeyCppString( env, strvalue )

