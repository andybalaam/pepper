
import subprocess

def run( exe_filename ):
    p = subprocess.Popen( args  = ( exe_filename, ) )

    p.communicate()

    # TODO: handle windows return code?
    return p.returncode


