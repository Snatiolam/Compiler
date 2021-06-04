import enum
import re

class Tokenizer:

    KeyWordMap = {}

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


        def initReg(self):
            
            KeyWordReg = ""
            for seg in KeWordMap.keys():
                keyWordReg += seg + "|"

            symbolReg = "[\\&\\*\\+\\(\\)\\.\\/\\,\\-\\]\\;\\~\\}\\|\\{\\>\\=\\[\\<]";
            intReg = "[0-9]+";
            strReg = "\"[^\"\n]*\"";
            idReg = "[a-zA-Z_]\\w*";
            tokenPatterns = Pattern.compile(idReg + "|" + keyWordReg + symbolReg + "|" + intReg + "|" + strReg);


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
