from Symbol import *
from collections import defaultdict

class SymbolTable:
     
    def __init__(self):
        
        #self.classSymbols = {}
        self.classSymbols = defaultdict(lambda:None)

        #self.subroutineSymbols = {}
        self.subroutineSymbols = defaultdict(lambda:None)
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
        if (kind == Symbol.KIND.ARG) or (kind == Symbol.KIND.VAR):

            index = self.indices[kind]
            symbol = Symbol(typeT, kind, index) 
            self.indices[kind]= index+1
            self.subroutineSymbols[name] = symbol

            #print("------------",name,"--------------", symbol.typeStr)
        elif (kind == Symbol.KIND.STATIC) or (kind == Symbol.KIND.FIELD):
            index = indices[kind]
            symbol = Symbol(typeT, kind, index)
            self.indices[kind] = index + 1
            self.classSymbols[name] = symbol
            #print("------------",name,"--------------", symbol.typeStr)

    def varCount(self, kind):
        return self.indices[kind]

    def kindOf(self, name):
        symbol = self.lookUp(name)
        if symbol != None:
            return symbol.getKind()

        return Symbol.KIND.NONE


    def typeOf(self, name):
        symbol = self.lookUp(name)
        if symbol != None:
            return symbol.getType()

        return ""


    def indexOf(self, name):
        symbol = self.lookUp(name)
        if symbol != None:
            return symbol.getIndex()

        return -1

    def lookUp(self, name):
        if self.classSymbols[name] != None:
            return self.classSymbols[name]
        elif self.subroutineSymbols[name] != None:
            return self.subroutineSymbols[name]
        else:
            return None