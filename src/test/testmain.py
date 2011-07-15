
from cStringIO import StringIO
from nose.tools import *

from libeeyore.buildsteps.buildstep import BuildStep
from libeeyore.buildsteps.lexbuildstep import LexBuildStep
from libeeyore.buildsteps.parsebuildstep import ParseBuildStep
from libeeyore.buildsteps.renderbuildstep import RenderBuildStep
from libeeyore.buildsteps.sourcebuildstep import SourceBuildStep
from libeeyore.eeyoreoptions import EeyoreOptions
from libeeyore.functionvalues import *
from libeeyore.usererrorexception import EeyUserErrorException
from libeeyore.values import *
from parse import EeyoreLexer

from tokenutils import Iterable2TokenStream, make_token

import libeeyore.main

class FakeObject( object ):
    pass

class FakeBuildStep( BuildStep ):
    def __init__( self, executor, name ):
        self.executor = executor
        self.name = name

    def read_from_file( self, fl ):
        self.executor.calls.append( self.name + ".read_from_file(%s)" % (
            fl.name ) )

    def process( self, inp ):
        self.executor.calls.append( self.name + ".process(inp)" )

    def write_to_file( self, val, fl ):
        self.executor.calls.append( self.name + ".write_to_file(val,%s)" % (
            fl.name ) )

class FakeCppCompiler( object ):
    def __init__( self, executor ):
        self.executor = executor

    def run( self, cpp, exe_filename ):
        self.executor.calls.append( "cppcompiler.run(%s)" % exe_filename )


class FakeCmdRunner( object ):
    def __init__( self, executor ):
        self.executor = executor

    def run( self, exe_filename ):
        self.executor.calls.append( "cmdrunner.run(%s)" % exe_filename )


class FakeExecutor( object ):
    def __init__( self, sys_ops ):
        self.calls = []
        self.build_steps = [
            FakeBuildStep( self, "Source" ),
            FakeBuildStep( self, "Lex" ),
            FakeBuildStep( self, "Parse" ),
            FakeBuildStep( self, "Render" ),
            ]
        self.cppcompiler = FakeCppCompiler( self )
        self.cmdrunner   = FakeCmdRunner( self )


class IdentifiableFakeFile( object ):
    def __init__( self, name ):
        self.name = name

    def __enter__( self ):
        return self

    def __exit__( self, arg1, arg2, arg3 ):
        pass

    def __str__( self ):
        return self.name


class FakeSystemOperations( object ):
    def __init__( self ):
        self.calls = []

    def open_read( self, filename ):
        self.calls.append( "open_read(%s)" % filename )
        return IdentifiableFakeFile( "r" )

    def open_write( self, filename ):
        self.calls.append( "open_write(%s)" % filename )
        return IdentifiableFakeFile( "w" )


class FakeOptions( object ):
    def __init__( self, argv ):
        self.infile = FakeObject()
        self.infile.filetype = EeyoreOptions.PARSE_TREE
        self.infile.filename = "test.eeyoreparsetree"
        self.outfile = FakeObject()
        self.outfile.filetype = EeyoreOptions.CPP
        self.outfile.filename = "test.cpp"

def test_process_options_parse_tree_to_cpp():

    options = FakeOptions( "" )
    file_operations = FakeSystemOperations()
    executor = FakeExecutor( None )

    libeeyore.main.process_options( options, file_operations, executor )

    fo_calls = file_operations.calls

    assert_equal( fo_calls, [
        "open_read(test.eeyoreparsetree)",
        "open_write(test.cpp)"
        ] )

    assert_equal( executor.calls, [
        "Parse.read_from_file(r)",
        "Render.process(inp)",
        "Render.write_to_file(val,w)",
        ] )

class AlwaysThrowUserErrorOptions( object ):
    def __init__( self, argv ):
        raise EeyUserErrorException( "usage: blah" )

def test_parse_and_process_options_arguments_wrong():

    stderr = StringIO()

    ret = libeeyore.main.parse_and_process_options( [],
        AlwaysThrowUserErrorOptions, FakeObject, FakeObject, stderr )

    assert_equal( stderr.getvalue(), "usage: blah\n" )
    assert_equal( ret, 1 )




def test_parse_and_process_options_arguments_right():

    stderr = StringIO()

    ret = libeeyore.main.parse_and_process_options( [],
        FakeOptions, FakeSystemOperations, FakeExecutor, stderr )

    assert_equal( stderr.getvalue(), "" )
    assert_equal( ret, 0 )



def test_process_options_source_to_lexed():

    options = FakeOptions( "" )
    options.infile.filetype = EeyoreOptions.SOURCE
    options.infile.filename = "test.eeyore"
    options.outfile.filetype = EeyoreOptions.LEXED
    options.outfile.filename = "test.eeyorelexed"

    file_operations = FakeSystemOperations()
    executor = FakeExecutor( None )

    libeeyore.main.process_options( options, file_operations, executor )

    fo_calls = file_operations.calls

    assert_equal( fo_calls, [
        "open_read(test.eeyore)",
        "open_write(test.eeyorelexed)"
        ] )

    assert_equal( executor.calls, [
        "Source.read_from_file(r)",
        "Lex.process(inp)",
        "Lex.write_to_file(val,w)",
        ] )


def test_process_options_lexed_to_parsed():

    options = FakeOptions( "" )
    options.infile.filetype = EeyoreOptions.LEXED
    options.infile.filename = "test.eeyorelexed"
    options.outfile.filetype = EeyoreOptions.PARSE_TREE
    options.outfile.filename = "test.eeyoreparsetree"

    file_operations = FakeSystemOperations()
    executor = FakeExecutor( None )

    libeeyore.main.process_options( options, file_operations, executor )

    fo_calls = file_operations.calls

    assert_equal( fo_calls, [
        "open_read(test.eeyorelexed)",
        "open_write(test.eeyoreparsetree)"
        ] )

    assert_equal( executor.calls, [
        "Lex.read_from_file(r)",
        "Parse.process(inp)",
        "Parse.write_to_file(val,w)",
        ] )



def test_process_options_parsed_to_cpp():

    options = FakeOptions( "" )
    options.infile.filetype = EeyoreOptions.PARSE_TREE
    options.infile.filename = "test.eeyoreparsetree"
    options.outfile.filetype = EeyoreOptions.CPP
    options.outfile.filename = "test.cpp"

    file_operations = FakeSystemOperations()
    executor = FakeExecutor( None )

    libeeyore.main.process_options( options, file_operations, executor )

    fo_calls = file_operations.calls

    assert_equal( fo_calls, [
        "open_read(test.eeyoreparsetree)",
        "open_write(test.cpp)"
        ] )

    assert_equal( executor.calls, [
        "Parse.read_from_file(r)",
        "Render.process(inp)",
        "Render.write_to_file(val,w)",
        ] )





def test_process_options_source_to_run():

    options = FakeOptions( "" )
    options.infile.filetype = EeyoreOptions.SOURCE
    options.infile.filename = "test.eeyore"
    options.outfile.filetype = EeyoreOptions.RUN

    file_operations = FakeSystemOperations()
    executor = FakeExecutor( None )

    libeeyore.main.process_options( options, file_operations, executor )

    fo_calls = file_operations.calls

    assert_equal( fo_calls, [
        "open_read(test.eeyore)",
        ] )

    assert_equal( executor.calls, [
        "Source.read_from_file(r)",
        "Lex.process(inp)",
        "Parse.process(inp)",
        "Render.process(inp)",
        "cppcompiler.run(./a.out)",
        "cmdrunner.run(./a.out)",
        ] )



def test_process_options_source_to_exe():

    options = FakeOptions( "" )
    options.infile.filetype = EeyoreOptions.SOURCE
    options.infile.filename = "test.eeyore"
    options.outfile.filetype = EeyoreOptions.EXE
    options.outfile.filename = "test"

    file_operations = FakeSystemOperations()
    executor = FakeExecutor( None )

    libeeyore.main.process_options( options, file_operations, executor )

    fo_calls = file_operations.calls

    assert_equal( fo_calls, [
        "open_read(test.eeyore)",
        ] )

    assert_equal( executor.calls, [
        "Source.read_from_file(r)",
        "Lex.process(inp)",
        "Parse.process(inp)",
        "Render.process(inp)",
        "cppcompiler.run(test)",
        ] )




def test_SourceBuildStep_read_from_file():
    prog = """

    # Comment
print( "Hello, world!" ) # comment 2

    """
    step = SourceBuildStep()
    in_fl = StringIO( prog )

    value = step.read_from_file( in_fl )

    assert_equal( value.getvalue(), prog )




def test_LexBuildStep_read_from_file():

    step = LexBuildStep()
    values = list( step.read_from_file( StringIO( """0001:0001     SYMBOL(print)
0001:0006     LPAREN
0001:0008     STRING(Hello, world!)
0001:0024     RPAREN
""" ) ) )

    assert_equal( values[0].getType(),   EeyoreLexer.SYMBOL )
    assert_equal( values[0].getText(),   "print" )
    assert_equal( values[0].getLine(),   1 )
    assert_equal( values[0].getColumn(), 1 )

    assert_equal( values[1].getType(),   EeyoreLexer.LPAREN )
    assert_equal( values[1].getLine(),   1 )
    assert_equal( values[1].getColumn(), 6 )

    assert_equal( values[2].getType(),   EeyoreLexer.STRING )
    assert_equal( values[2].getText(),   "Hello, world!" )
    assert_equal( values[2].getLine(),   1 )
    assert_equal( values[2].getColumn(), 8 )

    assert_equal( values[3].getType(),   EeyoreLexer.RPAREN )
    assert_equal( values[3].getLine(),   1 )
    assert_equal( values[3].getColumn(), 24 )

    assert_equal( len( values ), 4 )




def test_LexBuildStep_process():

    step = LexBuildStep()
    values = list( step.process( StringIO( """

    # Comment
print( "Hello, world!" ) # comment 2

    """ ) ) )

    assert_equal( values[0].getType(),   EeyoreLexer.SYMBOL )
    assert_equal( values[0].getText(),   "print" )
    assert_equal( values[0].getLine(),   4 )
    assert_equal( values[0].getColumn(), 1 )

    assert_equal( values[1].getType(),   EeyoreLexer.LPAREN )
    assert_equal( values[1].getLine(),   4 )
    assert_equal( values[1].getColumn(), 6 )

    assert_equal( values[2].getType(),   EeyoreLexer.STRING )
    assert_equal( values[2].getText(),   "Hello, world!" )
    assert_equal( values[2].getLine(),   4 )
    assert_equal( values[2].getColumn(), 8 )

    assert_equal( values[3].getType(),   EeyoreLexer.RPAREN )
    assert_equal( values[3].getLine(),   4 )
    assert_equal( values[3].getColumn(), 24 )

    assert_equal( len( values ), 4 )

class FakeToken( object ):
    def __init__( self, tp, text, line, column ):
        self.tp = tp
        self.text = text
        self.line = line
        self.column = column

    def getType( self ):
        return self.tp

    def getText( self ):
        return self.text

    def getLine( self ):
        return self.line

    def getColumn( self ):
        return self.column


def test_LexBuildStep_write_to_file():

    tokens = [
        FakeToken( EeyoreLexer.SYMBOL, "print", 4, 1 ),
        FakeToken( EeyoreLexer.LPAREN, None,    4, 6 ),
        FakeToken( EeyoreLexer.STRING, "Hello", 4, 8 ),
        FakeToken( EeyoreLexer.RPAREN, None,    4, 24 ),
        ]

    out_fl = StringIO()

    step = LexBuildStep()

    step.write_to_file( tokens, out_fl )

    assert_equal( out_fl.getvalue().strip().split( "\n" ), [
        "0004:0001     SYMBOL(print)",
        "0004:0006     LPAREN",
        "0004:0008     STRING(Hello)",
        "0004:0024     RPAREN",
        ] )


def test_ParseBuildStep_read_from_file():

    step = ParseBuildStep()

    in_fl = StringIO( """

    # Comment
    EeyFunctionCall( EeySymbol( "print" ), ( EeyString( "Hello, world!" ), ) ) #com
    """ )

    values = list( step.read_from_file( in_fl ) )

    assert_equal( len( values ), 1 )

    fncall = values[0]
    assert_equal( fncall.__class__, EeyFunctionCall )
    assert_equal( fncall.func_name, "print" )
    func = fncall.func
    assert_equal( func.__class__, EeySymbol )
    assert_equal( func.symbol_name, "print" )
    args = fncall.args
    assert_equal( len( args ), 1 )
    hwstr = args[0]
    assert_equal( hwstr.__class__, EeyString )
    assert_equal( hwstr.value, "Hello, world!" )


def test_ParseBuildStep_process():

    step = ParseBuildStep()

    tokens = Iterable2TokenStream( (
        make_token( "print", EeyoreLexer.SYMBOL, 4, 1 ),
        make_token( "(",     EeyoreLexer.LPAREN, 4, 6 ),
        make_token( "Hello", EeyoreLexer.STRING, 4, 8 ),
        make_token( ")",     EeyoreLexer.RPAREN, 4, 15 ),
        ) )

    values = list( step.process( tokens ) )

    assert_equal( len( values ), 1 )

    fncall = values[0]
    assert_equal( fncall.__class__, EeyFunctionCall )
    assert_equal( fncall.func_name, "print" )
    func = fncall.func
    assert_equal( func.__class__, EeySymbol )
    assert_equal( func.symbol_name, "print" )
    args = fncall.args
    assert_equal( len( args ), 1 )
    hwstr = args[0]
    assert_equal( hwstr.__class__, EeyString )
    assert_equal( hwstr.value, "Hello" )




def test_ParseBuildStep_write_to_file():

    step = ParseBuildStep()

    parsetree = [
        EeyFunctionCall( EeySymbol( 'print' ), (
            EeyString( 'Hello,' ),
            ) ),
        EeyFunctionCall( EeySymbol( 'print' ), (
            EeyString( 'world!' ),
            ) ),
        ]

    out_fl = StringIO()

    step.write_to_file( parsetree, out_fl )

    assert_equal( out_fl.getvalue(),
        """EeyFunctionCall(EeySymbol('print'),(EeyString('Hello,'),))
EeyFunctionCall(EeySymbol('print'),(EeyString('world!'),))
""" )



def test_RenderBuildStep_process():

    step = RenderBuildStep()

    parsetree = [ EeyFunctionCall( EeySymbol( "print" ), (
            EeyString( "Hello, world!" ),
        ) ) ]

    cpp = step.process( parsetree )

    assert_equal( cpp, """#include <stdio.h>

int main( int argc, char* argv[] )
{
    printf( "Hello, world!\\n" );

    return 0;
}
""" )

def test_RenderBuildStep_write_to_file():
    step = RenderBuildStep()
    out_fl = StringIO()
    step.write_to_file( "foobar", out_fl )
    assert_equal( out_fl.getvalue(), "foobar" )


