from Tokenizer import *
from VMWriter import *
from SymbolTable import *


class CompilationEngine:
    
    
    def __init__(self,inFile, outFile):
        self.currentClass = ""
        self.currentSubroutine = ""
        self.tokenizer = Tokenizer(inFile)
        self.vmWriter = VMWriter(outFile)
        self.symbolTable = SymbolTable()
        self.labelIndex = 0


    def currentFunction(self):
        if len(self.currentClass) != 0 and len(self.currentSubroutine) != 0:
            return str(self.currentClass) + "." + str(self.currentSubroutine)

        return ""
    
    def compileType(self):
        self.tokenizer.advance()

        if (self.tokenizer.tokenType() == Tokenizer.TYPE.KEYWORD 
        and (self.tokenizer.keyWord() == Tokenizer.KEYWORD.INT 
        or self.tokenizer.keyWord() == Tokenizer.KEYWORD.CHAR 
        or self.tokenizer.keyWord() == Tokenizer.KEYWORD.BOOLEAN)):
            return self.tokenizer.getCurrentToken()

        if self.tokenizer.tokenType() == Tokenizer.TYPE.IDENTIFIER:
            return self.tokenizer.identifier()

        self.error("in|char|boolean|className")


        return ""

    def compileClass(self):
        self.tokenizer.advance()

        if (self.tokenizer.tokenType() != self.tokenizer.TYPE.KEYWORD or self.tokenizer.keyWord() != self.tokenizer.KEYWORD.CLASS):
            print(self.tokenizer.getCurrentToken())
            self.error("class")
        
        self.tokenizer.advance()

        if (self.tokenizer.tokenType() != self.tokenizer.TYPE.IDENTIFIER):
            self.error("className")
        

        
        self.currentClass = self.tokenizer.identifier()
        self.requireSymbol('{')
        self.compileClassVarDec()
        self.compileSubroutine()
        self.requireSymbol('}')

        if (self.tokenizer.hasMoreTokens()):
            self.error("Unexpected tokens")
        
        self.vmWriter.close()


    def compileClassVarDec(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == self.tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '}'):
            self.tokenizer.pointerBack()
            return 
        
        if (self.tokenizer.tokenType() != Tokenizer.TYPE.KEYWORD):
            error("Keywords")
        
        if (self.tokenizer.keyWord() == Tokenizer.KEYWORD.CONSTRUCTOR or self.tokenizer.keyWord() == Tokenizer.KEYWORD.FUNCTION or self.tokenizer.keyWord() == Tokenizer.KEYWORD.METHOD):
            self.tokenizer.pointerBack()
            return 

        if (self.tokenizer.keyWord() != Tokenizer.KEYWORD.STATIC and self.tokenizer.keyWord() != Tokenizer.KEYWORD.FIELD):
            error("static or field")
        
        kind = None
        typeT = ""
        name = ""

        if self.tokenizer.keyWord() == Symbol.KIND.STATIC:
            kind = Symbol.KIND.STATIC
        elif self.tokenizer.keyWord() == Symbol.KIND.FIELD:
            kind = Symbol.KIND.FIELD
        '''
        switch (tokenizer.keyWord()){
            case STATIC:kind = Symbol.KIND.STATIC;break;
            case FIELD:kind = Symbol.KIND.FIELD;break;
        }
        '''
        typeT = self.compileType()
        varNamesDone = False
        while True:
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != Tokenizer.TYPE.IDENTIFIER):
                error("identifier")
            
            name = self.tokenizer.identifier()

            self.symbolTable.define(name,typeT,kind)

            self.tokenizer.advance()

            if (self.tokenizer.tokenType() != Tokenizer.TYPE.SYMBOL or (self.tokenizer.symbol() != ',' and self.tokenizer.symbol() != ';')):
                error("',' or ';'")

            if (self.tokenizer.symbol() == ';'):
                break

        self.compileClassVarDec()
    

    def compileSubroutine(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '}'):
            self.tokenizer.pointerBack()
            return

        if (self.tokenizer.tokenType() != Tokenizer.TYPE.KEYWORD or (self.tokenizer.keyWord() != Tokenizer.KEYWORD.CONSTRUCTOR 
        and self.tokenizer.keyWord() != Tokenizer.KEYWORD.FUNCTION 
        and self.tokenizer.keyWord() != Tokenizer.KEYWORD.METHOD)):
            error("constructor|fun|method")

        keyword = self.tokenizer.keyWord()

        self.symbolTable.startSubroutine()

        if (self.tokenizer.keyWord() == Tokenizer.KEYWORD.METHOD):
            self.symbolTable.define("this",self.currentClass, Symbol.KIND.ARG)

        typeT = ""

        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == Tokenizer.TYPE.KEYWORD and self.tokenizer.keyWord() == Tokenizer.KEYWORD.VOID):
            typeT = "void"
        else:
            self.tokenizer.pointerBack()
            typeT = self.compileType()
        
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != Tokenizer.TYPE.IDENTIFIER):
            self.error("subroutineName")

        self.currentSubroutine = self.tokenizer.identifier()

        
        self.requireSymbol('(')

        
        self.compileParameterList()

        
        self.requireSymbol(')')

        self.compileSubroutineBody(keyword)

        self.compileSubroutine()

    
    def compileSubroutineBody(self, keyword):
        
        self.requireSymbol('{')
        self.compileVarDec()
        self.writeFunctionDec(keyword)

        self.compileStatement()
        self.requireSymbol('}')


    def writeFunctionDec(self, keyword):

        self.vmWriter.writeFunction(self.currentFunction(),self.symbolTable.varCount(Symbol.KIND.VAR))
        if (keyword == Tokenizer.KEYWORD.METHOD):
            self.vmWriter.writePush(VMWriter.SEGMENT.ARG, 0)
            self.vmWriter.writePop(VMWriter.SEGMENT.POINTER,0)

        elif (keyword == Tokenizer.KEYWORD.CONSTRUCTOR):
            self.vmWriter.writePush(VMWriter.SEGMENT.CONST,self.symbolTable.varCount(Symbol.KIND.FIELD))
            self.vmWriter.writeCall("Memory.alloc", 1)
            self.vmWriter.writePop(VMWriter.SEGMENT.POINTER,0)




    def compileStatement(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '}'):
            self.tokenizer.pointerBack()
            return


        if (self.tokenizer.tokenType() != Tokenizer.TYPE.KEYWORD):
            error("keyword")
        else:
            if self.tokenizer.keyWord() == Tokenizer.KEYWORD.LET:
                self.compileLet()
            elif self.tokenizer.keyWord() == Tokenizer.KEYWORD.IF:
                self.compileIf()
            elif self.tokenizer.keyWord() == Tokenizer.KEYWORD.WHILE:
                self.compilesWhile()
            elif self.tokenizer.keyWord() == Tokenizer.KEYWORD.DO:
                self.compileDo()
            elif self.tokenizer.keyWord() == Tokenizer.KEYWORD.RETURN:
                self.compileReturn()
            else:
                self.error("'let'|'if'|'while'|'do'|'return'")
            '''
            switch (tokenizer.keyWord()){
                case LET:compileLet();break;
                case IF:compileIf();break;
                case WHILE:compilesWhile();break;
                case DO:compileDo();break;
                case RETURN:compileReturn();break;
                default:error("'let'|'if'|'while'|'do'|'return'");
            }
            '''
        
        self.compileStatement()
    

    def compileParameterList(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == ')'):
            self.tokenizer.pointerBack()
            return

        typeT = ""

        self.tokenizer.pointerBack()
        while True:
            typeT = self.compileType()
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != Tokenizer.TYPE.IDENTIFIER):
                error("identifier")

            self.symbolTable.define(self.tokenizer.identifier(),typeT, Symbol.KIND.ARG)

            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != Tokenizer.TYPE.SYMBOL or (self.tokenizer.symbol() != ',' and self.tokenizer.symbol() != ')')):
                self.error("',' or ')'")

            if (self.tokenizer.symbol() == ')'):
                self.tokenizer.pointerBack()
                break
            
    def compileVarDec(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != Tokenizer.TYPE.KEYWORD or self.tokenizer.keyWord() != Tokenizer.KEYWORD.VAR):
            self.tokenizer.pointerBack()
            return

        
        typeT = self.compileType()
        varNamesDone = False

        while True:
            self.tokenizer.advance()

            if (self.tokenizer.tokenType() != Tokenizer.TYPE.IDENTIFIER):
                error("identifier")
            
            self.symbolTable.define(self.tokenizer.identifier(),typeT, Symbol.KIND.VAR)
            self.tokenizer.advance()

            if (self.tokenizer.tokenType() != Tokenizer.TYPE.SYMBOL or (self.tokenizer.symbol() != ',' and self.tokenizer.symbol() != ';')):
                error("',' or ';'")

            if (self.tokenizer.symbol() == ';'):
                break

        self.compileVarDec()


    def compileDo(self):
        self.compileSubroutineCall()
        self.requireSymbol(';')
        self.vmWriter.writePop(VMWriter.SEGMENT.TEMP,0)

    def compileLet(self):

        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != Tokenizer.TYPE.IDENTIFIER):
            error("varName")

        varName = self.tokenizer.identifier()
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != Tokenizer.TYPE.SYMBOL or (self.tokenizer.symbol() != '[' and self.tokenizer.symbol() != '=')):
            error("'['|'='")
        

        expExist = False

        if (self.tokenizer.symbol() == '['):
            expExist = True
            self.vmWriter.writePush(getSeg(self.symbolTable.kindOf(varName)),self.symbolTable.indexOf(varName))
            compileExpression()

            requireSymbol(']')
            
            self.vmWriter.writeArithmetic(self.VMWriter.COMMAND.ADD)

        if (expExist): 
            self.tokenizer.advance()

        
        self.compileExpression()

        self.requireSymbol(';')

        if (expExist):
            self.vmWriter.writePop(self.VMWriter.SEGMENT.TEMP,0)
            self.vmWriter.writePop(self.VMWriter.SEGMENT.POINTER,1)
            self.vmWriter.writePush(self.VMWriter.SEGMENT.TEMP,0)
            self.vmWriter.writePop(self.VMWriter.SEGMENT.THAT,0)
        else:
            self.vmWriter.writePop(self.getSeg(self.symbolTable.kindOf(varName)), self.symbolTable.indexOf(varName))
    

    
    def getSeg(self, kind):

        if kind == Symbol.KIND.FIELD: 
            return VMWriter.SEGMENT.STATIC
        elif kind == Symbol.KIND.STATIC: 
            return VMWriter.SEGMENT.STATIC
        elif kind == Symbol.KIND.VAR: 
            return VMWriter.SEGMENT.LOCAL
        elif kind == Symbol.KIND.ARG: 
            return VMWriter.SEGMENT.ARG
        else:
            return VMWriter.SEGMENT.NONE
        '''
        switch (kind){
            case FIELD:
            case STATIC:return VMWriter.SEGMENT.STATIC;
            case VAR:return VMWriter.SEGMENT.LOCAL;
            case ARG:return VMWriter.SEGMENT.ARG;
            default:return VMWriter.SEGMENT.NONE;
        }
        '''

    def compilesWhile(self):

        continueLabel = self.newLabel()
        topLabel = self.newLabel()
        self.vmWriter.writeLabel(topLabel)

        self.requireSymbol('(')
        self.compileExpression()
        self.requireSymbol(')')
        self.vmWriter.writeArithmetic(VMWriter.COMMAND.NOT)
        self.vmWriter.writeIf(continueLabel)
        self.requireSymbol('{')
        self.compileStatement()
        self.requireSymbol('}')
        self.vmWriter.writeGoto(topLabel)
        self.vmWriter.writeLabel(continueLabel)

    def newLabel(self):
        self.labelIndex += 1
        return "LABEL_" + str(self.labelIndex)


    def compileReturn(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == ';'):
            self.vmWriter.writePush(VMWriter.SEGMENT.CONST,0)
        else:
            self.tokenizer.pointerBack()
            self.compileExpression()
            self.requireSymbol(';')

        self.vmWriter.writeReturn()


    def compileIf(self):

        elseLabel = self.newLabel()
        endLabel = self.newLabel()

        self.requireSymbol('(')
        self.compileExpression()
        self.requireSymbol(')')
        self.vmWriter.writeArithmetic(VMWriter.COMMAND.NOT)
        self.vmWriter.writeIf(elseLabel)
        self.requireSymbol('{')
        self.compileStatement()
        self.requireSymbol('}')
        self.vmWriter.writeGoto(endLabel)
        self.vmWriter.writeLabel(elseLabel)
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == Tokenizer.TYPE.KEYWORD and self.tokenizer.keyWord() == Tokenizer.KEYWORD.ELSE):
            self.requireSymbol('{')
            self.compileStatement()
            self.requireSymbol('}')
        else:
            self.tokenizer.pointerBack()

        self.vmWriter.writeLabel(endLabel)


    def compileTerm(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == Tokenizer.TYPE.IDENTIFIER):
            tempId = self.tokenizer.identifier()

            self.tokenizer.advance()
            if (self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '['):
                self.vmWriter.writePush(getSeg(self.symbolTable.kindOf(tempId)),self.symbolTable.indexOf(tempId))
                self.compileExpression()
                self.requireSymbol(']')
                self.vmWriter.writeArithmetic(VMWriter.COMMAND.ADD)
                self.vmWriter.writePop(VMWriter.SEGMENT.POINTER,1)
                self.vmWriter.writePush(VMWriter.SEGMENT.THAT,0)

            elif(self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and 
            (self.tokenizer.symbol() == '(' or 
            self.tokenizer.symbol() == '.')):
                self.tokenizer.pointerBack();self.tokenizer.pointerBack()
                self.compileSubroutineCall()
            else:
                self.tokenizer.pointerBack()
                self.vmWriter.writePush(self.getSeg(self.symbolTable.kindOf(tempId)), self.symbolTable.indexOf(tempId))

        else:
            
            if (self.tokenizer.tokenType() == Tokenizer.TYPE.INT_CONST):
                self.vmWriter.writePush(VMWriter.SEGMENT.CONST,self.tokenizer.intVal())
            elif(self.tokenizer.tokenType() == Tokenizer.TYPE.STRING_CONST):
                string = self.tokenizer.stringVal()
                self.vmWriter.writePush(VMWriter.SEGMENT.CONST,string.length())
                self.vmWriter.writeCall("String.new",1)
                for i in range(len(string)):
                    self.vmWriter.writePush(VMWriter.SEGMENT.CONST,int(str.charAt(i)))
                    self.vmWriter.writeCall("String.appendChar",2)

            elif(self.tokenizer.tokenType() == Tokenizer.TYPE.KEYWORD and self.tokenizer.keyWord() == Tokenizer.KEYWORD.TRUE):
                self.vmWriter.writePush(VMWriter.SEGMENT.CONST,0)
                self.vmWriter.writeArithmetic(VMWriter.COMMAND.NOT)
            elif(self.tokenizer.tokenType() == Tokenizer.TYPE.KEYWORD and self.tokenizer.keyWord() == Tokenizer.KEYWORD.THIS):
                self.vmWriter.writePush(VMWriter.SEGMENT.POINTER,0)

            elif(self.tokenizer.tokenType() == Tokenizer.TYPE.KEYWORD and 
            (self.tokenizer.keyWord() == Tokenizer.KEYWORD.FALSE or 
            self.tokenizer.keyWord() == Tokenizer.KEYWORD.NULL)):
                self.vmWriter.writePush(VMWriter.SEGMENT.CONST,0)
            elif(self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '('):
                self.compileExpression()
                self.requireSymbol(')')
            elif(self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL 
            and (self.tokenizer.symbol() == '-' or self.tokenizer.symbol() == '~')):
                s = self.tokenizer.symbol()
                self.compileTerm()
                if (s == '-'):
                    self.vmWriter.writeArithmetic(VMWriter.COMMAND.NEG)
                else:
                    self.vmWriter.writeArithmetic(VMWriter.COMMAND.NOT)
                
            else:
                error("integerConstant|stringConstant|keywordConstant|'(' expression ')'|unaryOp term")
        

    def compileSubroutineCall(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != Tokenizer.TYPE.IDENTIFIER):
            error("identifier")

        name = self.tokenizer.identifier()
        nArgs = 0

        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '('):
            self.vmWriter.writePush(VMWriter.SEGMENT.POINTER,0)
            nArgs = self.compileExpressionList() + 1
            self.requireSymbol(')')
            self.vmWriter.writeCall(self.currentClass + '.' + name, nArgs)

        elif(self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '.'):
            objName = name
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != Tokenizer.TYPE.IDENTIFIER):
                error("identifier")

            name = self.tokenizer.identifier()
            typeT = self.symbolTable.typeOf(objName)

            if (typeT=="int" or typeT=="boolean" or typeT=="char" or typeT=="void"):
                error("no built-in typeT")
            elif (typeT==""):
                name = objName + "." + name
            else:
                nArgs = 1
                self.vmWriter.writePush(self.getSeg(self.symbolTable.kindOf(objName)), self.symbolTable.indexOf(objName))
                name = self.symbolTable.typeOf(objName) + "." + name

            self.requireSymbol('(')
            nArgs += self.compileExpressionList()
            self.requireSymbol(')')
            self.vmWriter.writeCall(name,nArgs)
        else:
            error("'('|'.'")

    
    def compileExpression(self):
        self.compileTerm()
        while True:
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.isOp()):
                opCmd = ""

                if self.tokenizer.symbol() == '+':
                    opCmd = "add"
                elif self.tokenizer.symbol() == '-':
                    opCmd = "sub"
                elif self.tokenizer.symbol() == '*':
                    opCmd = "call Math.multiply 2"
                elif self.tokenizer.symbol() == '/':
                    opCmd = "call Math.divide 2"
                elif self.tokenizer.symbol() == '<':
                    opCmd = "lt"
                elif self.tokenizer.symbol() == '>':
                    opCmd = "gt"
                elif self.tokenizer.symbol() == '=':
                    opCmd = "eq"
                elif self.tokenizer.symbol() == '&':
                    opCmd = "and"
                elif self.tokenizer.symbol() == '|':
                    opCmd = "or"
                else: 
                    error("Unknown op!")
                '''
                switch (tokenizer.symbol()){
                    case '+':opCmd = "add";break;
                    case '-':opCmd = "sub";break;
                    case '*':opCmd = "call Math.multiply 2";break;
                    case '/':opCmd = "call Math.divide 2";break;
                    case '<':opCmd = "lt";break;
                    case '>':opCmd = "gt";break;
                    case '=':opCmd = "eq";break;
                    case '&':opCmd = "and";break;
                    case '|':opCmd = "or";break;
                    default:error("Unknown op!");
                }
                '''
                self.compileTerm()
                self.vmWriter.writeCommand(opCmd,"","")

            else:
                self.tokenizer.pointerBack()
                break
            
    def compileExpressionList(self):
        nArgs = 0

        self.tokenizer.advance()
        
        if (self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == ')'):
            self.tokenizer.pointerBack()
        else:
            nArgs = 1
            self.tokenizer.pointerBack()            
            self.compileExpression()
            while True:
                self.tokenizer.advance()
                if (self.tokenizer.tokenType() == Tokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == ','):
                    self.compileExpression()
                    nArgs += 1
                else:
                    self.tokenizer.pointerBack()
                    break

        return nArgs

    def error(self, val):
        print("Expected token missing : " + str(val) + " Current token:" + self.tokenizer.getCurrentToken())
    
    def requireSymbol(self, symbol):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != Tokenizer.TYPE.SYMBOL or self.tokenizer.symbol() != symbol):
            self.error("'" + symbol + "'")
    
