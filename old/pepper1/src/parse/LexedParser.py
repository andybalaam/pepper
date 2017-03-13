### $ANTLR 2.7.7 (20160104): "lexed.g" -> "LexedParser.py"$
### import antlr and other modules ..
import sys
import antlr

version = sys.version.split()[0]
if version < '2.2.1':
    False = 0
if version < '2.3':
    True = not False
### header action >>> 

### header action <<< 
### preamble action>>>

### preamble action <<<

### import antlr.Token 
from antlr import Token
### >>>The Known Token Types <<<
SKIP                = antlr.SKIP
INVALID_TYPE        = antlr.INVALID_TYPE
EOF_TYPE            = antlr.EOF_TYPE
EOF                 = antlr.EOF
NULL_TREE_LOOKAHEAD = antlr.NULL_TREE_LOOKAHEAD
MIN_USER_TYPE       = antlr.MIN_USER_TYPE
DIGIT = 4
COLON = 5
SPACES = 6
NEWLINE = 7
NUMBER = 8
SYMBOL = 9
QUOTED_LITERAL = 10
CONTENT = 11

class Parser(antlr.LLkParser):
    ### user action >>>
    ### user action <<<
    
    def __init__(self, *args, **kwargs):
        antlr.LLkParser.__init__(self, *args, **kwargs)
        self.tokenNames = _tokenNames
        
    def tokenName(self):    
        t = None
        
        s = None
        l = None
        pass
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [SYMBOL]:
            pass
            s = self.LT(1)
            self.match(SYMBOL)
            t=s
        elif la1 and la1 in [QUOTED_LITERAL]:
            pass
            l = self.LT(1)
            self.match(QUOTED_LITERAL)
            t=l
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        return t
    
    def line(self):    
        t = None
        
        linenum = None
        colnum = None
        content = None
        try:      ## for error handling
            pass
            linenum = self.LT(1)
            self.match(NUMBER)
            self.match(COLON)
            colnum = self.LT(1)
            self.match(NUMBER)
            self.match(SPACES)
            symbol=self.tokenName()
            la1 = self.LA(1)
            if False:
                pass
            elif la1 and la1 in [CONTENT]:
                pass
                content = self.LT(1)
                self.match(CONTENT)
            elif la1 and la1 in [NEWLINE]:
                pass
                self.match(NEWLINE)
            else:
                    raise antlr.NoViableAltException(self.LT(1), self.getFilename())
                
            from antlr import CommonToken
            import PepperParser
            t = CommonToken(
               type = PepperParser._tokenNames.index( symbol.getText() ) )
            if content is not None:
               t.setText( content.getText() )
            t.setLine( int( linenum.getText() ) )
            t.setColumn( int( colnum.getText() ) )
        
        except antlr.RecognitionException, ex:
            return None
        return t
    

_tokenNames = [
    "<0>", 
    "EOF", 
    "<2>", 
    "NULL_TREE_LOOKAHEAD", 
    "DIGIT", 
    "COLON", 
    "SPACES", 
    "NEWLINE", 
    "NUMBER", 
    "SYMBOL", 
    "QUOTED_LITERAL", 
    "CONTENT"
]
    
    
