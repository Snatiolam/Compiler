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
        CONTRUCTOR = 4
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
        try:
            scanner = open(inFile, "r")
            preprocessed = ""
            line = ""
            init_keywordmap()

            for lineN in scanner.readlines():
                line = noComments(lineN).strip()

                if len(line) > 0:
                    preprocessd += line + "\n"

            preprocessed = noBlockComments(preprocessed).strip()

            initRegs()
            m = tokenPatterns.search(preprocessed);
            token = []
            pointer = 0
            while m.find():
                tokens.append(m.group());

        except:
            traceback.print_exc()

        currentToken = ""
        currentTokenType = TYPE.NONE

    def init_keywordmap(self):
        KeyWordMap["class"] = KEYWORD.CLASS
        KeyWordMap["method"] = KEYWORD.METHOD
        KeyWordMap["declare"] = KEYWORD.VAR
        KeyWordMap["boolean"] = KEYWORD.BOOLEAN
        KeyWordMap["false"] = KEYWORD.FALSE
        KeyWordMap["let"] = KEYWORD.LET
        KeyWordMap["else"] = KEYWORD.ELSE
        KeyWordMap["constructor"] = KEYWORD.CONSTRUCTOR
        KeyWordMap["field"] = KEYWORD.FIELD
        KeyWordMap["int"] = KEYWORD.INT
        KeyWordMap["void"] = KEYWORD.VOID
        KeyWordMap["null"] = KEYWORD.NULL
        KeyWordMap["do"] = KEYWORD.DO
        KeyWordMap["while"] = KEYWORD.WHILE
        KeyWordMap["fun"] = KEYWORD.FUNCTION
        KeyWordMap["static"] = KEYWORD.STATIC
        KeyWordMap["char"] = KEYWORD.CHAR
        KeyWordMap["true"] = KEYWORD.TRUE
        KeyWordMap["this"] = KEYWORD.THIS
        KeyWordMap["if"] = KEYWORD.IF
        KeyWordMap["return"] = KEYWORD.RETURN

        opSet.append('+')
        opSet.append('-')
        opSet.append('*')
        opSet.append('/')
        opSet.append('&')
        opSet.append('|')
        opSet.append('<')
        opSet.append('>')
        opSet.append('=')

    def initReg(self):
        
        KeyWordReg = ""
        for seg in KeWordMap.keys():
            keyWordReg += seg + "|"

        symbolReg = "[\\&\\*\\+\\(\\)\\.\\/\\,\\-\\]\\;\\~\\}\\|\\{\\>\\=\\[\\<]";
        intReg = "[0-9]+";
        strReg = "\"[^\"\n]*\"";
        idReg = "[a-zA-Z_]\\w*";
        tokenPatterns = re.compile(idReg + "|" + keyWordReg + symbolReg + "|" + intReg + "|" + strReg);


    def hasMoreToken(self):
        return pointer < len(tokens)

    def advance(self):
        if (hasMoreToken()):
            currentToken = token[pointer]
            pointer += 1
        else:
            raise Exception("No more tokens")

        if re.match(keyWordReg, currentToken):
            currentTokenType = TYPE.KEYWORD
        elif re.match(symbolReg, currentToken):
            currentTokenType = TYPE.SYMBOL
        elif re.match(intReg, currentToken):
            currentTokenType = TYPE.INT_CONST
        elif re.match(strReg, currentToken):
            currentTokenType = TYPE.STRING_CONST
        elif re.match(idReg, currentToken):
            currentTokenType = TYPE.IDENTIFIER
        else:
            raise Exception("Unknow token:" + currentToken)

        def getCurrentToken(self):
            return currentToken

        def tokenType(self):
            return currentTokenType

        def keyWord(self):
            if currentTokenType == TYPE.KEYWORD:
                return keyWordMap[currentToken]
            else:
                raise Exception("Current token is not a keyword")

        def symbol(self):
            if currentTokenType == TYPE.SYMBOL:
                return currentToken[0]
            else:
                raise Exception("Current token is not  a symbol")

        def identifier(self):
            if currentTokenType == TYPE.IDENTIFIER:
                return currentToken
            else:
                raise Exception("Current token is not a identifier")

        def intVal(self):
            if currentTokenType == TYPE.INT_CONST:
                return int(currentToken)
            else:
                raise Exception("Current token is not an integer constant")

        def stringVal(self):
            if currentTokenType == TYPE.STRING_CONST:
                return currentToken[1: len(currentToken) - 1]
            else:
                raise Exception("Current token is not a string constant")

        def pointerBack(self):
            if pointer > 0:
                pointer -= 1
                currentToken = tokens[pointer]

        def isOp(self):
            return symbol() in opSet

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

