import java.io.*;
import antlr.CommonAST;
import antlr.collections.AST;
import antlr.debug.misc.ASTFrame;
public class Main
{
    public static void main(String args[])
    {
        try
        {
            FileInputStream input = new FileInputStream( args[0] );

            ExpressionLexer lexer = new ExpressionLexer( input );

            ExpressionParser parser = new ExpressionParser( lexer );
            parser.program();

            CommonAST parseTree = (CommonAST)parser.getAST();
            System.out.println( parseTree.toStringList() );
            ASTFrame frame = new ASTFrame( "The tree", parseTree );
            frame.setVisible( true );

            //ExpressionTreeWalker walker = new ExpressionTreeWalker();
            //double r = walker.expr(parseTree);
            //System.out.println("Value: "+r);
        }
        catch( Exception e )
        {
            e.printStackTrace();
        }
    }
}

