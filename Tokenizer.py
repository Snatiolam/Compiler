import enum
import re
import traceback

class Tokenizer:

    KeyWordMap = {}
    opSet = []

    class TYPE(enum.Enum):
        KEYWORD = 1
        SYMBOL = 2
        IDENTIFIER = 3
        INT_CONST = 4
        STRING_CONST = 5
        NONE = 6

    class KEYWORD(enum.Enum):
        CLASS = 1
        METHOD = 2
        FUNCTION = 3
        CONSTRUCTOR = 4
        INT = 5
        BOOLEAN = 6
        CHAR = 7
        VOID = 8
        VAR = 9
        STATIC = 10
        FIELD = 11
        LET = 12
        DO = 13
        IF = 14
        ELSE = 15
        WHILE = 16
        RETURN = 17
        TRUE = 18
        FALSE = 19
        NULL = 20
        THIS = 21

    def __init__(self, inFile):
        self.pointer = 0
        self.preprocessed = ""
        self.line = ""
        self.tokens = []
        self.init_keywordmap()
        self.keyWordReg = ""
        self.tokenPatterns = None
        try:
            scanner = open(inFile,'r')     
            for lineN in scanner.readlines():
                line = self.noComments(lineN)

                if len(line) > 0:
                    self.preprocessed += line + "\n"

            
            self.preprocessed = self.noBlockComments(self.preprocessed).strip()

            self.initRegs()
            #m = self.tokenPatterns.search(self.preprocessed)
            match = self.tokenPatterns.findall(self.preprocessed) # :)
            #input(self.preprocessed)

            for m in match:
                self.tokens.append(m)
                #print(m)

        except:
            traceback.print_exc()

        self.currentToken = ""
        self.currentTokenType = self.TYPE.NONE

    def init_keywordmap(self):
        self.KeyWordMap["class"] = self.KEYWORD.CLASS
        self.KeyWordMap["method"] = self.KEYWORD.METHOD
        self.KeyWordMap["declare"] = self.KEYWORD.VAR
        self.KeyWordMap["boolean"] = self.KEYWORD.BOOLEAN
        self.KeyWordMap["false"] = self.KEYWORD.FALSE
        self.KeyWordMap["let"] = self.KEYWORD.LET
        self.KeyWordMap["else"] = self.KEYWORD.ELSE
        self.KeyWordMap["constructor"] = self.KEYWORD.CONSTRUCTOR
        self.KeyWordMap["field"] = self.KEYWORD.FIELD
        self.KeyWordMap["int"] = self.KEYWORD.INT
        self.KeyWordMap["void"] = self.KEYWORD.VOID
        self.KeyWordMap["null"] = self.KEYWORD.NULL
        self.KeyWordMap["do"] = self.KEYWORD.DO
        self.KeyWordMap["while"] = self.KEYWORD.WHILE
        self.KeyWordMap["fun"] = self.KEYWORD.FUNCTION
        self.KeyWordMap["static"] = self.KEYWORD.STATIC
        self.KeyWordMap["char"] = self.KEYWORD.CHAR
        self.KeyWordMap["true"] = self.KEYWORD.TRUE
        self.KeyWordMap["this"] = self.KEYWORD.THIS
        self.KeyWordMap["if"] = self.KEYWORD.IF
        self.KeyWordMap["return"] = self.KEYWORD.RETURN

        self.opSet.append('+')
        self.opSet.append('-')
        self.opSet.append('*')
        self.opSet.append('/')
        self.opSet.append('&')
        self.opSet.append('|')
        self.opSet.append('<')
        self.opSet.append('>')
        self.opSet.append('=')

    def initRegs(self):
        
        self.KeyWordReg = ""
        for seg in self.KeyWordMap.keys():
            self.keyWordReg += seg + "|"

        symbolReg = "[\\&\\*\\+\\(\\)\\.\\/\\,\\-\\]\\;\\~\\}\\|\\{\\>\\=\\[\\<]"
        intReg = "[0-9]+"
        strReg = "\"[^\"\n]*\""
        idReg = "[a-zA-Z_]\\w*"
        self.tokenPatterns = re.compile(idReg + "|" + self.keyWordReg + symbolReg + "|" + intReg + "|" + strReg)

    def hasMoreToken(self):
        return self.pointer < len(self.tokens)

    def advance(self):
        if self.hasMoreToken():
            self.currentToken = self.tokens[self.pointer]
            self.pointer += 1
        else:
            raise Exception("No more tokens")

        if re.match(self.keyWordReg, self.currentToken):
            self.currentTokenType = self.TYPE.KEYWORD
        elif re.match("[\\&\\*\\+\\(\\)\\.\\/\\,\\-\\]\\;\\~\\}\\|\\{\\>\\=\\[\\<]", self.currentToken):
            self.currentTokenType = self.TYPE.SYMBOL
        elif re.match("[0-9]+", self.currentToken):
            self.currentTokenType = self.TYPE.INT_CONST
        elif re.match("\"[^\"\n]*\"", self.currentToken):
            self.currentTokenType = self.TYPE.STRING_CONST
        elif re.match("[a-zA-Z_]\\w*", self.currentToken):
            self.currentTokenType = self.TYPE.IDENTIFIER
        else:
            raise Exception("Unknow token:" + self.currentToken)

    def getCurrentToken(self):
        return self.currentToken

    def tokenType(self):
        return self.currentTokenType

    def keyWord(self):
        if self.currentTokenType == self.TYPE.KEYWORD:
            return self.KeyWordMap[self.currentToken]
        else:
            raise Exception("Current token is not a keyword")

    def symbol(self):
        if self.currentTokenType == self.TYPE.SYMBOL:
            return self.currentToken[0]
        else:
            raise Exception("Current token is not  a symbol")

    def identifier(self):
        print(self.currentTokenType)
        if self.currentTokenType == self.TYPE.IDENTIFIER:
            return self.currentToken
        else:
            raise Exception("Current token is not a identifier")

    def intVal(self):
        if self.currentTokenType == self.TYPE.INT_CONST:
            return int(self.currentToken)
        else:
            raise Exception("Current token is not an integer constant")

    def stringVal(self):
        if self.currentTokenType == self.TYPE.STRING_CONST:
            return self.currentToken[1: len(self.currentToken) - 1]
        else:
            raise Exception("Current token is not a string constant")

    def pointerBack(self):
        if self.pointer > 0:
            self.pointer -= 1
            self.currentToken = self.tokens[pointer]

    def isOp(self):
        return symbol() in self.opSet

    def noComments(self, strIn):
        position = strIn.find("//")
        if position != -1:
            strIn = strIn[0:position]

        return strIn

    def noSpaces(self, strIn):
        result = ""

        if len(strIn) != 0:
            segs = strIn.split(" ")

            for s in segs:
                result += s

        return result

    def noBlockComments(self, strIn):
        startIndex = strIn.find("/*")
        if startIndex == -1:
            return strIn
        result = strIn
        endIndex = strIn.find("*/")

        while startIndex != -1:
            if endIndex == -1:
                return strIn[0: startIndex - 1]
            result = result[0: startIndex] + result[endIndex + 2:]
            startIndex = result.find("/*")
            endIndex = result.find("*/")

        
        return result
    
    def error(self, val):
        print("Expected token missing : " + str(val) + " Current token:" )