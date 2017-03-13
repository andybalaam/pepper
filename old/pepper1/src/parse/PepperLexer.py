### $ANTLR 2.7.7 (20160104): "pepper.g" -> "PepperLexer.py"$
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
literals[u"if"] = 45
literals[u"for"] = 41
literals[u"quote"] = 47
literals[u"class"] = 39
literals[u"while"] = 43
literals[u"var"] = 48
literals[u"def"] = 37
literals[u"in"] = 42
literals[u"else"] = 46
literals[u"import"] = 44
literals[u"interface"] = 40
literals[u"return"] = 49
literals[u"def_init"] = 38


### import antlr.Token 
from antlr import Token
### >>>The Known Token Types <<<
SKIP                = antlr.SKIP
INVALID_TYPE        = antlr.INVALID_TYPE
EOF_TYPE            = antlr.EOF_TYPE
EOF                 = antlr.EOF
NULL_TREE_LOOKAHEAD = antlr.NULL_TREE_LOOKAHEAD
MIN_USER_TYPE       = antlr.MIN_USER_TYPE
INDENT = 4
DEDENT = 5
WHITESPACE = 6
LEADINGSP = 7
COMMENT = 8
DIGIT = 9
DIGITS = 10
INT = 11
FLOAT = 12
INT_OR_FLOAT = 13
TRIPLEDOUBLEQUOTE = 14
DOUBLEQUOTE = 15
DOUBLEQUOTESTRING = 16
TRIPLEDOUBLEQUOTESTRING = 17
STRING = 18
LPAREN = 19
RPAREN = 20
LSQUBR = 21
RSQUBR = 22
COMMA = 23
STARTSYMBOLCHAR = 24
MIDSYMBOLCHAR = 25
SYMBOL_EL = 26
SYMBOL = 27
NEWLINE = 28
PLUS = 29
MINUS = 30
TIMES = 31
PLUSEQUALS = 32
GT = 33
LT = 34
COLON = 35
EQUALS = 36
LITERAL_def = 37
LITERAL_def_init = 38
LITERAL_class = 39
LITERAL_interface = 40
LITERAL_for = 41
LITERAL_in = 42
LITERAL_while = 43
LITERAL_import = 44
LITERAL_if = 45
LITERAL_else = 46
LITERAL_quote = 47
LITERAL_var = 48
LITERAL_return = 49

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
                            elif la1 and la1 in u'#':
                                pass
                                self.mCOMMENT(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'.0123456789':
                                pass
                                self.mINT_OR_FLOAT(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'"':
                                pass
                                self.mSTRING(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'(':
                                pass
                                self.mLPAREN(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u')':
                                pass
                                self.mRPAREN(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'[':
                                pass
                                self.mLSQUBR(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u']':
                                pass
                                self.mRSQUBR(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u',':
                                pass
                                self.mCOMMA(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz':
                                pass
                                self.mSYMBOL(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'\n\r':
                                pass
                                self.mNEWLINE(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'-':
                                pass
                                self.mMINUS(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'*':
                                pass
                                self.mTIMES(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'>':
                                pass
                                self.mGT(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'<':
                                pass
                                self.mLT(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u':':
                                pass
                                self.mCOLON(True)
                                theRetToken = self._returnToken
                            elif la1 and la1 in u'=':
                                pass
                                self.mEQUALS(True)
                                theRetToken = self._returnToken
                            else:
                                if (self.LA(1)==u'+') and (self.LA(2)==u'='):
                                    pass
                                    self.mPLUSEQUALS(True)
                                    theRetToken = self._returnToken
                                elif ((self.LA(1)==u' ') and (True) and ( self.getColumn() > 1 )):
                                    pass
                                    self.mWHITESPACE(True)
                                    theRetToken = self._returnToken
                                elif (self.LA(1)==u' ') and (True):
                                    pass
                                    self.mLEADINGSP(True)
                                    theRetToken = self._returnToken
                                elif (self.LA(1)==u'+') and (True):
                                    pass
                                    self.mPLUS(True)
                                    theRetToken = self._returnToken
                                else:
                                    self.default(self.LA(1))
                                
                            if not self._returnToken:
                                raise antlr.TryAgain ### found SKIP token
                            ### option { testLiterals=true } 
                            self.testForLiteral(self._returnToken)
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
        
    def mWHITESPACE(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = WHITESPACE
        _saveIndex = 0
        if not  self.getColumn() > 1 :
            raise antlr.SemanticException(" self.getColumn() > 1 ")
        pass
        pass
        self.match(' ')
        if not self.inputState.guessing:
            _ttype = Token.SKIP;
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mLEADINGSP(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = LEADINGSP
        _saveIndex = 0
        pass
        if not self.inputState.guessing:
            self.getColumn() == 1
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
    
    def mCOMMENT(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = COMMENT
        _saveIndex = 0
        pass
        self.match("#")
        while True:
            if (_tokenSet_0.member(self.LA(1))):
                pass
                self.match(_tokenSet_0)
            else:
                break
            
        if not self.inputState.guessing:
            _ttype = Token.SKIP;
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mDIGIT(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = DIGIT
        _saveIndex = 0
        pass
        self.matchRange(u'0', u'9')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mDIGITS(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = DIGITS
        _saveIndex = 0
        pass
        _cnt13= 0
        while True:
            if ((self.LA(1) >= u'0' and self.LA(1) <= u'9')):
                pass
                self.mDIGIT(False)
            else:
                break
            
            _cnt13 += 1
        if _cnt13 < 1:
            self.raise_NoViableAlt(self.LA(1))
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mINT(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = INT
        _saveIndex = 0
        pass
        self.mDIGITS(False)
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mFLOAT(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = FLOAT
        _saveIndex = 0
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in u'.':
            pass
            self.match('.')
            self.mDIGITS(False)
        elif la1 and la1 in u'0123456789':
            pass
            self.mDIGITS(False)
            self.match('.')
            if ((self.LA(1) >= u'0' and self.LA(1) <= u'9')):
                pass
                self.mDIGITS(False)
            else: ## <m4>
                    pass
                
        else:
                self.raise_NoViableAlt(self.LA(1))
            
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mINT_OR_FLOAT(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = INT_OR_FLOAT
        _saveIndex = 0
        synPredMatched19 = False
        if (_tokenSet_1.member(self.LA(1))) and (_tokenSet_1.member(self.LA(2))):
            _m19 = self.mark()
            synPredMatched19 = True
            self.inputState.guessing += 1
            try:
                pass
                self.mINT(False)
                self.match('.')
            except antlr.RecognitionException, pe:
                synPredMatched19 = False
            self.rewind(_m19)
            self.inputState.guessing -= 1
        if synPredMatched19:
            pass
            self.mFLOAT(False)
            if not self.inputState.guessing:
                _ttype = FLOAT
        else:
            synPredMatched21 = False
            if (_tokenSet_1.member(self.LA(1))) and (_tokenSet_1.member(self.LA(2))):
                _m21 = self.mark()
                synPredMatched21 = True
                self.inputState.guessing += 1
                try:
                    pass
                    self.match('.')
                except antlr.RecognitionException, pe:
                    synPredMatched21 = False
                self.rewind(_m21)
                self.inputState.guessing -= 1
            if synPredMatched21:
                pass
                self.mFLOAT(False)
                if not self.inputState.guessing:
                    _ttype = FLOAT
            elif ((self.LA(1) >= u'0' and self.LA(1) <= u'9')) and (True):
                pass
                self.mINT(False)
                if not self.inputState.guessing:
                    _ttype = INT
            else:
                self.raise_NoViableAlt(self.LA(1))
            
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mTRIPLEDOUBLEQUOTE(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = TRIPLEDOUBLEQUOTE
        _saveIndex = 0
        pass
        self.match('"')
        self.match('"')
        self.match('"')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mDOUBLEQUOTE(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = DOUBLEQUOTE
        _saveIndex = 0
        pass
        self.match('"')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mDOUBLEQUOTESTRING(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = DOUBLEQUOTESTRING
        _saveIndex = 0
        pass
        _saveIndex = self.text.length()
        self.mDOUBLEQUOTE(False)
        self.text.setLength(_saveIndex)
        while True:
            if (_tokenSet_2.member(self.LA(1))):
                pass
                self.match(_tokenSet_2)
            else:
                break
            
        _saveIndex = self.text.length()
        self.mDOUBLEQUOTE(False)
        self.text.setLength(_saveIndex)
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mTRIPLEDOUBLEQUOTESTRING(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = TRIPLEDOUBLEQUOTESTRING
        _saveIndex = 0
        pass
        _saveIndex = self.text.length()
        self.mTRIPLEDOUBLEQUOTE(False)
        self.text.setLength(_saveIndex)
        while True:
            ###  nongreedy exit test
            if ((self.LA(1)==u'"') and (self.LA(2)==u'"')):
                break
            if ((self.LA(1) >= u'\u0000' and self.LA(1) <= u'\u00ff')) and ((self.LA(2) >= u'\u0000' and self.LA(2) <= u'\u00ff')):
                pass
                self.matchNot(antlr.EOF_CHAR)
            else:
                break
            
        _saveIndex = self.text.length()
        self.mTRIPLEDOUBLEQUOTE(False)
        self.text.setLength(_saveIndex)
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mSTRING(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = STRING
        _saveIndex = 0
        pass
        if (self.LA(1)==u'"') and (self.LA(2)==u'"'):
            pass
            self.mTRIPLEDOUBLEQUOTESTRING(False)
        elif (self.LA(1)==u'"') and ((self.LA(2) >= u'\u0000' and self.LA(2) <= u'\u00ff')):
            pass
            self.mDOUBLEQUOTESTRING(False)
        else:
            self.raise_NoViableAlt(self.LA(1))
        
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mLPAREN(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = LPAREN
        _saveIndex = 0
        pass
        self.match('(')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mRPAREN(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = RPAREN
        _saveIndex = 0
        pass
        self.match(')')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mLSQUBR(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = LSQUBR
        _saveIndex = 0
        pass
        self.match("[")
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mRSQUBR(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = RSQUBR
        _saveIndex = 0
        pass
        self.match("]")
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mCOMMA(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = COMMA
        _saveIndex = 0
        pass
        self.match(',')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mSTARTSYMBOLCHAR(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = STARTSYMBOLCHAR
        _saveIndex = 0
        pass
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in u'abcdefghijklmnopqrstuvwxyz':
            pass
            self.matchRange(u'a', u'z')
        elif la1 and la1 in u'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            pass
            self.matchRange(u'A', u'Z')
        elif la1 and la1 in u'_':
            pass
            self.match('_')
        else:
                self.raise_NoViableAlt(self.LA(1))
            
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mMIDSYMBOLCHAR(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = MIDSYMBOLCHAR
        _saveIndex = 0
        pass
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in u'abcdefghijklmnopqrstuvwxyz':
            pass
            self.matchRange(u'a', u'z')
        elif la1 and la1 in u'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            pass
            self.matchRange(u'A', u'Z')
        elif la1 and la1 in u'0123456789':
            pass
            self.matchRange(u'0', u'9')
        elif la1 and la1 in u'_':
            pass
            self.match('_')
        else:
                self.raise_NoViableAlt(self.LA(1))
            
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mSYMBOL_EL(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = SYMBOL_EL
        _saveIndex = 0
        pass
        self.mSTARTSYMBOLCHAR(False)
        while True:
            if (_tokenSet_3.member(self.LA(1))):
                pass
                self.mMIDSYMBOLCHAR(False)
            else:
                break
            
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mSYMBOL(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = SYMBOL
        _saveIndex = 0
        pass
        self.mSYMBOL_EL(False)
        while True:
            if (self.LA(1)==u'.'):
                pass
                self.match(".")
                self.mSYMBOL_EL(False)
            else:
                break
            
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mNEWLINE(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = NEWLINE
        _saveIndex = 0
        if (self.LA(1)==u'\r') and (self.LA(2)==u'\n'):
            pass
            self.match("\r\n")
        elif (self.LA(1)==u'\r') and (True):
            pass
            self.match('\r')
        elif (self.LA(1)==u'\n'):
            pass
            self.match('\n')
            if not self.inputState.guessing:
                self.newline()
        else:
            self.raise_NoViableAlt(self.LA(1))
        
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mPLUS(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = PLUS
        _saveIndex = 0
        pass
        self.match('+')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mMINUS(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = MINUS
        _saveIndex = 0
        pass
        self.match('-')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mTIMES(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = TIMES
        _saveIndex = 0
        pass
        self.match('*')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mPLUSEQUALS(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = PLUSEQUALS
        _saveIndex = 0
        pass
        self.match("+=")
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mGT(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = GT
        _saveIndex = 0
        pass
        self.match('>')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    def mLT(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = LT
        _saveIndex = 0
        pass
        self.match('<')
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
    
    def mEQUALS(self, _createToken):    
        _ttype = 0
        _token = None
        _begin = self.text.length()
        _ttype = EQUALS
        _saveIndex = 0
        pass
        self.match('=')
        self.set_return_token(_createToken, _token, _ttype, _begin)
    
    

### generate bit set
def mk_tokenSet_0(): 
    data = [0L] * 8 ### init list
    data[0] =-9217L
    for x in xrange(1, 4):
        data[x] = -1L
    return data
_tokenSet_0 = antlr.BitSet(mk_tokenSet_0())

### generate bit set
def mk_tokenSet_1(): 
    ### var1
    data = [ 288019269919178752L, 0L, 0L, 0L, 0L]
    return data
_tokenSet_1 = antlr.BitSet(mk_tokenSet_1())

### generate bit set
def mk_tokenSet_2(): 
    data = [0L] * 8 ### init list
    data[0] =-17179869185L
    for x in xrange(1, 4):
        data[x] = -1L
    return data
_tokenSet_2 = antlr.BitSet(mk_tokenSet_2())

### generate bit set
def mk_tokenSet_3(): 
    ### var1
    data = [ 287948901175001088L, 576460745995190270L, 0L, 0L, 0L]
    return data
_tokenSet_3 = antlr.BitSet(mk_tokenSet_3())
    
### __main__ header action >>> 
if __name__ == '__main__' :
    import sys
    import antlr
    import PepperLexer
    
    ### create lexer - shall read from stdin
    try:
        for token in PepperLexer.Lexer():
            print token
            
    except antlr.TokenStreamException, e:
        print "error: exception caught while lexing: ", e
### __main__ header action <<< 
