
import builtins
import cpp_compiler

from cpp.cpprenderer import EeyCppRenderer
from environment import EeyEnvironment
from parse import EeyoreLexer
from parse import EeyoreParser
from parse import EeyoreTreeWalker

def source_to_exe( source_in_fl, exe_out_filename ):
    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    lexer = EeyoreLexer.Lexer( source_in_fl )

    parser = EeyoreParser.Parser( lexer )
    parser.program();
    walker = EeyoreTreeWalker.Walker()
    eeyoreparsetree = [walker.functionCall( parser.getAST() )]

    cpp = env.render_exe( eeyoreparsetree )

    cpp_compiler.run( cpp, exe_out_filename )

