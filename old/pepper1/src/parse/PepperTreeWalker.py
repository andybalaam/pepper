### $ANTLR 2.7.7 (20160104): "pepper.g" -> "PepperTreeWalker.py"$
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
            elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,GT,LT,LITERAL_if,LITERAL_quote]:
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
            elif la1 and la1 in [LITERAL_for]:
                pass
                f=self.forStatement(_t)
                _t = self._retTree
                r = f
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
            elif la1 and la1 in [LITERAL_if]:
                pass
                i=self.ifExpression(_t)
                _t = self._retTree
                r = i
            elif la1 and la1 in [PLUS]:
                pass
                _t147 = _t
                tmp87_AST_in = _t
                self.match(_t,PLUS)
                _t = _t.getFirstChild()
                e1=self.expression(_t)
                _t = self._retTree
                e2=self.expression(_t)
                _t = self._retTree
                _t = _t147
                _t = _t.getNextSibling()
                r = PepPlus( e1, e2 )
            elif la1 and la1 in [MINUS]:
                pass
                _t148 = _t
                tmp88_AST_in = _t
                self.match(_t,MINUS)
                _t = _t.getFirstChild()
                e1=self.expression(_t)
                _t = self._retTree
                e2=self.expression(_t)
                _t = self._retTree
                _t = _t148
                _t = _t.getNextSibling()
                r = PepMinus( e1, e2 )
            elif la1 and la1 in [TIMES]:
                pass
                _t149 = _t
                tmp89_AST_in = _t
                self.match(_t,TIMES)
                _t = _t.getFirstChild()
                e1=self.expression(_t)
                _t = self._retTree
                e2=self.expression(_t)
                _t = self._retTree
                _t = _t149
                _t = _t.getNextSibling()
                r = PepTimes( e1, e2 )
            elif la1 and la1 in [GT]:
                pass
                _t150 = _t
                tmp90_AST_in = _t
                self.match(_t,GT)
                _t = _t.getFirstChild()
                e1=self.expression(_t)
                _t = self._retTree
                e2=self.expression(_t)
                _t = self._retTree
                _t = _t150
                _t = _t.getNextSibling()
                r = PepGreaterThan( e1, e2 )
            elif la1 and la1 in [LT]:
                pass
                _t151 = _t
                tmp91_AST_in = _t
                self.match(_t,LT)
                _t = _t.getFirstChild()
                e1=self.expression(_t)
                _t = self._retTree
                e2=self.expression(_t)
                _t = self._retTree
                _t = _t151
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
            _t153 = _t
            tmp92_AST_in = _t
            self.match(_t,EQUALS)
            _t = _t.getFirstChild()
            t=self.expression(_t)
            _t = self._retTree
            s=self.symbol(_t)
            _t = self._retTree
            v=self.expression(_t)
            _t = self._retTree
            _t = _t153
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
            _t155 = _t
            tmp93_AST_in = _t
            self.match(_t,PLUSEQUALS)
            _t = _t.getFirstChild()
            s=self.symbol(_t)
            _t = self._retTree
            v=self.expression(_t)
            _t = self._retTree
            _t = _t155
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
            _t157 = _t
            tmp94_AST_in = _t
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
            _t = _t157
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
            _t163 = _t
            tmp95_AST_in = _t
            self.match(_t,LITERAL_class)
            _t = _t.getFirstChild()
            n=self.symbol(_t)
            _t = self._retTree
            s=self.classSuite(_t)
            _t = self._retTree
            _t = _t163
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
            _t165 = _t
            tmp96_AST_in = _t
            self.match(_t,LITERAL_interface)
            _t = _t.getFirstChild()
            n=self.symbol(_t)
            _t = self._retTree
            s=self.interfaceSuite(_t)
            _t = self._retTree
            _t = _t165
            _t = _t.getNextSibling()
            r = PepInterface( n, (), s )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def forStatement(self, _t):    
        r = None
        
        forStatement_AST_in = None
        if _t != antlr.ASTNULL:
            forStatement_AST_in = _t
        try:      ## for error handling
            pass
            _t167 = _t
            tmp97_AST_in = _t
            self.match(_t,LITERAL_for)
            _t = _t.getFirstChild()
            t=self.expression(_t)
            _t = self._retTree
            v=self.symbol(_t)
            _t = self._retTree
            i=self.expression(_t)
            _t = self._retTree
            s=self.suite(_t)
            _t = self._retTree
            _t = _t167
            _t = _t.getNextSibling()
            r = PepFor( t, v, i, s )
        
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
            _t169 = _t
            tmp98_AST_in = _t
            self.match(_t,LITERAL_while)
            _t = _t.getFirstChild()
            e=self.expression(_t)
            _t = self._retTree
            s=self.suite(_t)
            _t = self._retTree
            _t = _t169
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
            _t171 = _t
            tmp99_AST_in = _t
            self.match(_t,LITERAL_import)
            _t = _t.getFirstChild()
            m = _t
            self.match(_t,SYMBOL)
            _t = _t.getNextSibling()
            _t = _t171
            _t = _t.getNextSibling()
            r = PepImport( m.getText() )
        
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
            elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,PLUSEQUALS,GT,LT,EQUALS,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_for,LITERAL_while,LITERAL_import,LITERAL_if,LITERAL_quote]:
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
            _t161 = _t
            tmp100_AST_in = _t
            self.match(_t,LITERAL_def_init)
            _t = _t.getFirstChild()
            a=self.typedArgumentsList(_t)
            _t = self._retTree
            s=self.initFunctionSuite(_t)
            _t = self._retTree
            _t = _t161
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
            _t159 = _t
            tmp101_AST_in = _t
            self.match(_t,LITERAL_def)
            _t = _t.getFirstChild()
            t=self.expression(_t)
            _t = self._retTree
            n=self.symbol(_t)
            _t = self._retTree
            a=self.typedArgumentsList(_t)
            _t = self._retTree
            _t = _t159
            _t = _t.getNextSibling()
            r = PepInterfaceDef( t, n, a )
        
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
    
    def arraylookup(self, _t):    
        r = None
        
        arraylookup_AST_in = None
        if _t != antlr.ASTNULL:
            arraylookup_AST_in = _t
        try:      ## for error handling
            pass
            _t174 = _t
            tmp102_AST_in = _t
            self.match(_t,LSQUBR)
            _t = _t.getFirstChild()
            arr=self.symbol(_t)
            _t = self._retTree
            idx=self.expression(_t)
            _t = self._retTree
            _t = _t174
            _t = _t.getNextSibling()
            r = PepArrayLookup( arr, idx )
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def ifExpression(self, _t):    
        r = None
        
        ifExpression_AST_in = None
        if _t != antlr.ASTNULL:
            ifExpression_AST_in = _t
        try:      ## for error handling
            pass
            _t176 = _t
            tmp103_AST_in = _t
            self.match(_t,LITERAL_if)
            _t = _t.getFirstChild()
            pred=self.expression(_t)
            _t = self._retTree
            s=self.suite(_t)
            _t = self._retTree
            es=self.elseExpression(_t)
            _t = self._retTree
            _t = _t176
            _t = _t.getNextSibling()
            r = PepIf( pred, s, es )
        
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
            _t187 = _t
            tmp104_AST_in = _t
            self.match(_t,LPAREN)
            _t = _t.getFirstChild()
            f=self.symbol(_t)
            _t = self._retTree
            a=self.argumentsList(_t)
            _t = self._retTree
            _t = _t187
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
            _t180 = _t
            tmp105_AST_in = _t
            self.match(_t,LITERAL_quote)
            _t = _t.getFirstChild()
            s=self.suite(_t)
            _t = self._retTree
            _t = _t180
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
            _t189 = _t
            tmp106_AST_in = _t
            self.match(_t,LPAREN)
            _t = _t.getFirstChild()
            if not _t:
                _t = antlr.ASTNULL
            la1 = _t.getType()
            if False:
                pass
            elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,GT,LT,LITERAL_if,LITERAL_quote]:
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
                        tmp107_AST_in = _t
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
                
            _t = _t189
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
            _t194 = _t
            tmp108_AST_in = _t
            self.match(_t,COLON)
            _t = _t.getFirstChild()
            s=self.statementsList(_t)
            _t = self._retTree
            _t = _t194
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
            _t200 = _t
            tmp109_AST_in = _t
            self.match(_t,COLON)
            _t = _t.getFirstChild()
            s=self.initFunctionStatementsList(_t)
            _t = self._retTree
            _t = _t200
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
            _t196 = _t
            tmp110_AST_in = _t
            self.match(_t,COLON)
            _t = _t.getFirstChild()
            s=self.classStatementsList(_t)
            _t = self._retTree
            _t = _t196
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
            _t198 = _t
            tmp111_AST_in = _t
            self.match(_t,COLON)
            _t = _t.getFirstChild()
            s=self.interfaceStatementsList(_t)
            _t = self._retTree
            _t = _t198
            _t = _t.getNextSibling()
            r = s
        
        except antlr.RecognitionException, ex:
            self.reportError(ex)
            if _t:
                _t = _t.getNextSibling()
        
        self._retTree = _t
        return r
    
    def elseExpression(self, _t):    
        r = None
        
        elseExpression_AST_in = None
        if _t != antlr.ASTNULL:
            elseExpression_AST_in = _t
        r = None
        try:      ## for error handling
            pass
            if not _t:
                _t = antlr.ASTNULL
            la1 = _t.getType()
            if False:
                pass
            elif la1 and la1 in [LITERAL_else]:
                pass
                tmp112_AST_in = _t
                self.match(_t,LITERAL_else)
                _t = _t.getNextSibling()
                s=self.suite(_t)
                _t = self._retTree
                r = s
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
    
    def tupleContents(self, _t):    
        r = None
        
        tupleContents_AST_in = None
        if _t != antlr.ASTNULL:
            tupleContents_AST_in = _t
        try:      ## for error handling
            pass
            _t183 = _t
            tmp113_AST_in = _t
            self.match(_t,COMMA)
            _t = _t.getFirstChild()
            e=self.expression(_t)
            _t = self._retTree
            r = (e,)
            while True:
                if not _t:
                    _t = antlr.ASTNULL
                if (_tokenSet_0.member(_t.getType())):
                    pass
                    e=self.expression(_t)
                    _t = self._retTree
                    r += (e,)
                else:
                    break
                
            _t = _t183
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
            elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,GT,LT,LITERAL_if,LITERAL_quote]:
                pass
                e=self.expression(_t)
                _t = self._retTree
                r = (e,)
                while True:
                    if not _t:
                        _t = antlr.ASTNULL
                    if (_t.getType()==COMMA):
                        pass
                        tmp114_AST_in = _t
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
                if (_tokenSet_1.member(_t.getType())):
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
            elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,PLUSEQUALS,GT,LT,EQUALS,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_for,LITERAL_while,LITERAL_import,LITERAL_if,LITERAL_quote]:
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
            _t202 = _t
            tmp115_AST_in = _t
            self.match(_t,COLON)
            _t = _t.getFirstChild()
            s=self.initialisationsList(_t)
            _t = self._retTree
            _t = _t202
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
            elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,LSQUBR,COMMA,SYMBOL,PLUS,MINUS,TIMES,PLUSEQUALS,GT,LT,EQUALS,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_for,LITERAL_while,LITERAL_import,LITERAL_if,LITERAL_quote]:
                pass
                s=self.statement(_t)
                _t = self._retTree
                r = s
            elif la1 and la1 in [LITERAL_return]:
                pass
                _t226 = _t
                tmp116_AST_in = _t
                self.match(_t,LITERAL_return)
                _t = _t.getFirstChild()
                e=self.expression(_t)
                _t = self._retTree
                _t = _t226
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
            _t224 = _t
            tmp117_AST_in = _t
            self.match(_t,LITERAL_var)
            _t = _t.getFirstChild()
            s=self.varSuite(_t)
            _t = self._retTree
            _t = _t224
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
    "INDENT", 
    "DEDENT", 
    "WHITESPACE", 
    "LEADINGSP", 
    "COMMENT", 
    "DIGIT", 
    "DIGITS", 
    "INT", 
    "FLOAT", 
    "INT_OR_FLOAT", 
    "TRIPLEDOUBLEQUOTE", 
    "DOUBLEQUOTE", 
    "DOUBLEQUOTESTRING", 
    "TRIPLEDOUBLEQUOTESTRING", 
    "STRING", 
    "LPAREN", 
    "RPAREN", 
    "LSQUBR", 
    "RSQUBR", 
    "COMMA", 
    "STARTSYMBOLCHAR", 
    "MIDSYMBOLCHAR", 
    "SYMBOL_EL", 
    "SYMBOL", 
    "NEWLINE", 
    "PLUS", 
    "MINUS", 
    "TIMES", 
    "PLUSEQUALS", 
    "GT", 
    "LT", 
    "COLON", 
    "EQUALS", 
    "\"def\"", 
    "\"def_init\"", 
    "\"class\"", 
    "\"interface\"", 
    "\"for\"", 
    "\"in\"", 
    "\"while\"", 
    "\"import\"", 
    "\"if\"", 
    "\"else\"", 
    "\"quote\"", 
    "\"var\"", 
    "\"return\""
]
    

### generate bit set
def mk_tokenSet_0(): 
    ### var1
    data = [ 175951533840384L, 0L]
    return data
_tokenSet_0 = antlr.BitSet(mk_tokenSet_0())

### generate bit set
def mk_tokenSet_1(): 
    ### var1
    data = [ 769348510423040L, 0L]
    return data
_tokenSet_1 = antlr.BitSet(mk_tokenSet_1())

### generate bit set
def mk_tokenSet_2(): 
    ### var1
    data = [ 206673434908672L, 0L]
    return data
_tokenSet_2 = antlr.BitSet(mk_tokenSet_2())

### generate bit set
def mk_tokenSet_3(): 
    ### var1
    data = [ 206398557001728L, 0L]
    return data
_tokenSet_3 = antlr.BitSet(mk_tokenSet_3())
