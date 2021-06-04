
class CompilationEngine:
    
    
    def __init__(self,inFile, outFile):
        self.currentClass = ""
        self.currentSubroutine = ""
        self.tokenizer = JackTokenizer(inFile)
        self.vmWriter = VMWriter(outFile)
        self.symbolTable = SymbolTable()
        self.labelIndex = 0


    def currentFunction(self):
        if len(self.currentClass) != 0 and len(self.currentSubroutine) != 0:
            return str(self.currentClass) + "." + str(self.currentSubroutine)

        return ""
    
    def compileType(self):
        self.tokenizer.advance()

        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.KEYWORD 
        and (self.tokenizer.keyWord() == JackTokenizer.KEYWORD.INT 
        or self.tokenizer.keyWord() == JackTokenizer.KEYWORD.CHAR 
        or self.tokenizer.keyWord() == JackTokenizer.KEYWORD.BOOLEAN)):
            return self.tokenizer.getCurrentToken()

        if self.tokenizer.tokenType() == JackTokenizer.TYPE.IDENTIFIER:
            return self.tokenizer.identifier()

        error("in|char|boolean|className")


        return ""

    def compileClass(self):
        self.tokenizer.advance()

        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.KEYWORD or self.tokenizer.keyWord() != JackTokenizer.KEYWORD.CLASS):
            print(self.tokenizer.getCurrentToken())
            error("class")
        
        self.tokenizer.advance()

        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.IDENTIFIER):
            error("className")
        

        
        currentClass = self.tokenizer.identifier()
        requireSymbol('{')
        compileClassVarDec()
        compileSubroutine()
        requireSymbol('}')

        if (tokenizer.hasMoreTokens()):
            error("Unexpected tokens")
        
        self.vmWriter.close()


    def compileClassVarDec(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '}'):
            self.tokenizer.pointerBack()
            return 
        
        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.KEYWORD):
            error("Keywords")
        
        if (self.tokenizer.keyWord() == JackTokenizer.KEYWORD.CONSTRUCTOR or self.tokenizer.keyWord() == JackTokenizer.KEYWORD.FUNCTION or tokenizer.keyWord() == JackTokenizer.KEYWORD.METHOD):
            self.tokenizer.pointerBack()
            return 

        if (self.tokenizer.keyWord() != JackTokenizer.KEYWORD.STATIC and self.tokenizer.keyWord() != JackTokenizer.KEYWORD.FIELD):
            error("static or field")
        
        kind = None
        type = ""
        name = ""

        dict = {
            "STATIC:kind" : Symbol.KIND.STATIC,
            "FIELD:kind" :  Symbol.KIND.FIELD
        }

        dict[tokenizer.keyWord()]
        '''
        switch (tokenizer.keyWord()){
            case STATIC:kind = Symbol.KIND.STATIC;break;
            case FIELD:kind = Symbol.KIND.FIELD;break;
        }
        '''
        type = compileType()
        varNamesDone = False
        while True:
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != JackTokenizer.TYPE.IDENTIFIER):
                error("identifier")
            
            name = self.tokenizer.identifier()

            self.symbolTable.define(name,type,kind)

            self.tokenizer.advance()

            if (self.tokenizer.tokenType() != JackTokenizer.TYPE.SYMBOL or (self.tokenizer.symbol() != ',' and self.tokenizer.symbol() != ';')):
                error("',' or ';'")

            if (self.tokenizer.symbol() == ';'):
                break

        compileClassVarDec()
    

    def compileSubroutine(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '}'):
            self.tokenizer.pointerBack()
            return

        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.KEYWORD or (self.tokenizer.keyWord() != JackTokenizer.KEYWORD.CONSTRUCTOR 
        and self.tokenizer.keyWord() != JackTokenizer.KEYWORD.FUNCTION 
        and self.tokenizer.keyWord() != JackTokenizer.KEYWORD.METHOD)):
            error("constructor|fun|method")

        keyword = self.tokenizer.keyWord()

        self.symbolTable.startSubroutine()

        if (self.tokenizer.keyWord() == JackTokenizer.KEYWORD.METHOD):
            self.symbolTable.define("this",self.currentClass, Symbol.KIND.ARG)

        type = ""

        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.KEYWORD and self.tokenizer.keyWord() == JackTokenizer.KEYWORD.VOID):
            type = "void"
        else:
            self.tokenizer.pointerBack()
            type = compileType()
        
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.IDENTIFIER):
            error("subroutineName")

        currentSubroutine = self.tokenizer.identifier()

        
        requireSymbol('(')

        
        compileParameterList()

        
        requireSymbol(')')

        compileSubroutineBody(keyword)

        compileSubroutine()

    
    def compileSubroutineBody(self, keyword):
        
        requireSymbol('{')
        compileVarDec()
        wrtieFunctionDec(keyword)

        compileStatement()
        requireSymbol('}')


    def wrtieFunctionDec(self, keyword):

        self.vmWriter.writeFunction(currentFunction(),self.symbolTable.varCount(Symbol.KIND.VAR))
        if (keyword == JackTokenizer.KEYWORD.METHOD):
            self.vmWriter.writePush(VMWriter.SEGMENT.ARG, 0)
            self.vmWriter.writePop(VMWriter.SEGMENT.POINTER,0)

        elif (keyword == JackTokenizer.KEYWORD.CONSTRUCTOR):
            self.vmWriter.writePush(VMWriter.SEGMENT.CONST,self.symbolTable.varCount(Symbol.KIND.FIELD))
            self.vmWriter.writeCall("Memory.alloc", 1)
            self.vmWriter.writePop(VMWriter.SEGMENT.POINTER,0)




    def compileStatement(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '}'):
            self.tokenizer.pointerBack()
            return


        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.KEYWORD):
            error("keyword")
        else:
            if self.tokenizer.keyWord() == LET:
                compileLet()
            elif self.tokenizer.keyWord() == IF:
                compileIf()
            elif self.tokenizer.keyWord() == WHILE:
                compilesWhile()
            elif self.tokenizer.keyWord() == DO:
                compileDo()
            elif self.tokenizer.keyWord() == RETURN:
                compileReturn()
            else:
                error("'let'|'if'|'while'|'do'|'return'")
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
        
        compileStatement()
    

    def compileParameterList(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and tokenizer.symbol() == ')'):
            self.tokenizer.pointerBack()
            return

        type = ""

        self.tokenizer.pointerBack()
        while True:
            type = compileType()
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != JackTokenizer.TYPE.IDENTIFIER):
                error("identifier")

            self.symbolTable.define(self.tokenizer.identifier(),type, Symbol.KIND.ARG)

            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != JackTokenizer.TYPE.SYMBOL or (self.tokenizer.symbol() != ',' and tokenizer.symbol() != ')')):
                error("',' or ')'")

            if (self.tokenizer.symbol() == ')'):
                self.tokenizer.pointerBack()
                break
            
    def compileVarDec(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.KEYWORD or self.tokenizer.keyWord() != JackTokenizer.KEYWORD.VAR):
            self.tokenizer.pointerBack()
            return

        
        type = compileType()
        varNamesDone = False

        while True:
            self.tokenizer.advance()

            if (self.tokenizer.tokenType() != JackTokenizer.TYPE.IDENTIFIER):
                error("identifier")
            
            self.symbolTable.define(self.tokenizer.identifier(),type, Symbol.KIND.VAR)
            self.tokenizer.advance()

            if (self.tokenizer.tokenType() != JackTokenizer.TYPE.SYMBOL or (self.tokenizer.symbol() != ',' and self.tokenizer.symbol() != ';')):
                error("',' or ';'")

            if (self.tokenizer.symbol() == ';'):
                break

        compileVarDec()


    def compileDo(self):
        compileSubroutineCall()
        requireSymbol(';')
        self.vmWriter.writePop(self.VMWriter.SEGMENT.TEMP,0)

    def compileLet(self):

        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.IDENTIFIER):
            error("varName")

        varName = self.tokenizer.identifier()
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.SYMBOL or (self.tokenizer.symbol() != '[' and self.tokenizer.symbol() != '=')):
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

        
        compileExpression()

        requireSymbol(';')

        if (expExist):
            self.vmWriter.writePop(self.VMWriter.SEGMENT.TEMP,0)
            self.vmWriter.writePop(self.VMWriter.SEGMENT.POINTER,1)
            self.vmWriter.writePush(self.VMWriter.SEGMENT.TEMP,0)
            self.vmWriter.writePop(self.VMWriter.SEGMENT.THAT,0)
        else:
            self.vmWriter.writePop(getSeg(self.symbolTable.kindOf(varName)), self.symbolTable.indexOf(varName))
    

    
    def getSeg(self, kind):

        if kind == FIELD: 
            return self.VMWriter.SEGMENT.THIS
        elif kind == STATIC: 
            return self.VMWriter.SEGMENT.STATIC
        elif kind == VAR: 
            return self.VMWriter.SEGMENT.LOCAL
        elif kind == ARG: 
            return self.VMWriter.SEGMENT.ARG
        else:
            return self.VMWriter.SEGMENT.NONE
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

        continueLabel = newLabel()
        topLabel = newLabel()
        self.vmWriter.writeLabel(topLabel)

        requireSymbol('(')
        compileExpression()
        requireSymbol(')')
        self.vmWriter.writeArithmetic(self.VMWriter.COMMAND.NOT)
        self.vmWriter.writeIf(continueLabel)
        requireSymbol('{')
        compileStatement()
        requireSymbol('}')
        self.vmWriter.writeGoto(topLabel)
        self.vmWriter.writeLabel(continueLabel)

    def newLabel(self):
        self.labelIndex += 1
        return "LABEL_" + str(self.labelIndex)


    def compileReturn(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == ';'):
            self.vmWriter.writePush(self.VMWriter.SEGMENT.CONST,0)
        else:
            self.tokenizer.pointerBack()
            compileExpression()
            requireSymbol(';')

        self.vmWriter.writeReturn()


    def compileIf(self):

        elseLabel = newLabel()
        endLabel = newLabel()

        requireSymbol('(')
        compileExpression()
        requireSymbol(')')
        self.vmWriter.writeArithmetic(self.VMWriter.COMMAND.NOT)
        self.vmWriter.writeIf(elseLabel)
        requireSymbol('{')
        compileStatement()
        requireSymbol('}')
        self.vmWriter.writeGoto(endLabel)
        self.vmWriter.writeLabel(elseLabel)
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.KEYWORD and self.tokenizer.keyWord() == JackTokenizer.KEYWORD.ELSE):
            requireSymbol('{')
            compileStatement()
            requireSymbol('}')
        else:
            self.tokenizer.pointerBack()

        self.vmWriter.writeLabel(endLabel)


    def compileTerm(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.IDENTIFIER):
            tempId = self.tokenizer.identifier()

            self.tokenizer.advance()
            if (self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '['):
                self.vmWriter.writePush(getSeg(self.symbolTable.kindOf(tempId)),self.symbolTable.indexOf(tempId))
                compileExpression()
                requireSymbol(']')
                self.vmWriter.writeArithmetic(VMWriter.COMMAND.ADD)
                self.vmWriter.writePop(VMWriter.SEGMENT.POINTER,1)
                self.vmWriter.writePush(VMWriter.SEGMENT.THAT,0)

            elif(self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and 
            (self.tokenizer.symbol() == '(' or 
            self.tokenizer.symbol() == '.')):
                self.tokenizer.pointerBack();self.tokenizer.pointerBack()
                compileSubroutineCall()
            else:
                self.tokenizer.pointerBack()
                self.vmWriter.writePush(getSeg(self.symbolTable.kindOf(tempId)), self.symbolTable.indexOf(tempId))

        else:
            
            if (self.tokenizer.tokenType() == JackTokenizer.TYPE.INT_CONST):
                self.vmWriter.writePush(VMWriter.SEGMENT.CONST,self.tokenizer.intVal())
            elif(self.tokenizer.tokenType() == JackTokenizer.TYPE.STRING_CONST):
                string = self.tokenizer.stringVal()
                self.vmWriter.writePush(VMWriter.SEGMENT.CONST,string.length())
                self.vmWriter.writeCall("String.new",1)
                for i in range(len(string)):
                    self.vmWriter.writePush(VMWriter.SEGMENT.CONST,int(str.charAt(i)))
                    self.vmWriter.writeCall("String.appendChar",2)

            elif(self.tokenizer.tokenType() == JackTokenizer.TYPE.KEYWORD and self.tokenizer.keyWord() == JackTokenizer.KEYWORD.TRUE):
                self.vmWriter.writePush(VMWriter.SEGMENT.CONST,0)
                self.vmWriter.writeArithmetic(VMWriter.COMMAND.NOT)
            elif(self.tokenizer.tokenType() == JackTokenizer.TYPE.KEYWORD and self.tokenizer.keyWord() == JackTokenizer.KEYWORD.THIS):
                self.vmWriter.writePush(VMWriter.SEGMENT.POINTER,0)

            elif(self.tokenizer.tokenType() == JackTokenizer.TYPE.KEYWORD and 
            (self.tokenizer.keyWord() == JackTokenizer.KEYWORD.FALSE or 
            self.tokenizer.keyWord() == JackTokenizer.KEYWORD.NULL)):
                self.vmWriter.writePush(VMWriter.SEGMENT.CONST,0)
            elif(self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '('):
                compileExpression()
                requireSymbol(')')
            elif(self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL 
            and (self.tokenizer.symbol() == '-' or self.tokenizer.symbol() == '~')):
                s = self.tokenizer.symbol()
                compileTerm()
                if (s == '-'):
                    self.vmWriter.writeArithmetic(self.VMWriter.COMMAND.NEG)
                else:
                    self.vmWriter.writeArithmetic(self.VMWriter.COMMAND.NOT)
                
            else:
                error("integerConstant|stringConstant|keywordConstant|'(' expression ')'|unaryOp term")
        

    def compileSubroutineCall(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.IDENTIFIER):
            error("identifier")

        name = tokenizer.identifier()
        nArgs = 0

        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '('):
            self.vmWriter.writePush(self.VMWriter.SEGMENT.POINTER,0)
            nArgs = compileExpressionList() + 1
            requireSymbol(')')
            self.vmWriter.writeCall(self.currentClass + '.' + name, nArgs)

        elif(self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == '.'):
            objName = name
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != JackTokenizer.TYPE.IDENTIFIER):
                error("identifier")

            name = tokenizer.identifier()
            type = self.symbolTable.typeOf(objName)

            if (type.equals("int") or type.equals("boolean") or type.equals("char") or type.equals("void")):
                error("no built-in type")
            elif (type.equals("")):
                name = objName + "." + name
            else:
                nArgs = 1
                self.vmWriter.writePush(getSeg(self.symbolTable.kindOf(objName)), self.symbolTable.indexOf(objName))
                name = self.symbolTable.typeOf(objName) + "." + name

            requireSymbol('(')
            nArgs += compileExpressionList()
            requireSymbol(')')
            self.vmWriter.writeCall(name,nArgs)
        else:
            error("'('|'.'")

    
    def compileExpression(self):
        compileTerm()
        while True:
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.isOp()):
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
                compileTerm()
                self.vmWriter.writeCommand(opCmd,"","")

            else:
                self.tokenizer.pointerBack()
                break
            
    def compileExpressionList(self):
        nArgs = 0

        self.tokenizer.advance()
        
        if (self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == ')'):
            self.tokenizer.pointerBack()
        else:
            nArgs = 1
            self.tokenizer.pointerBack()            
            compileExpression()
            while True:
                tokenizer.advance()
                if (self.tokenizer.tokenType() == JackTokenizer.TYPE.SYMBOL and self.tokenizer.symbol() == ','):
                    compileExpression()
                    nArgs += 1
                else:
                    self.tokenizer.pointerBack()
                    break

        return nArgs

    def error(self, val):
        print("Expected token missing : " + str(val) + " Current token:" + self.tokenizer.getCurrentToken())
    
    def requireSymbol(self, symbol):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.TYPE.SYMBOL or self.tokenizer.symbol() != symbol):
            error("'" + symbol + "'")
    