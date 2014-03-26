# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from libpepper.pepinterface import implements_interface
from libpepper.builtinmodules.pepsys import PepSysArgv
from libpepper.vals.all_values import *


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

    if value.__class__ is PepPlus: # TODO: and if an arg is a string
        append_print_arg( fmtstr, fmtargs, value.left_value, env )
        append_print_arg( fmtstr, fmtargs, value.right_value, env )
        return

    cls = value.evaluated_type( env ).underlying_class()

    if cls is PepString:
        # We don't call render, because we add our own quotes here
        fmtstr.append( value.as_py_str() )
    elif cls is PepInt:
        fmtstr.append( "%d" )
        fmtargs.append( value.render( env ) )
    elif cls is PepFloat:
        fmtstr.append( "%f" )
        fmtargs.append( value.render( env ) )
        # TODO: format float output better
    elif cls is PepBool:
        fmtstr.append( "%s" )
        fmtargs.append( '(%s ? "True" : "False")' % value.render( env ) )
    elif implements_interface( value, PepString ):
        fmtstr.append( "%s" )
        fmtargs.append( value.render( env ) )
    else:
        raise Exception( "Unknown argument type to print: "
            + str( arg0.__class__ ) )


def render_PepRuntimePrint( value, env ):
    assert( len( value.args ) == 1 ) # TODO: not an assert
    arg0 = value.args[0]
    #assert( arg0.__class__ is PepString ) # TODO: not assert, less specific?

    env.renderer.add_header( "stdio.h" )

    arg0 = arg0#.evaluate( env )

    fmtstr = FormatString( '"' )
    fmtargs = FormatArgs()

    append_print_arg( fmtstr, fmtargs, arg0, env )

    fmtstr.append( '\\n"' )

    ret = 'printf( '
    ret += ", ".join( [ str( fmtstr ) ] + fmtargs.as_list()  )
    ret += " )"

    return ret

def render_PepRuntimeLen( value, env ):
    if value.arg.evaluated_type( env ).underlying_class() == PepSysArgv:
        return "argc"
    else:
        raise Exception(
            "We don't yet support taking the length of anything"
            + " except sys.argv."
        )

