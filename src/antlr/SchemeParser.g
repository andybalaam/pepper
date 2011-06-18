// A parser for some of the constructs in Scheme
//
// My learning exercise with ANTLR - created as I
// went through Scott Stanchfield's tutorial here:
//
// http://javadude.com/articles/antlrtut/

header
{
//package com.javadude.xl2;
import java.io.*;
import antlr.CommonAST;
import antlr.collections.AST;
import antlr.debug.misc.ASTFrame;
}

class SchemeParser extends Parser;

options
{
    defaultErrorHandler = true; // Don't generate parser error handlers
    buildAST = true;
}


// Define some methods and variables to use in the generated parser.
{
    // Define a main
    public static void main(String[] args) {
        // Use a try/catch block for parser exceptions
        try {
            // if we have at least one command-line argument
            if (args.length > 0 ) {
                System.err.println("Parsing...");

                // for each directory/file specified on the command line
                for(int i=0; i< args.length;i++)
                {
                    doFile(new File(args[i])); // parse it
                }
            }
            else
                System.err.println("Usage: java SchemeParser <directory name>");

        }
        catch(Exception e) {
            System.err.println("exception: "+e);
            e.printStackTrace(System.err);     // so we can get stack trace
        }
    }


    // This method decides what action to take based on the type of
    //     file we are looking at
    public static void doFile(File f) throws Exception {
        // If this is a directory, walk each file/dir in that directory
        if (f.isDirectory()) {
            String files[] = f.list();
            for(int i=0; i < files.length; i++)
                doFile(new File(f, files[i]));
        }

        // otherwise, if this is a java file, parse it!
        else if ((f.getName().length()>5) &&
                         f.getName().endsWith( ".scm" ) ) {
            System.err.println("-------------------------------------------");
            System.err.println(f.getAbsolutePath());
            parseFile(new FileInputStream(f));
        }
	}

    // Here's where we do the real work...
    public static void parseFile(InputStream s) throws Exception {
        try {
            // Create a scanner that reads from the input stream passed to us
            SchemeLexer lexer = new SchemeLexer(s);

            // Create a parser that reads from the scanner
            SchemeParser parser = new SchemeParser(lexer);

            CommonAST parseTree = (CommonAST)parser.getAST();

            // start parsing at the compilationUnit rule
            parser.program();

            System.out.println(parseTree.toStringList());

            ASTFrame frame = new ASTFrame("The tree", parseTree);
            frame.setVisible(true);

            SchemeTreeWalker walker = new SchemeTreeWalker();
            int r = walker.expression( parseTree );
            System.out.println( "Value: " + r );

            //System.out.println( parser.getAST().toString() );
        }
        catch (Exception e) {
            System.err.println("parser exception: "+e);
            e.printStackTrace();     // so we can get stack trace
        }
    }
}


program :
    (expression)*
;

expression :
    LPAREN^
    operator
    (operand)*
    RPAREN
;

operator : (
      s:SYMBOL
    | expression
{
    System.out.println( s.getText() );
})
;

operand : (
            s:SYMBOL
        | INTLIT
        | STRINGLIT
        | expression
{
    System.out.println( s.getText() );
})
;



class SchemeTreeWalker extends TreeParser;

expression returns [int r]
    { int opt, opn; r = 0; }
    : #(LPAREN opt=expression opn=expression) { r=1; }
;


