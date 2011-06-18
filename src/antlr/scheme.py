import sys

from SchemeLexer import Lexer
from SchemeParser import Parser

def parse_file( infl ):

    lexer = Lexer( infl )
    parser = Parser( lexer )
    parser.program();

    parse_tree = parser.getAST()

    print( parse_tree.toStringList() )

    #frame = ASTFrame( "The tree", parse_tree )
    #frame.setVisible( true )

    #ExpressionTreeWalker walker = new ExpressionTreeWalker();
    #double r = walker.expr(parseTree);
    #System.out.println("Value: "+r);

def main( argv ):
    if len( argv ) < 2:
        sys.stderr.write( "You must supply a filename to parse.\n" )
        sys.exit( 1 )

    with file( argv[1] ) as infl:
        parse_file( infl )

if __name__ == "__main__":
    main( sys.argv )
