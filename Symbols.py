import enum

class Symbol:

    class KIND(enum.Enum):
        STATIC = 1
        FIELD = 2
        ARG = 3
        VAR = 4
        NONE = 5

    def __init__(self, typeStr, kind, index):
        self.typeStr = typeStr
        self.kind = kind
        self.index = index

    def getType(self):
        return self.typeStr

    def getKind(self):
        return self.kind

    def getIndex(self):
        return self.index
