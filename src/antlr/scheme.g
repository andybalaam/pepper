
options
{
    language = "Python";
}

class SchemeLexer extends Lexer;

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
          { $newline }
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


class SchemeParser extends Parser;

options
{
    buildAST = true;
}

program :
    (expression)*
;

expression :
    LPAREN^
    operator
    (operand)*
    RPAREN!
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


//class SchemeTreeWalker extends TreeParser;
//
//expr returns [r]
//    { r = 0 }
//
//    : #(LPAREN expr..expr)  { r = "x" }
//    | s:SYMBOL { r = "s[" + str( s ) + "]" }
//    | i:INTLIT { r = "i[" + str( i ) + "]" }
//    | p:RPAREN { r = 3 }
//;

