
from libeeyore.eeyinterface import implements_interface
from libeeyore.builtinmodules.eeysys import EeySysArgv
from libeeyore.vals.all_values import *


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


def append_print_arg( fmtstr, fmtargs, value, env ):

    if value.__class__ is EeyPlus: # TODO: and if an arg is a string
        append_print_arg( fmtstr, fmtargs, value.left_value, env )
        append_print_arg( fmtstr, fmtargs, value.right_value, env )
        return

    if value.is_known( env ):
        cls = value.__class__
    else:
        cls = value.evaluated_type( env ).underlying_class()

    if cls is EeyString:
        # We don't call render, because we add our own quotes here
        fmtstr.append( value.as_py_str() )
    elif cls is EeyInt:
        fmtstr.append( "%d" )
        fmtargs.append( value.render( env ) )
    elif cls is EeyFloat:
        fmtstr.append( "%f" )
        fmtargs.append( value.render( env ) )
        # TODO: format float output better
    elif cls is EeyBool:
        fmtstr.append( "%s" )
        fmtargs.append( '(%s ? "true" : "false")' % value.render( env ) )
    elif implements_interface( value, EeyString ):
        fmtstr.append( "%s" )
        fmtargs.append( value.render( env ) )
    else:
        raise Exception( "Unknown argument type to print: "
            + str( arg0.__class__ ) )


def render_EeyRuntimePrint( value, env ):
    assert( len( value.args ) == 1 ) # TODO: not an assert
    arg0 = value.args[0]
    #assert( arg0.__class__ is EeyString ) # TODO: not assert, less specific?

    env.renderer.add_header( "stdio.h" )

    arg0 = arg0.evaluate( env )

    fmtstr = FormatString( '"' )
    fmtargs = FormatArgs()

    append_print_arg( fmtstr, fmtargs, arg0, env )

    fmtstr.append( '\\n"' )

    ret = 'printf( '
    ret += ", ".join( [ str( fmtstr ) ] + fmtargs.as_list()  )
    ret += " )"

    return ret

def render_EeyRuntimeLen( value, env ):
    arg = value.arg.evaluate( env )
    assert( arg.__class__ == EeySysArgv ) # TODO other types
    return "argc"

