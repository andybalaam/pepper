### $ANTLR 2.7.7 (20160104): "newsyntaxpepper.g" -> "NewSyntaxPepperParser.py"$
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
            if (_tokenSet_0.member(self.LA(1))):
                pass
                self.statement()
                self.addASTChild(currentAST, self.returnAST)
            else:
                break
            
        tmp31_AST = None
        tmp31_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp31_AST)
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
        elif la1 and la1 in [SEMICOLON]:
            pass
            tmp32_AST = None
            tmp32_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp32_AST)
            self.match(SEMICOLON)
            statement_AST = currentAST.root
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
        elif la1 and la1 in [LBRACE]:
            pass
            self.codeBlock()
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
        if (self.LA(1)==SYMBOL) and (self.LA(2)==EQUALS):
            pass
            tmp33_AST = None
            tmp33_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp33_AST)
            self.match(SYMBOL)
            tmp34_AST = None
            tmp34_AST = self.astFactory.create(self.LT(1))
            self.makeASTRoot(currentAST, tmp34_AST)
            self.match(EQUALS)
            self.expression()
            self.addASTChild(currentAST, self.returnAST)
        elif (_tokenSet_3.member(self.LA(1))) and (_tokenSet_4.member(self.LA(2))):
            pass
        else:
            raise antlr.NoViableAltException(self.LT(1), self.getFilename())
        
        initialisationOrExpression_AST = currentAST.root
        self.returnAST = initialisationOrExpression_AST
    
    def modification(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        modification_AST = None
        pass
        tmp35_AST = None
        tmp35_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp35_AST)
        self.match(SYMBOL)
        tmp36_AST = None
        tmp36_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp36_AST)
        self.match(PLUSEQUALS)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        modification_AST = currentAST.root
        self.returnAST = modification_AST
    
    def functionDefinition(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        functionDefinition_AST = None
        pass
        tmp37_AST = None
        tmp37_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp37_AST)
        self.match(LITERAL_def)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        tmp38_AST = None
        tmp38_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp38_AST)
        self.match(SYMBOL)
        self.typedArgumentsList()
        self.addASTChild(currentAST, self.returnAST)
        self.suite()
        self.addASTChild(currentAST, self.returnAST)
        functionDefinition_AST = currentAST.root
        self.returnAST = functionDefinition_AST
    
    def classDefinition(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        classDefinition_AST = None
        pass
        tmp39_AST = None
        tmp39_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp39_AST)
        self.match(LITERAL_class)
        tmp40_AST = None
        tmp40_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp40_AST)
        self.match(SYMBOL)
        self.classSuite()
        self.addASTChild(currentAST, self.returnAST)
        classDefinition_AST = currentAST.root
        self.returnAST = classDefinition_AST
    
    def interfaceDefinition(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        interfaceDefinition_AST = None
        pass
        tmp41_AST = None
        tmp41_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp41_AST)
        self.match(LITERAL_interface)
        tmp42_AST = None
        tmp42_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp42_AST)
        self.match(SYMBOL)
        self.interfaceSuite()
        self.addASTChild(currentAST, self.returnAST)
        interfaceDefinition_AST = currentAST.root
        self.returnAST = interfaceDefinition_AST
    
    def whileStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        whileStatement_AST = None
        pass
        tmp43_AST = None
        tmp43_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp43_AST)
        self.match(LITERAL_while)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        self.suite()
        self.addASTChild(currentAST, self.returnAST)
        whileStatement_AST = currentAST.root
        self.returnAST = whileStatement_AST
    
    def importStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        importStatement_AST = None
        pass
        tmp44_AST = None
        tmp44_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp44_AST)
        self.match(LITERAL_import)
        tmp45_AST = None
        tmp45_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp45_AST)
        self.match(SYMBOL)
        importStatement_AST = currentAST.root
        self.returnAST = importStatement_AST
    
    def codeBlock(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        codeBlock_AST = None
        pass
        tmp46_AST = None
        tmp46_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp46_AST)
        self.match(LBRACE)
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [PIPE]:
            pass
            self.codeBlockArgs()
            self.addASTChild(currentAST, self.returnAST)
        elif la1 and la1 in [INT,FLOAT,STRING,LBRACE,RBRACE,LPAREN,SEMICOLON,SYMBOL,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_while,LITERAL_import,LITERAL_quote]:
            pass
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        while True:
            if (_tokenSet_0.member(self.LA(1))):
                pass
                self.statement()
                self.addASTChild(currentAST, self.returnAST)
            else:
                break
            
        self.match(RBRACE)
        codeBlock_AST = currentAST.root
        self.returnAST = codeBlock_AST
    
    def codeBlockArgs(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        codeBlockArgs_AST = None
        pass
        tmp48_AST = None
        tmp48_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp48_AST)
        self.match(PIPE)
        tmp49_AST = None
        tmp49_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp49_AST)
        self.match(SYMBOL)
        self.match(PIPE)
        codeBlockArgs_AST = currentAST.root
        self.returnAST = codeBlockArgs_AST
    
    def classStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        classStatement_AST = None
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [INT,FLOAT,STRING,LBRACE,LPAREN,SEMICOLON,SYMBOL,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_while,LITERAL_import,LITERAL_quote]:
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
        tmp51_AST = None
        tmp51_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp51_AST)
        self.match(LITERAL_def_init)
        self.typedArgumentsList()
        self.addASTChild(currentAST, self.returnAST)
        self.initFunctionSuite()
        self.addASTChild(currentAST, self.returnAST)
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
        tmp52_AST = None
        tmp52_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp52_AST)
        self.match(LITERAL_def)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        tmp53_AST = None
        tmp53_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp53_AST)
        self.match(SYMBOL)
        self.typedArgumentsList()
        self.addASTChild(currentAST, self.returnAST)
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
        elif la1 and la1 in [INT,FLOAT,STRING,SYMBOL,LITERAL_quote]:
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
        tmp56_AST = None
        tmp56_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp56_AST)
        self.match(LPAREN)
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,SYMBOL,LITERAL_quote]:
            pass
            self.noCommaExpression()
            self.addASTChild(currentAST, self.returnAST)
            tmp57_AST = None
            tmp57_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp57_AST)
            self.match(SYMBOL)
            while True:
                if (self.LA(1)==COMMA):
                    pass
                    tmp58_AST = None
                    tmp58_AST = self.astFactory.create(self.LT(1))
                    self.addASTChild(currentAST, tmp58_AST)
                    self.match(COMMA)
                    self.noCommaExpression()
                    self.addASTChild(currentAST, self.returnAST)
                    tmp59_AST = None
                    tmp59_AST = self.astFactory.create(self.LT(1))
                    self.addASTChild(currentAST, tmp59_AST)
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
        tmp61_AST = None
        tmp61_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp61_AST)
        self.match(COLON)
        self.suiteStart()
        self.addASTChild(currentAST, self.returnAST)
        _cnt114= 0
        while True:
            la1 = self.LA(1)
            if False:
                pass
            elif la1 and la1 in [INT,FLOAT,STRING,LBRACE,LPAREN,SEMICOLON,SYMBOL,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_while,LITERAL_import,LITERAL_quote]:
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
                
            _cnt114 += 1
        if _cnt114 < 1:
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
        tmp64_AST = None
        tmp64_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp64_AST)
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
                
        elif la1 and la1 in [INT,FLOAT,STRING,LBRACE,LPAREN,SEMICOLON,SYMBOL,LITERAL_def,LITERAL_class,LITERAL_interface,LITERAL_while,LITERAL_import,LITERAL_quote]:
            pass
            _cnt135= 0
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
                
                _cnt135 += 1
            if _cnt135 < 1:
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
        tmp67_AST = None
        tmp67_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp67_AST)
        self.match(COLON)
        self.suiteStart()
        self.addASTChild(currentAST, self.returnAST)
        _cnt119= 0
        while True:
            if (_tokenSet_5.member(self.LA(1))):
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
            
            _cnt119 += 1
        if _cnt119 < 1:
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
        tmp69_AST = None
        tmp69_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp69_AST)
        self.match(COLON)
        self.suiteStart()
        self.addASTChild(currentAST, self.returnAST)
        _cnt124= 0
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
            
            _cnt124 += 1
        if _cnt124 < 1:
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
        elif la1 and la1 in [INT,FLOAT,STRING,SYMBOL,LITERAL_quote]:
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
        elif la1 and la1 in [PLUS,MINUS,TIMES,GT,LT,EQUALSEQUALS]:
            pass
            la1 = self.LA(1)
            if False:
                pass
            elif la1 and la1 in [EQUALSEQUALS]:
                pass
                tmp73_AST = None
                tmp73_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp73_AST)
                self.match(EQUALSEQUALS)
            elif la1 and la1 in [PLUS]:
                pass
                tmp74_AST = None
                tmp74_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp74_AST)
                self.match(PLUS)
            elif la1 and la1 in [MINUS]:
                pass
                tmp75_AST = None
                tmp75_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp75_AST)
                self.match(MINUS)
            elif la1 and la1 in [TIMES]:
                pass
                tmp76_AST = None
                tmp76_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp76_AST)
                self.match(TIMES)
            elif la1 and la1 in [GT]:
                pass
                tmp77_AST = None
                tmp77_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp77_AST)
                self.match(GT)
            elif la1 and la1 in [LT]:
                pass
                tmp78_AST = None
                tmp78_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp78_AST)
                self.match(LT)
            else:
                    raise antlr.NoViableAltException(self.LT(1), self.getFilename())
                
            self.noCommaExpression()
            self.addASTChild(currentAST, self.returnAST)
        elif la1 and la1 in [EOF,INT,DOT,FLOAT,STRING,LBRACE,RBRACE,LPAREN,RPAREN,RSQUBR,COMMA,SEMICOLON,SYMBOL,COLON,LITERAL_def,LITERAL_def_init,LITERAL_class,LITERAL_interface,LITERAL_while,LITERAL_import,LITERAL_quote,NEWLINE,DEDENT,LITERAL_return]:
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
        self.lookupExpression()
        self.addASTChild(currentAST, self.returnAST)
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [COMMA]:
            pass
            tmp79_AST = None
            tmp79_AST = self.astFactory.create(self.LT(1))
            self.makeASTRoot(currentAST, tmp79_AST)
            self.match(COMMA)
            self.lookupExpression()
            self.addASTChild(currentAST, self.returnAST)
            while True:
                if (self.LA(1)==COMMA):
                    pass
                    self.match(COMMA)
                    self.lookupExpression()
                    self.addASTChild(currentAST, self.returnAST)
                else:
                    break
                
        elif la1 and la1 in [EOF,INT,FLOAT,STRING,LBRACE,RBRACE,LPAREN,RPAREN,RSQUBR,SEMICOLON,SYMBOL,COLON,LITERAL_def,LITERAL_def_init,LITERAL_class,LITERAL_interface,LITERAL_while,LITERAL_import,LITERAL_quote,NEWLINE,DEDENT,LITERAL_return]:
            pass
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        commaExpression_AST = currentAST.root
        self.returnAST = commaExpression_AST
    
    def lookupExpression(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        lookupExpression_AST = None
        pass
        self.calcExpression()
        self.addASTChild(currentAST, self.returnAST)
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [DOT]:
            pass
            tmp81_AST = None
            tmp81_AST = self.astFactory.create(self.LT(1))
            self.makeASTRoot(currentAST, tmp81_AST)
            self.match(DOT)
            self.calcExpression()
            self.addASTChild(currentAST, self.returnAST)
        elif la1 and la1 in [EOF,INT,FLOAT,STRING,LBRACE,RBRACE,LPAREN,RPAREN,RSQUBR,COMMA,SEMICOLON,SYMBOL,COLON,LITERAL_def,LITERAL_def_init,LITERAL_class,LITERAL_interface,LITERAL_while,LITERAL_import,LITERAL_quote,NEWLINE,DEDENT,LITERAL_return]:
            pass
        else:
                raise antlr.NoViableAltException(self.LT(1), self.getFilename())
            
        lookupExpression_AST = currentAST.root
        self.returnAST = lookupExpression_AST
    
    def simpleExpression(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        simpleExpression_AST = None
        la1 = self.LA(1)
        if False:
            pass
        elif la1 and la1 in [INT]:
            pass
            tmp82_AST = None
            tmp82_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp82_AST)
            self.match(INT)
            simpleExpression_AST = currentAST.root
        elif la1 and la1 in [FLOAT]:
            pass
            tmp83_AST = None
            tmp83_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp83_AST)
            self.match(FLOAT)
            simpleExpression_AST = currentAST.root
        elif la1 and la1 in [STRING]:
            pass
            tmp84_AST = None
            tmp84_AST = self.astFactory.create(self.LT(1))
            self.addASTChild(currentAST, tmp84_AST)
            self.match(STRING)
            simpleExpression_AST = currentAST.root
        elif la1 and la1 in [LITERAL_quote]:
            pass
            self.quotedCode()
            self.addASTChild(currentAST, self.returnAST)
            simpleExpression_AST = currentAST.root
        else:
            if (self.LA(1)==SYMBOL) and (_tokenSet_6.member(self.LA(2))):
                pass
                self.functionCallOrSymbol()
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
    
    def functionCallOrSymbol(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        functionCallOrSymbol_AST = None
        pass
        tmp85_AST = None
        tmp85_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp85_AST)
        self.match(SYMBOL)
        while True:
            if (self.LA(1)==LPAREN) and (_tokenSet_7.member(self.LA(2))):
                pass
                tmp86_AST = None
                tmp86_AST = self.astFactory.create(self.LT(1))
                self.makeASTRoot(currentAST, tmp86_AST)
                self.match(LPAREN)
                self.argumentsList()
                self.addASTChild(currentAST, self.returnAST)
                self.match(RPAREN)
            else:
                break
            
        functionCallOrSymbol_AST = currentAST.root
        self.returnAST = functionCallOrSymbol_AST
    
    def arrayLookup(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        arrayLookup_AST = None
        pass
        tmp88_AST = None
        tmp88_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp88_AST)
        self.match(SYMBOL)
        tmp89_AST = None
        tmp89_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp89_AST)
        self.match(LSQUBR)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        self.match(RSQUBR)
        arrayLookup_AST = currentAST.root
        self.returnAST = arrayLookup_AST
    
    def quotedCode(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        quotedCode_AST = None
        pass
        tmp91_AST = None
        tmp91_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp91_AST)
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
        elif la1 and la1 in [INT,FLOAT,STRING,LPAREN,SYMBOL,LITERAL_quote]:
            pass
            self.noCommaExpression()
            self.addASTChild(currentAST, self.returnAST)
            while True:
                if (self.LA(1)==COMMA):
                    pass
                    tmp92_AST = None
                    tmp92_AST = self.astFactory.create(self.LT(1))
                    self.addASTChild(currentAST, tmp92_AST)
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
        _cnt104= 0
        while True:
            if (self.LA(1)==NEWLINE):
                pass
                self.match(NEWLINE)
            else:
                break
            
            _cnt104 += 1
        if _cnt104 < 1:
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
        tmp97_AST = None
        tmp97_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp97_AST)
        self.match(LITERAL_return)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        returnStatement_AST = currentAST.root
        self.returnAST = returnStatement_AST
    
    def varStatement(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        varStatement_AST = None
        pass
        tmp98_AST = None
        tmp98_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp98_AST)
        self.match(LITERAL_var)
        self.varSuite()
        self.addASTChild(currentAST, self.returnAST)
        varStatement_AST = currentAST.root
        self.returnAST = varStatement_AST
    
    def varSuite(self):    
        
        self.returnAST = None
        currentAST = antlr.ASTPair()
        varSuite_AST = None
        pass
        tmp99_AST = None
        tmp99_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp99_AST)
        self.match(COLON)
        self.suiteStart()
        self.addASTChild(currentAST, self.returnAST)
        _cnt140= 0
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
            
            _cnt140 += 1
        if _cnt140 < 1:
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
        tmp101_AST = None
        tmp101_AST = self.astFactory.create(self.LT(1))
        self.addASTChild(currentAST, tmp101_AST)
        self.match(SYMBOL)
        tmp102_AST = None
        tmp102_AST = self.astFactory.create(self.LT(1))
        self.makeASTRoot(currentAST, tmp102_AST)
        self.match(EQUALS)
        self.expression()
        self.addASTChild(currentAST, self.returnAST)
        initialisation_AST = currentAST.root
        self.returnAST = initialisation_AST
    
    
    def buildTokenTypeASTClassMap(self):
        self.tokenTypeToASTClassMap = None

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
    data = [ 34360041604352L, 0L]
    return data
_tokenSet_0 = antlr.BitSet(mk_tokenSet_0())

### generate bit set
def mk_tokenSet_1(): 
    ### var1
    data = [ 17592455595264L, 0L]
    return data
_tokenSet_1 = antlr.BitSet(mk_tokenSet_1())

### generate bit set
def mk_tokenSet_2(): 
    ### var1
    data = [ 773982959109890L, 0L]
    return data
_tokenSet_2 = antlr.BitSet(mk_tokenSet_2())

### generate bit set
def mk_tokenSet_3(): 
    ### var1
    data = [ 773781611545858L, 0L]
    return data
_tokenSet_3 = antlr.BitSet(mk_tokenSet_3())

### generate bit set
def mk_tokenSet_4(): 
    ### var1
    data = [ 773987265087234L, 0L]
    return data
_tokenSet_4 = antlr.BitSet(mk_tokenSet_4())

### generate bit set
def mk_tokenSet_5(): 
    ### var1
    data = [ 34909797418240L, 0L]
    return data
_tokenSet_5 = antlr.BitSet(mk_tokenSet_5())

### generate bit set
def mk_tokenSet_6(): 
    ### var1
    data = [ 773982965401346L, 0L]
    return data
_tokenSet_6 = antlr.BitSet(mk_tokenSet_6())

### generate bit set
def mk_tokenSet_7(): 
    ### var1
    data = [ 17592457692416L, 0L]
    return data
_tokenSet_7 = antlr.BitSet(mk_tokenSet_7())
    
