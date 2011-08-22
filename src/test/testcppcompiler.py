
from nose.tools import *

from libeeyore.cpp.cppcompiler import CppCompiler
from libeeyore.cpp.cmdrunner import CmdRunner


class FakeProcess( object ):
    def __init__( self, sys_op, retcode ):
        self.sys_op = sys_op
        self.returncode = retcode

    def communicate( self, inp = None ):
        if inp is None:
            istr = ""
        else:
            istr = inp
        self.sys_op.calls.append( "communicate(%s)" % istr )
        return "", ""


class FakeSystemOperations( object ):
    def __init__( self, retcode = 0 ):
        self.calls = []
        self.retcode = retcode

    def Popen( self, args, stdin = None, stdout = None, stderr = None ):
        self.calls.append( "Popen(%s)" % ",".join( args ) )
        return FakeProcess( self, self.retcode )


def test_CppCompiler_success():

    fs = FakeSystemOperations()
    c = CppCompiler( fs )
    c.run( "myprog", "testexe" )

    assert_equal( fs.calls, [
        "Popen(g++,-x,c++,-o,testexe,-)",
        "communicate(myprog)",
        ] )

# TODO: not just an exception
@raises( Exception )
def test_CppCompiler_failure():

    fs = FakeSystemOperations( 1 )
    c = CppCompiler( fs )
    c.run( "myprog", "testexe" )


def test_CmdRunner():
    fs = FakeSystemOperations( 3 )
    r = CmdRunner( fs )
    retcode = r.run( "exename", [ "arg1", "arg2" ] )

    assert_equal( fs.calls, [
        "Popen(exename,arg1,arg2)",
        "communicate()",
        ] )

    assert_equal( retcode, 3 )


