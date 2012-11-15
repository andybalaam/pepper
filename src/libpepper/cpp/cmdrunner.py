# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


class CmdRunner:
    def __init__( self, sys_op ):
        self.sys_op = sys_op

    def run( self, exe_filename, args ):
        p = self.sys_op.Popen( args  = [ exe_filename, ] + args )

        p.communicate()

        # TODO: handle windows return code?
        return p.returncode


