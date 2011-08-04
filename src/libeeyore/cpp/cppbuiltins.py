
from libeeyore.eeyinterface import implements_interface
from libeeyore.values import *
from libeeyore.builtinmodules.eeysys import EeySysArgv


class FormatString( object ):
    def __init__( self, string ):
        self.string = string

    def append( self, to_append ):
        self.string += to_append

    def __str__( self ):
        return self.string

class FormatArgs( object ):
    def __init__( self ):
        self.lst = []

    def append( self, to_append ):
        self.lst.append( to_append )

    def as_list( self ):
        return self.lst


def append_print_arg( fmtstr, fmtargs, env, value ):
    if value.__class__ is EeyString:
        # We don't call render, because we add our own quotes here
        fmtstr.append( value.as_py_str() )
    elif value.__class__ is EeyInt:
        fmtstr.append( "%d" )
        fmtargs.append( value.render( env ) )
    elif value.__class__ is EeyPlus:
        append_print_arg( fmtstr, fmtargs, env, value.left_value )
        append_print_arg( fmtstr, fmtargs, env, value.right_value )
    elif implements_interface( value, EeyString ):
        fmtstr.append( "%s" )
        fmtargs.append( value.render( env ) )
    else:
        raise Exception( "Unknown argument type to print: "
            + str( arg0.__class__ ) )


def render_EeyRuntimePrint( env, value ):
    assert( len( value.args ) == 1 ) # TODO: not an assert
    arg0 = value.args[0]
    #assert( arg0.__class__ is EeyString ) # TODO: not assert, less specific?

    env.renderer.headers.append( "stdio.h" )

    arg0 = arg0.evaluate( env )

    fmtstr = FormatString( '"' )
    fmtargs = FormatArgs()

    append_print_arg( fmtstr, fmtargs, env, arg0 )

    fmtstr.append( '\\n"' )

    ret = 'printf( '
    ret += ", ".join( [ str( fmtstr ) ] + fmtargs.as_list()  )
    ret += " )"

    return ret

def render_EeyRuntimeLen( env, value ):
    arg = value.arg.evaluate( env )
    assert( arg.__class__ == EeySysArgv ) # TODO other types
    return "argc"

