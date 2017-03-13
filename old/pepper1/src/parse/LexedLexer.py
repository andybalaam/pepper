### $ANTLR 2.7.7 (20160104): "lexed.g" -> "LexedLexer.py"$
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
### preamble action >>> 

### preamble action <<< 
### >>>The Literals<<<
literals = {}


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

class Lexer(antlr.CharScanner) :
    ### user action >>>
    ### user action <<<
    def __init__(self, *argv, **kwargs) :
        antlr.CharScanner.__init__(self, *argv, **kwargs)
        self.caseSensitiveLiterals = True
        self.setCaseSensitive(True)
        self.literals = literals
    
    def nextToken(self):
        while True:
            try: ### try again ..
                while True:
                    _token = None
                    _ttype = INVALID_TYPE
                    self.resetText()
                    try: ## for char stream error handling
                        try: ##for lexical error handling
                            la1 = self.LA(1)
                            if False:
                                pass
                            elif la1 and la1 in u':':
                                pass
                                self.mCOLON(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u' ':
                                pass
                                self.mSPACES(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'\n':
                                pass
                                self.mNEWLINE(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'0123456789':
                                pass
                                self.mNUMBER(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                                pass
                                self.mSYMBOL(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'"':
                                pass
                                self.mQUOTED_LITERAL(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'(':
                                pass
                                self.mCONTENT(True)
                                theRetToken = self._returnToken
                            else:
                                    self.default(self.LA(1))
                                
                            if not self._returnToken:
                                raise antlr.TryAgain ### found SKIP token
                            ### return token to caller
                            return self._returnToken
                        ### handle lexical errors ....
                        except antlr.RecognitionException, e:
                            raise antlr.TokenStreamRecognitionException(e)
                    ### handle char stream errors ...
                    except antlr.CharStreamException,cse:
                        if isinstance(cse, antlr.CharStreamIOException):
                            raise antlr.TokenStreamIOException(cse.io)
                        else:
                            raise antlr.TokenStreamException(str(cse))
            except antlr.TryAgain:
                pass
        
    def mDIGIT(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = DIGIT
        _saveIndex = 0
        pass
        self.matchRange(u'0', u'9')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mCOLON(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = COLON
        _saveIndex = 0
        pass
        self.match(':')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mSPACES(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = SPACES
        _saveIndex = 0
        pass
        _cnt5= 0
        while True:
            if (self.LA(1)==u' '):
                pass
                self.match(' ')
            else:
                break
            
            _cnt5 += 1
        if _cnt5 < 1:
            self.raise_NoViableAlt(self.LA(1))
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mNEWLINE(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = NEWLINE
        _saveIndex = 0
        pass
        self.match('\n')
        self.newline();
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mNUMBER(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = NUMBER
        _saveIndex = 0
        pass
        _cnt9= 0
        while True:
            if ((self.LA(1) >= u'0' and self.LA(1) <= u'9')):
                pass
                self.mDIGIT(False)
            else:
                break
            
            _cnt9 += 1
        if _cnt9 < 1:
            self.raise_NoViableAlt(self.LA(1))
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mSYMBOL(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = SYMBOL
        _saveIndex = 0
        pass
        _cnt12= 0
        while True:
            if ((self.LA(1) >= u'A' and self.LA(1) <= u'Z')):
                pass
                self.matchRange(u'A', u'Z')
            else:
                break
            
            _cnt12 += 1
        if _cnt12 < 1:
            self.raise_NoViableAlt(self.LA(1))
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mQUOTED_LITERAL(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = QUOTED_LITERAL
        _saveIndex = 0
        pass
        self.match('"')
        _cnt15= 0
        while True:
            la1 = self.LA(1)
            if False:
                pass
            elif la1 and la1 in u'abcdefghijklmnopqrstuvwxyz':
                pass
                self.matchRange(u'a', u'z')
            elif la1 and la1 in u'_':
                pass
                self.match('_')
            else:
                    break
                
            _cnt15 += 1
        if _cnt15 < 1:
            self.raise_NoViableAlt(self.LA(1))
        self.match('"')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mCONTENT(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = CONTENT
        _saveIndex = 0
        pass
        _saveIndex = self.text.length()
        self.match('(')
        self.text.setLength(_saveIndex)
        while True:
            ###  nongreedy exit test
            if ((self.LA(1)==u')') and (self.LA(2)==u'\n')):
                break
            if ((self.LA(1) >= u'\u0000' and self.LA(1) <= u'\u00ff')) and ((self.LA(2) >= u'\u0000' and self.LA(2) <= u'\u00ff')):
                pass
                self.matchNot(antlr.EOF_CHAR)
            else:
                break
            
        _saveIndex = self.text.length()
        self.match(')')
        self.text.setLength(_saveIndex)
        _saveIndex = self.text.length()
        self.mNEWLINE(False)
        self.text.setLength(_saveIndex)
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    
    
### __main__ header action >>> 
if __name__ == '__main__' :
    import sys
    import antlr
    import LexedLexer
    
    ### create lexer - shall read from stdin
    try:
        for token in LexedLexer.Lexer():
            print token
            
    except antlr.TokenStreamException, e:
        print "error: exception caught while lexing: ", e
### __main__ header action <<< 
