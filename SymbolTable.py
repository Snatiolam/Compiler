from Symbol import *

class SymbolTable:
     
    def __init__(self):
        
        self.classSymbols = {}
        self.subroutineSymbols = {}

        self.indices = {}
        self.indices[Symbol.KIND.ARG] = 0
        self.indices[Symbol.KIND.FIELD] = 0
        self.indices[Symbol.KIND.STATIC] = 0
        self.indices[Symbol.KIND.VAR] = 0


    def startSubroutine(self):
        self.subroutineSymbols.clear()
        self.indices[Symbol.KIND.VAR] = 0
        self.indices[Symbol.KIND.ARG] = 0

    def define(self, name, typeT, kind):
        if (kind == Symbol.KIND.ARG) or (Kind == Symbol.KIND.VAR):

            index = indices[kind]
            symbol = Symbol(typeT, kind, index) 
            indices[kind]= index+1
            subroutineSymbols[name] = symbol
        elif (kind == Symbol.KIND.STATIC) or (kind == Symbol.KIND.FIELD):
            index = indices[kind]
            symbol = Symbol(typeT, kind, index)
            indices[kind] = index + 1
            classSymbols[name] = symbol



    def varCount(self, kind):
        return indices[kind]

    def kindOf(self, name):
        symbol = lookUp(name)
        if symbol != None:
            return symbol.getKind()

        return Symbol.KIND.NONE


    def typeOf(self, name):
        symbol = lookUp(name)
        if symbol != None:
            return symbol.getType()

        return ""


    def indexOf(self, name):
        symbol = lookUp(name)
        if symbol != None:
            return symbol.getIndex()

        return -1

    def lookUp(self, name):
        if classSymbols[name] != None:
            return classSymbols[name]
        elif subroutineSymbols[name] != None:
            return subroutineSymbols[name]
        else:
            return None

