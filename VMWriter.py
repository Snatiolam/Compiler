import enum
from collections import defaultdict

class VMWriter:

    class SEGMENT(enum.Enum):
        CONST = 1
        ARG =  2
        LOCAL = 3
        STATIC = 4
        THIS = 5
        THAT = 6
        POINTER = 7
        TEMP = 8
        NONE = 9

    class COMMAND(enum.Enum):
        ADD = 1
        SUB = 2
        NEG = 3
        EQ = 4
        GT = 5
        LT =6
        AND =7
        OR =8
        NOT =9


    def init_segment(self):

        self.segmentStringHashMap['SEGMENT.CONST'] = "constant"
        self.segmentStringHashMap['SEGMENT.ARG']="argument"
        self.segmentStringHashMap['SEGMENT.LOCAL'] = "local"
        self.segmentStringHashMap['SEGMENT.STATIC'] = "static"
        self.segmentStringHashMap['SEGMENT.THIS'] = "this"
        self.segmentStringHashMap['SEGMENT.THAT'] = "that"
        self.segmentStringHashMap['SEGMENT.POINTER'] = "pointer"
        self.segmentStringHashMap['SEGMENT.TEMP'] = "temp"

        self.commandStringHashMap['COMMAND.ADD'] = "add"
        self.commandStringHashMap['COMMAND.SUB'] = "sub"
        self.commandStringHashMap['COMMAND.NEG'] = "neg"
        self.commandStringHashMap['COMMAND.EQ'] = "eq"
        self.commandStringHashMap['COMMAND.GT'] = "gt"
        self.commandStringHashMap['COMMAND.LT'] = "lt"
        self.commandStringHashMap['COMMAND.AND'] = "and"
        self.commandStringHashMap['COMMAND.OR'] = "or"
        self.commandStringHashMap['COMMAND.NOT'] = "not"

    def __init__(self, fOut):

        #segmentStringHashMap = {}
        self.segmentStringHashMap = defaultdict(lambda:None)
        #commandStringHashMap = {}
        self.commandStringHashMap = defaultdict(lambda:None)
        self.init_segment()
        try:
            # self.f = open(fOut, 'w')
            self.f = fOut # self.f = fOut -> Seria la otra opcion si esta linea saca error
        except:
            print("No se encontro el archivo o bien tienes un error en el VMWriter")
        


    def writePush(self,segment, index):
        self.writeCommand("push", self.segmentStringHashMap[segment],int(index))


    def writePop(self, segment, index):
        self.writeCommand("pop", self.segmentStringHashMap[segment],int(index))


    def writeArithmetic(self, command):
        self.writeCommand(self.commandStringHashMap[command],"","")

    def writeLabel(self, label):
        self.writeCommand("label",label,"")

    def writeGoto(self, label):
        self.writeCommand("goto",label,"")

    def writeIf(self, label):
        self.writeCommand("if-goto",label,"")
    
    def writeCall(self, name, nArgs):
        self.writeCommand("call",name,int(nArgs))
    

    def writeFunction(self, name, nlocals):
        self.writeCommand("function",name,int(nlocals))


    def writeReturn(self):
        self.writeCommand("return","","")

    def writeCommand(self, cmd, arg1, arg2):

        self.f.write(str(cmd) + " " + str(arg1) + " " + str(arg2) + "\n")

    def close(self):
        self.f.close()
    




