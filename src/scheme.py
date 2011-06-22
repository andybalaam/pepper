import sys

from parse.EeyoreLexer import Lexer
from parse.EeyoreParser import Parser
#from parse.EeyoreTreeWalker import Walker

def display_ast( node, indent ):
    if node is None:
        return

    print " " * indent, node.getType(), node.getText()

    display_ast( node.getFirstChild(), indent + 4 )
    display_ast( node.getNextSibling(), indent )

def parse_file( infl ):

    lexer = Lexer( infl )
    parser = Parser( lexer )
    parser.program();

    parse_tree = parser.getAST()

    #print( parse_tree.toStringTree() )

    display_ast( parse_tree, 0 )

    #frame = ASTFrame( "The tree", parse_tree )
    #frame.setVisible( true )

    #walker = Walker()
    #value = walker.expr( parse_tree )
    #print( value )

def main( argv ):
    if len( argv ) < 2:
        sys.stderr.write( "You must supply a filename to parse.\n" )
        sys.exit( 1 )

    with file( argv[1] ) as infl:
        parse_file( infl )

if __name__ == "__main__":
    main( sys.argv )
