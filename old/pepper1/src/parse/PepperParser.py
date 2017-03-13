### $ANTLR 2.7.7 (20160104): "pepper.g" -> "PepperParser.py"$
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

class Parser(antlr.LLkParser):
    ### user action >>>
    ### user action <<<
    
    def __init__(self, *args, **kwargs):
        antlr.LLkParser.__init__(self, *args, **kwargs)
        self.tokenNames = _tokenNames
        self.buildTokenTypeASTClassMap()
        self.astFactory = antlr.ASTFactory(self.getTokenTypeToASTClassMap())
        self.astFactory.setASTNodeClass()
        
    def program(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        program_AST = None
        pass
        while True:
            if (self.LA(1)==NEWLINE):
                pass
                self.match(NEWLINE)
            else:
                break
            
        while True:
            if (_tokenSet_0.member(self.LA(1))):
                pass
                self.statement()
                self.addASTChild(currentAST, self.returnAST)
                while True:
                    if (self.LA(1)==NEWLINE):
                        pass
                        self.match(NEWLINE)
                    else:
                        break
                    
            else:
                break
            
        tmp3_AST = None
        tmp3_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp3_AST)
        self.match(EOF_TYPE)
        program_AST = currentAST.root
        self.returnAST = program_AST
    
    def statement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        statement_AST = None
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [LITERAL_def]:
            pass
            self.functionDefinition()
            self.addASTChild(currentAST, self.returnAST)
            statement_AST = currentAST.root
        elif la1 and la1 in [LITERAL_class]:
            pass
            self.classDefinition()
            self.addASTChild(currentAST, self.returnAST)
            statement_AST = currentAST.root
        elif la1 and la1 in [LITERAL_interface]:
            pass
            self.interfaceDefinition()
            self.addASTChild(currentAST, self.returnAST)
            statement_AST = currentAST.root
        elif la1 and la1 in [LITERAL_for]:
            pass
            self.forStatement()
            self.addASTChild(currentAST, self.returnAST)
            statement_AST = currentAST.root
        elif la1 and la1 in [LITERAL_while]:
            pass
            self.whileStatement()
            self.addASTChild(currentAST, self.returnAST)
            statement_AST = currentAST.root
        elif la1 and la1 in [LITERAL_import]:
            pass
            self.importStatement()
            self.addASTChild(currentAST, self.returnAST)
            statement_AST = currentAST.root
        else:
            if (_tokenSet_1.member(self.LA(1))) and (_tokenSet_2.member(self.LA(2))):
                pass
                self.initialisationOrExpression()
                self.addASTChild(currentAST, self.returnAST)
                statement_AST = currentAST.root
            elif (self.LA(1)==SYMBOL) and (self.LA(2)==PLUSEQUALS):
                pass
                self.modification()
                self.addASTChild(currentAST, self.returnAST)
                statement_AST = currentAST.root
            else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        self.returnAST = statement_AST
    
    def initialisationOrExpression(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        initialisationOrExpression_AST = None
        pass
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [SYMBOL]:
            pass
            tmp4_AST = None
            tmp4_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp4_AST)
            self.match(SYMBOL)
            tmp5_AST = None
            tmp5_AST = self.astFactory.create(self.LT(1))
            self.makeASTRoot(currentAST, tmp5_AST)
            self.match(EQUALS)
            self.expression()
            self.addASTChild(currentAST, self.returnAST)
        elif la1 and la1 in [NEWLINE]:
            pass
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        self.match(NEWLINE)
        initialisationOrExpression_AST = currentAST.root
        self.returnAST = initialisationOrExpression_AST
    
    def modification(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        modification_AST = None
        pass
        tmp7_AST = None
        tmp7_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp7_AST)
        self.match(SYMBOL)
        tmp8_AST = None
        tmp8_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp8_AST)
        self.match(PLUSEQUALS)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        modification_AST = currentAST.root
        self.returnAST = modification_AST
    
    def functionDefinition(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        functionDefinition_AST = None
        pass
        tmp10_AST = None
        tmp10_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp10_AST)
        self.match(LITERAL_def)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        tmp11_AST = None
        tmp11_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp11_AST)
        self.match(SYMBOL)
        self.typedArgumentsList()
        self.addASTChild(currentAST, self.returnAST)
        self.suite()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        functionDefinition_AST = currentAST.root
        self.returnAST = functionDefinition_AST
    
    def classDefinition(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        classDefinition_AST = None
        pass
        tmp13_AST = None
        tmp13_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp13_AST)
        self.match(LITERAL_class)
        tmp14_AST = None
        tmp14_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp14_AST)
        self.match(SYMBOL)
        self.classSuite()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        classDefinition_AST = currentAST.root
        self.returnAST = classDefinition_AST
    
    def interfaceDefinition(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        interfaceDefinition_AST = None
        pass
        tmp16_AST = None
        tmp16_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp16_AST)
        self.match(LITERAL_interface)
        tmp17_AST = None
        tmp17_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp17_AST)
        self.match(SYMBOL)
        self.interfaceSuite()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        interfaceDefinition_AST = currentAST.root
        self.returnAST = interfaceDefinition_AST
    
    def forStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        forStatement_AST = None
        pass
        tmp19_AST = None
        tmp19_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp19_AST)
        self.match(LITERAL_for)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        tmp20_AST = None
        tmp20_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp20_AST)
        self.match(SYMBOL)
        self.match(LITERAL_in)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        self.suite()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        forStatement_AST = currentAST.root
        self.returnAST = forStatement_AST
    
    def whileStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        whileStatement_AST = None
        pass
        tmp23_AST = None
        tmp23_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp23_AST)
        self.match(LITERAL_while)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        self.suite()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        whileStatement_AST = currentAST.root
        self.returnAST = whileStatement_AST
    
    def importStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        importStatement_AST = None
        pass
        tmp25_AST = None
        tmp25_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp25_AST)
        self.match(LITERAL_import)
        tmp26_AST = None
        tmp26_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp26_AST)
        self.match(SYMBOL)
        self.match(NEWLINE)
        importStatement_AST = currentAST.root
        self.returnAST = importStatement_AST
    
    def classStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        classStatement_AST = None
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,SYMBOL,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_for,LITERAL_while,LITERAL_import,LITERAL_if,LITERAL_quote]:
            pass
            self.statement()
            self.addASTChild(currentAST, self.returnAST)
            classStatement_AST = currentAST.root
        elif la1 and la1 in [LITERAL_def_init]:
            pass
            self.initFunctionDefinition()
            self.addASTChild(currentAST, self.returnAST)
            classStatement_AST = currentAST.root
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        self.returnAST = classStatement_AST
    
    def initFunctionDefinition(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        initFunctionDefinition_AST = None
        pass
        tmp28_AST = None
        tmp28_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp28_AST)
        self.match(LITERAL_def_init)
        self.typedArgumentsList()
        self.addASTChild(currentAST, self.returnAST)
        self.initFunctionSuite()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        initFunctionDefinition_AST = currentAST.root
        self.returnAST = initFunctionDefinition_AST
    
    def interfaceStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        interfaceStatement_AST = None
        pass
        self.interfaceFunctionDefinition()
        self.addASTChild(currentAST, self.returnAST)
        interfaceStatement_AST = currentAST.root
        self.returnAST = interfaceStatement_AST
    
    def interfaceFunctionDefinition(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        interfaceFunctionDefinition_AST = None
        pass
        tmp30_AST = None
        tmp30_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp30_AST)
        self.match(LITERAL_def)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        tmp31_AST = None
        tmp31_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp31_AST)
        self.match(SYMBOL)
        self.typedArgumentsList()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        interfaceFunctionDefinition_AST = currentAST.root
        self.returnAST = interfaceFunctionDefinition_AST
    
    def expression(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        expression_AST = None
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [LPAREN]:
            pass
            self.match(LPAREN)
            self.expression()
            self.addASTChild(currentAST, self.returnAST)
            self.match(RPAREN)
            expression_AST = currentAST.root
        elif la1 and la1 in [INT,FLOAT,STRING,SYMBOL,LITERAL_if,LITERAL_quote]:
            pass
            self.commaExpression()
            self.addASTChild(currentAST, self.returnAST)
            expression_AST = currentAST.root
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        self.returnAST = expression_AST
    
    def typedArgumentsList(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        typedArgumentsList_AST = None
        pass
        tmp35_AST = None
        tmp35_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp35_AST)
        self.match(LPAREN)
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,SYMBOL,LITERAL_if,LITERAL_quote]:
            pass
            self.noCommaExpression()
            self.addASTChild(currentAST, self.returnAST)
            tmp36_AST = None
            tmp36_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp36_AST)
            self.match(SYMBOL)
            while True:
                if (self.LA(1)==COMMA):
                    pass
                    tmp37_AST = None
                    tmp37_AST = self.astFactory.create(self.LT(1))
                    self.addASTChild(currentAST, tmp37_AST)
                    self.match(COMMA)
                    self.noCommaExpression()
                    self.addASTChild(currentAST, self.returnAST)
                    tmp38_AST = None
                    tmp38_AST = self.astFactory.create(self.LT(1))
                    self.addASTChild(currentAST, tmp38_AST)
                    self.match(SYMBOL)
                else:
                    break
                
        elif la1 and la1 in [RPAREN]:
            pass
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        self.match(RPAREN)
        typedArgumentsList_AST = currentAST.root
        self.returnAST = typedArgumentsList_AST
    
    def suite(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        suite_AST = None
        pass
        tmp40_AST = None
        tmp40_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp40_AST)
        self.match(COLON)
        self.suiteStart()
        self.addASTChild(currentAST, self.returnAST)
        _cnt113= 0
        while True:
            la1 = self.LA(1)
            if False:
                pass
            elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,SYMBOL,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_for,LITERAL_while,LITERAL_import,LITERAL_if,LITERAL_quote]:
                pass
                self.statement()
                self.addASTChild(currentAST, self.returnAST)
                while True:
                    if (self.LA(1)==NEWLINE):
                        pass
                        self.match(NEWLINE)
                    else:
                        break
                    
            elif la1 and la1 in [LITERAL_return]:
                pass
                self.returnStatement()
                self.addASTChild(currentAST, self.returnAST)
                while True:
                    if (self.LA(1)==NEWLINE):
                        pass
                        self.match(NEWLINE)
                    else:
                        break
                    
            else:
                    break
                
            _cnt113 += 1
        if _cnt113 < 1:
            raise antlr.NoViableAltException(self.LT(1), self.getFilename())
        self.suiteEnd()
        self.addASTChild(currentAST, self.returnAST)
        suite_AST = currentAST.root
        self.returnAST = suite_AST
    
    def initFunctionSuite(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        initFunctionSuite_AST = None
        pass
        tmp43_AST = None
        tmp43_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp43_AST)
        self.match(COLON)
        self.suiteStart()
        self.addASTChild(currentAST, self.returnAST)
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [LITERAL_var]:
            pass
            pass
            self.varStatement()
            self.addASTChild(currentAST, self.returnAST)
            while True:
                if (_tokenSet_0.member(self.LA(1))):
                    pass
                    self.statement()
                    self.addASTChild(currentAST, self.returnAST)
                    while True:
                        if (self.LA(1)==NEWLINE):
                            pass
                            self.match(NEWLINE)
                        else:
                            break
                        
                else:
                    break
                
        elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,SYMBOL,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_for,LITERAL_while,LITERAL_import,LITERAL_if,LITERAL_quote]:
            pass
            _cnt134= 0
            while True:
                if (_tokenSet_0.member(self.LA(1))):
                    pass
                    self.statement()
                    self.addASTChild(currentAST, self.returnAST)
                    while True:
                        if (self.LA(1)==NEWLINE):
                            pass
                            self.match(NEWLINE)
                        else:
                            break
                        
                else:
                    break
                
                _cnt134 += 1
            if _cnt134 < 1:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        self.suiteEnd()
        self.addASTChild(currentAST, self.returnAST)
        initFunctionSuite_AST = currentAST.root
        self.returnAST = initFunctionSuite_AST
    
    def classSuite(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        classSuite_AST = None
        pass
        tmp46_AST = None
        tmp46_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp46_AST)
        self.match(COLON)
        self.suiteStart()
        self.addASTChild(currentAST, self.returnAST)
        _cnt118= 0
        while True:
            if (_tokenSet_3.member(self.LA(1))):
                pass
                self.classStatement()
                self.addASTChild(currentAST, self.returnAST)
                while True:
                    if (self.LA(1)==NEWLINE):
                        pass
                        self.match(NEWLINE)
                    else:
                        break
                    
            else:
                break
            
            _cnt118 += 1
        if _cnt118 < 1:
            raise antlr.NoViableAltException(self.LT(1), self.getFilename())
        self.suiteEnd()
        self.addASTChild(currentAST, self.returnAST)
        classSuite_AST = currentAST.root
        self.returnAST = classSuite_AST
    
    def interfaceSuite(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        interfaceSuite_AST = None
        pass
        tmp48_AST = None
        tmp48_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp48_AST)
        self.match(COLON)
        self.suiteStart()
        self.addASTChild(currentAST, self.returnAST)
        _cnt123= 0
        while True:
            if (self.LA(1)==LITERAL_def):
                pass
                self.interfaceStatement()
                self.addASTChild(currentAST, self.returnAST)
                while True:
                    if (self.LA(1)==NEWLINE):
                        pass
                        self.match(NEWLINE)
                    else:
                        break
                    
            else:
                break
            
            _cnt123 += 1
        if _cnt123 < 1:
            raise antlr.NoViableAltException(self.LT(1), self.getFilename())
        self.suiteEnd()
        self.addASTChild(currentAST, self.returnAST)
        interfaceSuite_AST = currentAST.root
        self.returnAST = interfaceSuite_AST
    
    def noCommaExpression(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        noCommaExpression_AST = None
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [LPAREN]:
            pass
            self.match(LPAREN)
            self.expression()
            self.addASTChild(currentAST, self.returnAST)
            self.match(RPAREN)
            noCommaExpression_AST = currentAST.root
        elif la1 and la1 in [INT,FLOAT,STRING,SYMBOL,LITERAL_if,LITERAL_quote]:
            pass
            self.calcExpression()
            self.addASTChild(currentAST, self.returnAST)
            noCommaExpression_AST = currentAST.root
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        self.returnAST = noCommaExpression_AST
    
    def calcExpression(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        calcExpression_AST = None
        pass
        self.simpleExpression()
        self.addASTChild(currentAST, self.returnAST)
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [PLUS,MINUS,TIMES,GT,LT]:
            pass
            la1 = self.LA(1)
            if False:
                pass
            elif la1 and la1 in [PLUS]:
                pass
                tmp52_AST = None
                tmp52_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp52_AST)
                self.match(PLUS)
            elif la1 and la1 in [MINUS]:
                pass
                tmp53_AST = None
                tmp53_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp53_AST)
                self.match(MINUS)
            elif la1 and la1 in [TIMES]:
                pass
                tmp54_AST = None
                tmp54_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp54_AST)
                self.match(TIMES)
            elif la1 and la1 in [GT]:
                pass
                tmp55_AST = None
                tmp55_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp55_AST)
                self.match(GT)
            elif la1 and la1 in [LT]:
                pass
                tmp56_AST = None
                tmp56_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp56_AST)
                self.match(LT)
            else:
                    raise antlr.NoViableAltException(self.LT(1), self.getFilename())
                
            self.noCommaExpression()
            self.addASTChild(currentAST, self.returnAST)
        elif la1 and la1 in [RPAREN,RSQUBR,COMMA,SYMBOL,NEWLINE,COLON]:
            pass
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        calcExpression_AST = currentAST.root
        self.returnAST = calcExpression_AST
    
    def commaExpression(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        commaExpression_AST = None
        pass
        self.calcExpression()
        self.addASTChild(currentAST, self.returnAST)
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [COMMA]:
            pass
            tmp57_AST = None
            tmp57_AST = self.astFactory.create(self.LT(1))
            self.makeASTRoot(currentAST, tmp57_AST)
            self.match(COMMA)
            self.calcExpression()
            self.addASTChild(currentAST, self.returnAST)
            while True:
                if (self.LA(1)==COMMA):
                    pass
                    self.match(COMMA)
                    self.calcExpression()
                    self.addASTChild(currentAST, self.returnAST)
                else:
                    break
                
        elif la1 and la1 in [RPAREN,RSQUBR,SYMBOL,NEWLINE,COLON]:
            pass
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        commaExpression_AST = currentAST.root
        self.returnAST = commaExpression_AST
    
    def simpleExpression(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        simpleExpression_AST = None
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [INT]:
            pass
            tmp59_AST = None
            tmp59_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp59_AST)
            self.match(INT)
            simpleExpression_AST = currentAST.root
        elif la1 and la1 in [FLOAT]:
            pass
            tmp60_AST = None
            tmp60_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp60_AST)
            self.match(FLOAT)
            simpleExpression_AST = currentAST.root
        elif la1 and la1 in [STRING]:
            pass
            tmp61_AST = None
            tmp61_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp61_AST)
            self.match(STRING)
            simpleExpression_AST = currentAST.root
        elif la1 and la1 in [LITERAL_if]:
            pass
            self.ifExpression()
            self.addASTChild(currentAST, self.returnAST)
            simpleExpression_AST = currentAST.root
        elif la1 and la1 in [LITERAL_quote]:
            pass
            self.quotedCode()
            self.addASTChild(currentAST, self.returnAST)
            simpleExpression_AST = currentAST.root
        else:
            if (self.LA(1)==SYMBOL) and (_tokenSet_4.member(self.LA(2))):
                pass
                tmp62_AST = None
                tmp62_AST = self.astFactory.create(self.LT(1))
                self.addASTChild(currentAST, tmp62_AST)
                self.match(SYMBOL)
                simpleExpression_AST = currentAST.root
            elif (self.LA(1)==SYMBOL) and (self.LA(2)==LPAREN):
                pass
                self.functionCall()
                self.addASTChild(currentAST, self.returnAST)
                simpleExpression_AST = currentAST.root
            elif (self.LA(1)==SYMBOL) and (self.LA(2)==LSQUBR):
                pass
                self.arrayLookup()
                self.addASTChild(currentAST, self.returnAST)
                simpleExpression_AST = currentAST.root
            else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        self.returnAST = simpleExpression_AST
    
    def functionCall(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        functionCall_AST = None
        pass
        tmp63_AST = None
        tmp63_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp63_AST)
        self.match(SYMBOL)
        tmp64_AST = None
        tmp64_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp64_AST)
        self.match(LPAREN)
        self.argumentsList()
        self.addASTChild(currentAST, self.returnAST)
        self.match(RPAREN)
        functionCall_AST = currentAST.root
        self.returnAST = functionCall_AST
    
    def arrayLookup(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        arrayLookup_AST = None
        pass
        tmp66_AST = None
        tmp66_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp66_AST)
        self.match(SYMBOL)
        tmp67_AST = None
        tmp67_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp67_AST)
        self.match(LSQUBR)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        self.match(RSQUBR)
        arrayLookup_AST = currentAST.root
        self.returnAST = arrayLookup_AST
    
    def ifExpression(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        ifExpression_AST = None
        pass
        tmp69_AST = None
        tmp69_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp69_AST)
        self.match(LITERAL_if)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        self.suite()
        self.addASTChild(currentAST, self.returnAST)
        if (self.LA(1)==NEWLINE) and (self.LA(2)==LITERAL_else):
            pass
            self.match(NEWLINE)
            tmp71_AST = None
            tmp71_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp71_AST)
            self.match(LITERAL_else)
            self.suite()
            self.addASTChild(currentAST, self.returnAST)
        elif (_tokenSet_4.member(self.LA(1))) and (_tokenSet_5.member(self.LA(2))):
            pass
        else:
            raise antlr.NoViableAltException(self.LT(1), self.getFilename())
        
        ifExpression_AST = currentAST.root
        self.returnAST = ifExpression_AST
    
    def quotedCode(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        quotedCode_AST = None
        pass
        tmp72_AST = None
        tmp72_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp72_AST)
        self.match(LITERAL_quote)
        self.suite()
        self.addASTChild(currentAST, self.returnAST)
        quotedCode_AST = currentAST.root
        self.returnAST = quotedCode_AST
    
    def argumentsList(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        argumentsList_AST = None
        pass
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,SYMBOL,LITERAL_if,LITERAL_quote]:
            pass
            self.noCommaExpression()
            self.addASTChild(currentAST, self.returnAST)
            while True:
                if (self.LA(1)==COMMA):
                    pass
                    tmp73_AST = None
                    tmp73_AST = self.astFactory.create(self.LT(1))
                    self.addASTChild(currentAST, tmp73_AST)
                    self.match(COMMA)
                    self.noCommaExpression()
                    self.addASTChild(currentAST, self.returnAST)
                else:
                    break
                
        elif la1 and la1 in [RPAREN]:
            pass
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        argumentsList_AST = currentAST.root
        self.returnAST = argumentsList_AST
    
    def suiteStart(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        suiteStart_AST = None
        pass
        _cnt103= 0
        while True:
            if (self.LA(1)==NEWLINE):
                pass
                self.match(NEWLINE)
            else:
                break
            
            _cnt103 += 1
        if _cnt103 < 1:
            raise antlr.NoViableAltException(self.LT(1), self.getFilename())
        self.match(INDENT)
        while True:
            if (self.LA(1)==NEWLINE):
                pass
                self.match(NEWLINE)
            else:
                break
            
        suiteStart_AST = currentAST.root
        self.returnAST = suiteStart_AST
    
    def suiteEnd(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        suiteEnd_AST = None
        pass
        self.match(DEDENT)
        suiteEnd_AST = currentAST.root
        self.returnAST = suiteEnd_AST
    
    def returnStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        returnStatement_AST = None
        pass
        tmp78_AST = None
        tmp78_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp78_AST)
        self.match(LITERAL_return)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        returnStatement_AST = currentAST.root
        self.returnAST = returnStatement_AST
    
    def varStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        varStatement_AST = None
        pass
        tmp80_AST = None
        tmp80_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp80_AST)
        self.match(LITERAL_var)
        self.varSuite()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        varStatement_AST = currentAST.root
        self.returnAST = varStatement_AST
    
    def varSuite(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        varSuite_AST = None
        pass
        tmp82_AST = None
        tmp82_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp82_AST)
        self.match(COLON)
        self.suiteStart()
        self.addASTChild(currentAST, self.returnAST)
        _cnt139= 0
        while True:
            if (_tokenSet_1.member(self.LA(1))):
                pass
                self.initialisation()
                self.addASTChild(currentAST, self.returnAST)
                while True:
                    if (self.LA(1)==NEWLINE):
                        pass
                        self.match(NEWLINE)
                    else:
                        break
                    
            else:
                break
            
            _cnt139 += 1
        if _cnt139 < 1:
            raise antlr.NoViableAltException(self.LT(1), self.getFilename())
        self.suiteEnd()
        self.addASTChild(currentAST, self.returnAST)
        varSuite_AST = currentAST.root
        self.returnAST = varSuite_AST
    
    def initialisation(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        initialisation_AST = None
        pass
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        tmp84_AST = None
        tmp84_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp84_AST)
        self.match(SYMBOL)
        tmp85_AST = None
        tmp85_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp85_AST)
        self.match(EQUALS)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        self.match(NEWLINE)
        initialisation_AST = currentAST.root
        self.returnAST = initialisation_AST
    
    
    def buildTokenTypeASTClassMap(self):
        self.tokenTypeToASTClassMap = None

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
    data = [ 206296004171776L, 0L]
    return data
_tokenSet_0 = antlr.BitSet(mk_tokenSet_0())

### generate bit set
def mk_tokenSet_1(): 
    ### var1
    data = [ 175921995454464L, 0L]
    return data
_tokenSet_1 = antlr.BitSet(mk_tokenSet_1())

### generate bit set
def mk_tokenSet_2(): 
    ### var1
    data = [ 175986162014208L, 0L]
    return data
_tokenSet_2 = antlr.BitSet(mk_tokenSet_2())

### generate bit set
def mk_tokenSet_3(): 
    ### var1
    data = [ 206570882078720L, 0L]
    return data
_tokenSet_3 = antlr.BitSet(mk_tokenSet_3())

### generate bit set
def mk_tokenSet_4(): 
    ### var1
    data = [ 64303923200L, 0L]
    return data
_tokenSet_4 = antlr.BitSet(mk_tokenSet_4())

### generate bit set
def mk_tokenSet_5(): 
    ### var1
    data = [ 774051771193378L, 0L]
    return data
_tokenSet_5 = antlr.BitSet(mk_tokenSet_5())
    
