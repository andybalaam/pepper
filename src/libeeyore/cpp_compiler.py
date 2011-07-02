
import subprocess

def run( cpp, exe_out_filename ):
    p = subprocess.Popen(
        args  = ( "g++", "-x", "c++", "-o", exe_out_filename, "-", ),
        stdin = subprocess.PIPE )

    ( stdout, stderr ) = p.communicate( cpp )

    if p.returncode != 0:
        raise Exception( "Compile error: " + stderr )


