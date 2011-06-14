// A lexer for some of the constructs in Scheme
//
// My learning exercise with ANTLR - created as I
// went through Scott Stanchfield's tutorial here:
//
// http://javadude.com/articles/antlrtut/

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

