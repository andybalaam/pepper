### $ANTLR 2.7.7 (20160104): "newsyntaxpepper.g" -> "NewSyntaxPepperTreeWalker.py"$
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

### import antlr.Token 
from antlr import Token
### >>>The Known Token Types <<<
SKIP                = antlr.SKIP
INVALID_TYPE        = antlr.INVALID_TYPE
EOF_TYPE            = antlr.EOF_TYPE
EOF                 = antlr.EOF
NULL_TREE_LOOKAHEAD = antlr.NULL_TREE_LOOKAHEAD
MIN_USER_TYPE       = antlr.MIN_USER_TYPE
WHITESPACE = 4
COMMENT = 5
DIGIT = 6
DIGITS = 7
INT = 8
DOT = 9
FLOAT = 10
INT_OR_DOT_OR_FLOAT = 11
TRIPLEDOUBLEQUOTE = 12
DOUBLEQUOTE = 13
DOUBLEQUOTESTRING = 14
TRIPLEDOUBLEQUOTESTRING = 15
STRING = 16
LBRACE = 17
RBRACE = 18
PIPE = 19
LPAREN = 20
RPAREN = 21
LSQUBR = 22
RSQUBR = 23
COMMA = 24
SEMICOLON = 25
STARTSYMBOLCHAR = 26
MIDSYMBOLCHAR = 27
SYMBOL = 28
PLUS = 29
MINUS = 30
TIMES = 31
PLUSEQUALS = 32
GT = 33
LT = 34
COLON = 35
EQUALS = 36
EQUALSEQUALS = 37
LITERAL_def = 38
LITERAL_def_init = 39
LITERAL_class = 40
LITERAL_interface = 41
LITERAL_while = 42
LITERAL_import = 43
LITERAL_quote = 44
NEWLINE = 45
INDENT = 46
DEDENT = 47
LITERAL_var = 48
LITERAL_return = 49

### user code>>>
from libpepper.vals.all_values import *
### user code<<<

class Walker(antlr.TreeParser):
    
    # ctor ..
    def __init__(self, *args, **kwargs):
        antlr.TreeParser.__init__(self, *args, **kwargs)
        self.tokenNames = _tokenNames
    
    ### user action >>>
    ### user action <<<
    def statement(self, _t):    
        r = None
        
        statement_AST_in = None
        if _t != antlr.ASTNULL:
            statement_AST_in = _t
        try:      ## for error handling
            if not _t:
                _t = antlr.ASTNULL
            la1 = _t.getType()
            if False:
                pass
            elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,GT,LT,LITERAL_quote]:
                pass
                e=self.expression(_t)
                _t = self._retTree
                r = e
            elif la1 and la1 in [EQUALS]:
                pass
                i=self.initialisation(_t)
                _t = self._retTree
                r = i
            elif la1 and la1 in [PLUSEQUALS]:
                pass
                m=self.modification(_t)
                _t = self._retTree
                r = m
            elif la1 and la1 in [LITERAL_def]:
                pass
                f=self.functionDefinition(_t)
                _t = self._retTree
                r = f
            elif la1 and la1 in [LITERAL_class]:
                pass
                c=self.classDefinition(_t)
                _t = self._retTree
                r = c
            elif la1 and la1 in [LITERAL_interface]:
                pass
                n=self.interfaceDefinition(_t)
                _t = self._retTree
                r = n
            elif la1 and la1 in [LITERAL_while]:
                pass
                w=self.whileStatement(_t)
                _t = self._retTree
                r = w
            elif la1 and la1 in [LITERAL_import]:
                pass
                i=self.importStatement(_t)
                _t = self._retTree
                r = i
            elif la1 and la1 in [LBRACE]:
                pass
                c=self.codeBlock(_t)
                _t = self._retTree
                r = c
            else:
                    raise antlr.NoViableAltException(_t)
                
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def expression(self, _t):    
        r = None
        
        expression_AST_in = None
        if _t != antlr.ASTNULL:
            expression_AST_in = _t
        i = None
        d = None
        t = None
        try:      ## for error handling
            if not _t:
                _t = antlr.ASTNULL
            la1 = _t.getType()
            if False:
                pass
            elif la1 and la1 in [SYMBOL]:
                pass
                s=self.symbol(_t)
                _t = self._retTree
                r = s
            elif la1 and la1 in [INT]:
                pass
                i = _t
                self.match(_t,INT)
                _t = _t.getNextSibling()
                r = PepInt(    i.getText() )
            elif la1 and la1 in [FLOAT]:
                pass
                d = _t
                self.match(_t,FLOAT)
                _t = _t.getNextSibling()
                r = PepFloat(  d.getText() )
            elif la1 and la1 in [STRING]:
                pass
                t = _t
                self.match(_t,STRING)
                _t = _t.getNextSibling()
                r = PepString( t.getText() )
            elif la1 and la1 in [LSQUBR]:
                pass
                a=self.arraylookup(_t)
                _t = self._retTree
                r = a
            elif la1 and la1 in [PLUS]:
                pass
                _t152 = _t
                tmp1_AST_in = _t
                self.match(_t,PLUS)
                _t = _t.getFirstChild()
                e1=self.expression(_t)
                _t = self._retTree
                e2=self.expression(_t)
                _t = self._retTree
                _t = _t152
                _t = _t.getNextSibling()
                r = PepPlus( e1, e2 )
            elif la1 and la1 in [MINUS]:
                pass
                _t153 = _t
                tmp2_AST_in = _t
                self.match(_t,MINUS)
                _t = _t.getFirstChild()
                e1=self.expression(_t)
                _t = self._retTree
                e2=self.expression(_t)
                _t = self._retTree
                _t = _t153
                _t = _t.getNextSibling()
                r = PepMinus( e1, e2 )
            elif la1 and la1 in [TIMES]:
                pass
                _t154 = _t
                tmp3_AST_in = _t
                self.match(_t,TIMES)
                _t = _t.getFirstChild()
                e1=self.expression(_t)
                _t = self._retTree
                e2=self.expression(_t)
                _t = self._retTree
                _t = _t154
                _t = _t.getNextSibling()
                r = PepTimes( e1, e2 )
            elif la1 and la1 in [GT]:
                pass
                _t155 = _t
                tmp4_AST_in = _t
                self.match(_t,GT)
                _t = _t.getFirstChild()
                e1=self.expression(_t)
                _t = self._retTree
                e2=self.expression(_t)
                _t = self._retTree
                _t = _t155
                _t = _t.getNextSibling()
                r = PepGreaterThan( e1, e2 )
            elif la1 and la1 in [LT]:
                pass
                _t156 = _t
                tmp5_AST_in = _t
                self.match(_t,LT)
                _t = _t.getFirstChild()
                e1=self.expression(_t)
                _t = self._retTree
                e2=self.expression(_t)
                _t = self._retTree
                _t = _t156
                _t = _t.getNextSibling()
                r = PepLessThan( e1, e2 )
            elif la1 and la1 in [LPAREN]:
                pass
                f=self.functionCall(_t)
                _t = self._retTree
                r = f
            elif la1 and la1 in [LITERAL_quote]:
                pass
                q=self.quotedCode(_t)
                _t = self._retTree
                r = q
            elif la1 and la1 in [COMMA]:
                pass
                t=self.tuple(_t)
                _t = self._retTree
                r = t
            else:
                    raise antlr.NoViableAltException(_t)
                
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def initialisation(self, _t):    
        r = None
        
        initialisation_AST_in = None
        if _t != antlr.ASTNULL:
            initialisation_AST_in = _t
        try:      ## for error handling
            pass
            _t158 = _t
            tmp6_AST_in = _t
            self.match(_t,EQUALS)
            _t = _t.getFirstChild()
            t=self.expression(_t)
            _t = self._retTree
            s=self.symbol(_t)
            _t = self._retTree
            v=self.expression(_t)
            _t = self._retTree
            _t = _t158
            _t = _t.getNextSibling()
            r = PepInit( t, s, v )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def modification(self, _t):    
        r = None
        
        modification_AST_in = None
        if _t != antlr.ASTNULL:
            modification_AST_in = _t
        try:      ## for error handling
            pass
            _t160 = _t
            tmp7_AST_in = _t
            self.match(_t,PLUSEQUALS)
            _t = _t.getFirstChild()
            s=self.symbol(_t)
            _t = self._retTree
            v=self.expression(_t)
            _t = self._retTree
            _t = _t160
            _t = _t.getNextSibling()
            r = PepModification( s, v )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def functionDefinition(self, _t):    
        r = None
        
        functionDefinition_AST_in = None
        if _t != antlr.ASTNULL:
            functionDefinition_AST_in = _t
        try:      ## for error handling
            pass
            _t162 = _t
            tmp8_AST_in = _t
            self.match(_t,LITERAL_def)
            _t = _t.getFirstChild()
            t=self.expression(_t)
            _t = self._retTree
            n=self.symbol(_t)
            _t = self._retTree
            a=self.typedArgumentsList(_t)
            _t = self._retTree
            s=self.suite(_t)
            _t = self._retTree
            _t = _t162
            _t = _t.getNextSibling()
            r = PepDef( t, n, a, s )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def classDefinition(self, _t):    
        r = None
        
        classDefinition_AST_in = None
        if _t != antlr.ASTNULL:
            classDefinition_AST_in = _t
        try:      ## for error handling
            pass
            _t168 = _t
            tmp9_AST_in = _t
            self.match(_t,LITERAL_class)
            _t = _t.getFirstChild()
            n=self.symbol(_t)
            _t = self._retTree
            s=self.classSuite(_t)
            _t = self._retTree
            _t = _t168
            _t = _t.getNextSibling()
            r = PepClass( n, (), s )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def interfaceDefinition(self, _t):    
        r = None
        
        interfaceDefinition_AST_in = None
        if _t != antlr.ASTNULL:
            interfaceDefinition_AST_in = _t
        try:      ## for error handling
            pass
            _t170 = _t
            tmp10_AST_in = _t
            self.match(_t,LITERAL_interface)
            _t = _t.getFirstChild()
            n=self.symbol(_t)
            _t = self._retTree
            s=self.interfaceSuite(_t)
            _t = self._retTree
            _t = _t170
            _t = _t.getNextSibling()
            r = PepInterface( n, (), s )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def whileStatement(self, _t):    
        r = None
        
        whileStatement_AST_in = None
        if _t != antlr.ASTNULL:
            whileStatement_AST_in = _t
        try:      ## for error handling
            pass
            _t172 = _t
            tmp11_AST_in = _t
            self.match(_t,LITERAL_while)
            _t = _t.getFirstChild()
            e=self.expression(_t)
            _t = self._retTree
            s=self.suite(_t)
            _t = self._retTree
            _t = _t172
            _t = _t.getNextSibling()
            r = PepWhile( e, s )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def importStatement(self, _t):    
        r = None
        
        importStatement_AST_in = None
        if _t != antlr.ASTNULL:
            importStatement_AST_in = _t
        m = None
        try:      ## for error handling
            pass
            _t174 = _t
            tmp12_AST_in = _t
            self.match(_t,LITERAL_import)
            _t = _t.getFirstChild()
            m = _t
            self.match(_t,SYMBOL)
            _t = _t.getNextSibling()
            _t = _t174
            _t = _t.getNextSibling()
            r = PepImport( m.getText() )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def codeBlock(self, _t):    
        r = None
        
        codeBlock_AST_in = None
        if _t != antlr.ASTNULL:
            codeBlock_AST_in = _t
        try:      ## for error handling
            pass
            _t146 = _t
            tmp13_AST_in = _t
            self.match(_t,LBRACE)
            _t = _t.getFirstChild()
            a=self.codeBlockArgs(_t)
            _t = self._retTree
            s=self.statementsList(_t)
            _t = self._retTree
            _t = _t146
            _t = _t.getNextSibling()
            r = PepCodeBlock(a, s)
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def codeBlockArgs(self, _t):    
        r = None
        
        codeBlockArgs_AST_in = None
        if _t != antlr.ASTNULL:
            codeBlockArgs_AST_in = _t
        try:      ## for error handling
            pass
            _t148 = _t
            tmp14_AST_in = _t
            self.match(_t,PIPE)
            _t = _t.getFirstChild()
            s=self.symbol(_t)
            _t = self._retTree
            _t = _t148
            _t = _t.getNextSibling()
            r = (s,)
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def statementsList(self, _t):    
        r = None
        
        statementsList_AST_in = None
        if _t != antlr.ASTNULL:
            statementsList_AST_in = _t
        r = ()
        try:      ## for error handling
            pass
            s=self.statementOrReturnStatement(_t)
            _t = self._retTree
            r = (s,)
            while True:
                if not _t:
                    _t = antlr.ASTNULL
                if (_tokenSet_0.member(_t.getType())):
                    pass
                    s=self.statementOrReturnStatement(_t)
                    _t = self._retTree
                    r += (s,)
                else:
                    break
                
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def symbol(self, _t):    
        r = None
        
        symbol_AST_in = None
        if _t != antlr.ASTNULL:
            symbol_AST_in = _t
        f = None
        try:      ## for error handling
            pass
            f = _t
            self.match(_t,SYMBOL)
            _t = _t.getNextSibling()
            r = PepSymbol( f.getText() )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def classStatement(self, _t):    
        r = None
        
        classStatement_AST_in = None
        if _t != antlr.ASTNULL:
            classStatement_AST_in = _t
        try:      ## for error handling
            if not _t:
                _t = antlr.ASTNULL
            la1 = _t.getType()
            if False:
                pass
            elif la1 and la1 in [INT,FLOAT,STRING,LBRACE,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,PLUSEQUALS,GT,LT,EQUALS,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_while,LITERAL_import,LITERAL_quote]:
                pass
                s=self.statement(_t)
                _t = self._retTree
                r = s
            elif la1 and la1 in [LITERAL_def_init]:
                pass
                f=self.initFunctionDefinition(_t)
                _t = self._retTree
                r = f
            else:
                    raise antlr.NoViableAltException(_t)
                
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def initFunctionDefinition(self, _t):    
        r = None
        
        initFunctionDefinition_AST_in = None
        if _t != antlr.ASTNULL:
            initFunctionDefinition_AST_in = _t
        try:      ## for error handling
            pass
            _t166 = _t
            tmp15_AST_in = _t
            self.match(_t,LITERAL_def_init)
            _t = _t.getFirstChild()
            a=self.typedArgumentsList(_t)
            _t = self._retTree
            s=self.initFunctionSuite(_t)
            _t = self._retTree
            _t = _t166
            _t = _t.getNextSibling()
            r = PepDefInit( a, s )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def interfaceStatement(self, _t):    
        r = None
        
        interfaceStatement_AST_in = None
        if _t != antlr.ASTNULL:
            interfaceStatement_AST_in = _t
        try:      ## for error handling
            pass
            f=self.interfaceFunctionDefinition(_t)
            _t = self._retTree
            r = f
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def interfaceFunctionDefinition(self, _t):    
        r = None
        
        interfaceFunctionDefinition_AST_in = None
        if _t != antlr.ASTNULL:
            interfaceFunctionDefinition_AST_in = _t
        try:      ## for error handling
            pass
            _t164 = _t
            tmp16_AST_in = _t
            self.match(_t,LITERAL_def)
            _t = _t.getFirstChild()
            t=self.expression(_t)
            _t = self._retTree
            n=self.symbol(_t)
            _t = self._retTree
            a=self.typedArgumentsList(_t)
            _t = self._retTree
            _t = _t164
            _t = _t.getNextSibling()
            r = PepInterfaceDef( t, n, a )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def arraylookup(self, _t):    
        r = None
        
        arraylookup_AST_in = None
        if _t != antlr.ASTNULL:
            arraylookup_AST_in = _t
        try:      ## for error handling
            pass
            _t177 = _t
            tmp17_AST_in = _t
            self.match(_t,LSQUBR)
            _t = _t.getFirstChild()
            arr=self.symbol(_t)
            _t = self._retTree
            idx=self.expression(_t)
            _t = self._retTree
            _t = _t177
            _t = _t.getNextSibling()
            r = PepArrayLookup( arr, idx )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def functionCall(self, _t):    
        r = None
        
        functionCall_AST_in = None
        if _t != antlr.ASTNULL:
            functionCall_AST_in = _t
        try:      ## for error handling
            pass
            _t186 = _t
            tmp18_AST_in = _t
            self.match(_t,LPAREN)
            _t = _t.getFirstChild()
            f=self.symbol(_t)
            _t = self._retTree
            a=self.argumentsList(_t)
            _t = self._retTree
            _t = _t186
            _t = _t.getNextSibling()
            r = PepFunctionCall( f, a )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def quotedCode(self, _t):    
        r = None
        
        quotedCode_AST_in = None
        if _t != antlr.ASTNULL:
            quotedCode_AST_in = _t
        try:      ## for error handling
            pass
            _t179 = _t
            tmp19_AST_in = _t
            self.match(_t,LITERAL_quote)
            _t = _t.getFirstChild()
            s=self.suite(_t)
            _t = self._retTree
            _t = _t179
            _t = _t.getNextSibling()
            r = PepQuote( s )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def tuple(self, _t):    
        r = None
        
        tuple_AST_in = None
        if _t != antlr.ASTNULL:
            tuple_AST_in = _t
        try:      ## for error handling
            pass
            t=self.tupleContents(_t)
            _t = self._retTree
            r = PepTuple( t )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def typedArgumentsList(self, _t):    
        r = None
        
        typedArgumentsList_AST_in = None
        if _t != antlr.ASTNULL:
            typedArgumentsList_AST_in = _t
        r = ()
        try:      ## for error handling
            pass
            _t188 = _t
            tmp20_AST_in = _t
            self.match(_t,LPAREN)
            _t = _t.getFirstChild()
            if not _t:
                _t = antlr.ASTNULL
            la1 = _t.getType()
            if False:
                pass
            elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,GT,LT,LITERAL_quote]:
                pass
                e=self.expression(_t)
                _t = self._retTree
                s=self.symbol(_t)
                _t = self._retTree
                r = ( (e,s), )
                while True:
                    if not _t:
                        _t = antlr.ASTNULL
                    if (_t.getType()==COMMA):
                        pass
                        tmp21_AST_in = _t
                        self.match(_t,COMMA)
                        _t = _t.getNextSibling()
                        e=self.expression(_t)
                        _t = self._retTree
                        s=self.symbol(_t)
                        _t = self._retTree
                        r += ( (e,s), )
                    else:
                        break
                    
            elif la1 and la1 in [3]:
                pass
            else:
                    raise antlr.NoViableAltException(_t)
                
            _t = _t188
            _t = _t.getNextSibling()
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def suite(self, _t):    
        r = None
        
        suite_AST_in = None
        if _t != antlr.ASTNULL:
            suite_AST_in = _t
        try:      ## for error handling
            pass
            _t193 = _t
            tmp22_AST_in = _t
            self.match(_t,COLON)
            _t = _t.getFirstChild()
            s=self.statementsList(_t)
            _t = self._retTree
            _t = _t193
            _t = _t.getNextSibling()
            r = s
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def initFunctionSuite(self, _t):    
        r = None
        
        initFunctionSuite_AST_in = None
        if _t != antlr.ASTNULL:
            initFunctionSuite_AST_in = _t
        try:      ## for error handling
            pass
            _t199 = _t
            tmp23_AST_in = _t
            self.match(_t,COLON)
            _t = _t.getFirstChild()
            s=self.initFunctionStatementsList(_t)
            _t = self._retTree
            _t = _t199
            _t = _t.getNextSibling()
            r = s
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def classSuite(self, _t):    
        r = None
        
        classSuite_AST_in = None
        if _t != antlr.ASTNULL:
            classSuite_AST_in = _t
        try:      ## for error handling
            pass
            _t195 = _t
            tmp24_AST_in = _t
            self.match(_t,COLON)
            _t = _t.getFirstChild()
            s=self.classStatementsList(_t)
            _t = self._retTree
            _t = _t195
            _t = _t.getNextSibling()
            r = s
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def interfaceSuite(self, _t):    
        r = None
        
        interfaceSuite_AST_in = None
        if _t != antlr.ASTNULL:
            interfaceSuite_AST_in = _t
        try:      ## for error handling
            pass
            _t197 = _t
            tmp25_AST_in = _t
            self.match(_t,COLON)
            _t = _t.getFirstChild()
            s=self.interfaceStatementsList(_t)
            _t = self._retTree
            _t = _t197
            _t = _t.getNextSibling()
            r = s
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def tupleContents(self, _t):    
        r = None
        
        tupleContents_AST_in = None
        if _t != antlr.ASTNULL:
            tupleContents_AST_in = _t
        try:      ## for error handling
            pass
            _t182 = _t
            tmp26_AST_in = _t
            self.match(_t,COMMA)
            _t = _t.getFirstChild()
            e=self.expression(_t)
            _t = self._retTree
            r = (e,)
            while True:
                if not _t:
                    _t = antlr.ASTNULL
                if (_tokenSet_1.member(_t.getType())):
                    pass
                    e=self.expression(_t)
                    _t = self._retTree
                    r += (e,)
                else:
                    break
                
            _t = _t182
            _t = _t.getNextSibling()
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def argumentsList(self, _t):    
        r = None
        
        argumentsList_AST_in = None
        if _t != antlr.ASTNULL:
            argumentsList_AST_in = _t
        r = ()
        try:      ## for error handling
            pass
            if not _t:
                _t = antlr.ASTNULL
            la1 = _t.getType()
            if False:
                pass
            elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,GT,LT,LITERAL_quote]:
                pass
                e=self.expression(_t)
                _t = self._retTree
                r = (e,)
                while True:
                    if not _t:
                        _t = antlr.ASTNULL
                    if (_t.getType()==COMMA):
                        pass
                        tmp27_AST_in = _t
                        self.match(_t,COMMA)
                        _t = _t.getNextSibling()
                        e=self.expression(_t)
                        _t = self._retTree
                        r += (e,)
                    else:
                        break
                    
            elif la1 and la1 in [3]:
                pass
            else:
                    raise antlr.NoViableAltException(_t)
                
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def classStatementsList(self, _t):    
        r = None
        
        classStatementsList_AST_in = None
        if _t != antlr.ASTNULL:
            classStatementsList_AST_in = _t
        r = ()
        try:      ## for error handling
            pass
            s=self.classStatement(_t)
            _t = self._retTree
            r = (s,)
            while True:
                if not _t:
                    _t = antlr.ASTNULL
                if (_tokenSet_2.member(_t.getType())):
                    pass
                    s=self.classStatement(_t)
                    _t = self._retTree
                    r += (s,)
                else:
                    break
                
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def interfaceStatementsList(self, _t):    
        r = None
        
        interfaceStatementsList_AST_in = None
        if _t != antlr.ASTNULL:
            interfaceStatementsList_AST_in = _t
        r = ()
        try:      ## for error handling
            pass
            s=self.interfaceStatement(_t)
            _t = self._retTree
            r = (s,)
            while True:
                if not _t:
                    _t = antlr.ASTNULL
                if (_t.getType()==LITERAL_def):
                    pass
                    s=self.interfaceStatement(_t)
                    _t = self._retTree
                    r += (s,)
                else:
                    break
                
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def initFunctionStatementsList(self, _t):    
        r = None
        
        initFunctionStatementsList_AST_in = None
        if _t != antlr.ASTNULL:
            initFunctionStatementsList_AST_in = _t
        r = ()
        try:      ## for error handling
            pass
            if not _t:
                _t = antlr.ASTNULL
            la1 = _t.getType()
            if False:
                pass
            elif la1 and la1 in [LITERAL_var]:
                pass
                v=self.varStatement(_t)
                _t = self._retTree
                r = (v,)
            elif la1 and la1 in [INT,FLOAT,STRING,LBRACE,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,PLUSEQUALS,GT,LT,EQUALS,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_while,LITERAL_import,LITERAL_quote]:
                pass
                s=self.statement(_t)
                _t = self._retTree
                r = (s,)
            else:
                    raise antlr.NoViableAltException(_t)
                
            while True:
                if not _t:
                    _t = antlr.ASTNULL
                if (_tokenSet_3.member(_t.getType())):
                    pass
                    s=self.statement(_t)
                    _t = self._retTree
                    r += (s,)
                else:
                    break
                
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def varSuite(self, _t):    
        r = None
        
        varSuite_AST_in = None
        if _t != antlr.ASTNULL:
            varSuite_AST_in = _t
        try:      ## for error handling
            pass
            _t201 = _t
            tmp28_AST_in = _t
            self.match(_t,COLON)
            _t = _t.getFirstChild()
            s=self.initialisationsList(_t)
            _t = self._retTree
            _t = _t201
            _t = _t.getNextSibling()
            r = s
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def initialisationsList(self, _t):    
        r = None
        
        initialisationsList_AST_in = None
        if _t != antlr.ASTNULL:
            initialisationsList_AST_in = _t
        r = ()
        try:      ## for error handling
            pass
            i=self.initialisation(_t)
            _t = self._retTree
            r = (i,)
            while True:
                if not _t:
                    _t = antlr.ASTNULL
                if (_t.getType()==EQUALS):
                    pass
                    i=self.initialisation(_t)
                    _t = self._retTree
                    r += (i,)
                else:
                    break
                
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def statementOrReturnStatement(self, _t):    
        r = None
        
        statementOrReturnStatement_AST_in = None
        if _t != antlr.ASTNULL:
            statementOrReturnStatement_AST_in = _t
        try:      ## for error handling
            if not _t:
                _t = antlr.ASTNULL
            la1 = _t.getType()
            if False:
                pass
            elif la1 and la1 in [INT,FLOAT,STRING,LBRACE,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,PLUSEQUALS,GT,LT,EQUALS,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_while,LITERAL_import,LITERAL_quote]:
                pass
                s=self.statement(_t)
                _t = self._retTree
                r = s
            elif la1 and la1 in [LITERAL_return]:
                pass
                _t225 = _t
                tmp29_AST_in = _t
                self.match(_t,LITERAL_return)
                _t = _t.getFirstChild()
                e=self.expression(_t)
                _t = self._retTree
                _t = _t225
                _t = _t.getNextSibling()
                r = PepReturn( e )
            else:
                    raise antlr.NoViableAltException(_t)
                
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def varStatement(self, _t):    
        r = None
        
        varStatement_AST_in = None
        if _t != antlr.ASTNULL:
            varStatement_AST_in = _t
        try:      ## for error handling
            pass
            _t223 = _t
            tmp30_AST_in = _t
            self.match(_t,LITERAL_var)
            _t = _t.getFirstChild()
            s=self.varSuite(_t)
            _t = self._retTree
            _t = _t223
            _t = _t.getNextSibling()
            r = PepVar( s )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    

_tokenNames = [
    "<0>", 
    "EOF", 
    "<2>", 
    "NULL_TREE_LOOKAHEAD", 
    "WHITESPACE", 
    "COMMENT", 
    "DIGIT", 
    "DIGITS", 
    "INT", 
    "DOT", 
    "FLOAT", 
    "INT_OR_DOT_OR_FLOAT", 
    "TRIPLEDOUBLEQUOTE", 
    "DOUBLEQUOTE", 
    "DOUBLEQUOTESTRING", 
    "TRIPLEDOUBLEQUOTESTRING", 
    "STRING", 
    "LBRACE", 
    "RBRACE", 
    "PIPE", 
    "LPAREN", 
    "RPAREN", 
    "LSQUBR", 
    "RSQUBR", 
    "COMMA", 
    "SEMICOLON", 
    "STARTSYMBOLCHAR", 
    "MIDSYMBOLCHAR", 
    "SYMBOL", 
    "PLUS", 
    "MINUS", 
    "TIMES", 
    "PLUSEQUALS", 
    "GT", 
    "LT", 
    "COLON", 
    "EQUALS", 
    "EQUALSEQUALS", 
    "\"def\"", 
    "\"def_init\"", 
    "\"class\"", 
    "\"interface\"", 
    "\"while\"", 
    "\"import\"", 
    "\"quote\"", 
    "NEWLINE", 
    "INDENT", 
    "DEDENT", 
    "\"var\"", 
    "\"return\""
]
    

### generate bit set
def mk_tokenSet_0(): 
    ### var1
    data = [ 597412524786944L, 0L]
    return data
_tokenSet_0 = antlr.BitSet(mk_tokenSet_0())

### generate bit set
def mk_tokenSet_1(): 
    ### var1
    data = [ 17622004466944L, 0L]
    return data
_tokenSet_1 = antlr.BitSet(mk_tokenSet_1())

### generate bit set
def mk_tokenSet_2(): 
    ### var1
    data = [ 35012327179520L, 0L]
    return data
_tokenSet_2 = antlr.BitSet(mk_tokenSet_2())

### generate bit set
def mk_tokenSet_3(): 
    ### var1
    data = [ 34462571365632L, 0L]
    return data
_tokenSet_3 = antlr.BitSet(mk_tokenSet_3())
