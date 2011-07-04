
class CmdRunner:
    def __init__( self, sys_op ):
        self.sys_op = sys_op

    def run( self, exe_filename ):
        p = self.sys_op.Popen( args  = ( exe_filename, ) )

        p.communicate()

        # TODO: handle windows return code?
        return p.returncode


