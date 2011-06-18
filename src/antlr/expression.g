class ExpressionParser extends Parser;

options
{
    buildAST=true;
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

operator :
      SYMBOL
    | expression
;

operand :
            SYMBOL
        | INTLIT
        | STRINGLIT
        | expression
;

//expr     : sumExpr SEMI!;
//sumExpr  : prodExpr ((PLUS^|MINUS^) prodExpr)* ;
//prodExpr : powExpr ((MUL^|DIV^|MOD^) powExpr)* ;
//powExpr  : atom (POW^ atom)? ;
//atom     : INT ;

class ExpressionLexer extends Lexer;

options
{
    charVocabulary = '\0'..'\377';
    testLiterals = false;    // don't automatically test for literals
    k = 2;                   // two characters of lookahead
}

WHITESPACE :
    (
          ' '
        | '\t'
        | '\f'
        | (
              "\r\n"
            | '\r'
            | '\n'
          )
          { newline(); }
    )
    { $setType(Token.SKIP); }
;

COMMENT :
    ";" (~('\n'|'\r'))*
    { $setType(Token.SKIP); }
;

protected DIGIT :
    '0'..'9'
;

INTLIT :
    (DIGIT)+
;

protected QUOTE :
    '"'
;

protected LINEFEED :
    '\r'
;

protected CARRIAGERETURN :
    '\n'
;

STRINGLIT : // TODO: escaped quotes within strings
    QUOTE!
    ( ~( '"'|'\r'|'\n' ) )* // Terminate string on quote or newline
    ( QUOTE! | )              // Fail if there was no " at the end
;

LPAREN :
    '('
;

RPAREN :
    ')'
;

SYMBOL :
    (
          'a'..'z'
        | 'A'..'Z'
        | '_'
        | '-'
        | '+'
        | '='
        | '!'
        | '?'
        // TODO: more
    )+
;


{import java.lang.Math;}
class ExpressionTreeWalker extends TreeParser;

expr returns [double r]
  { double a,b; r=0; }

  : #(PLUS  a=expr b=expr)  { r=a+b; }
  | #(MINUS a=expr b=expr)  { r=a-b; }
  | #(MUL   a=expr b=expr)  { r=a*b; }
  | #(DIV   a=expr b=expr)  { r=a/b; }
  | #(MOD   a=expr b=expr)  { r=a%b; }
  | #(POW   a=expr b=expr)  { r=Math.pow(a,b); }
  | i:INT { r=(double)Integer.parseInt(i.getText()); }
  ;

