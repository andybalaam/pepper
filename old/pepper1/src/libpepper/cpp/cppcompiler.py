# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


import subprocess

class CppCompiler:
    def __init__( self, sys_op ):
        self.sys_op = sys_op

    def run( self, cpp, exe_out_filename ):
        p = self.sys_op.Popen(
            args = ( "g++", "-x", "c++", "-o", exe_out_filename, "-", ),
            stdin  = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            )

        ( stdout, stderr ) = p.communicate( cpp )

        if p.returncode != 0:
            # TODO: not just a exception
            raise Exception( "Compile error: " + stdout )


