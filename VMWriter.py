class VMWriter:

    SEGMENT = ["CONST","ARG","LOCAL","STATIC","THIS","THAT","POINTER","TEMP","NONE"]
    COMMAND = ["ADD","SUB","NEG","EQ","GT","LT","AND","OR","NOT"]

    segmentStringHashMap = {}
    commandStringHashMap = {}

    segmentStringHashMap['SEGMENT.CONST'] = "constant"
    segmentStringHashMap['SEGMENT.ARG']="argument"
    segmentStringHashMap['SEGMENT.LOCAL'] = "local"
    segmentStringHashMap['SEGMENT.STATIC'] = "static"
    segmentStringHashMap['SEGMENT.THIS'] = "this"
    segmentStringHashMap['SEGMENT.THAT'] = "that"
    segmentStringHashMap['SEGMENT.POINTER'] = "pointer"
    segmentStringHashMap['SEGMENT.TEMP'] = "temp"

    commandStringHashMap['COMMAND.ADD'] = "add"
    commandStringHashMap['COMMAND.SUB'] = "sub"
    commandStringHashMap['COMMAND.NEG'] = "neg"
    commandStringHashMap['COMMAND.EQ'] = "eq"
    commandStringHashMap['COMMAND.GT'] = "gt"
    commandStringHashMap['COMMAND.LT'] = "lt"
    commandStringHashMap['COMMAND.AND'] = "and"
    commandStringHashMap['COMMAND.OR'] = "or"
    commandStringHashMap['COMMAND.NOT'] = "not"

    def __init__(self, fOut):
        try:
            # self.f = open(fOut, 'w')
            self.f = fOut # self.f = fOut -> Seria la otra opcion si esta linea saca error
        except:
            print("No se encontro el archivo o bien tienes un error en el VMWriter")
        


    def writePush(self,segment, index):
        writeCommand("push",segmentStringHashMap[segment],int(index))


    def writePop(self, segment, index):
        writeCommand("pop",segmentStringHashMap[segment],int(index))


    def writeArithmetic(self, command):
        writeCommand(commandStringHashMap[command],"","")

    def writeLabel(self, label):
        writeCommand("label",label,"")

    def writeGoto(self, label):
        writeCommand("goto",label,"")

    def writeIf(self, label):
        writeCommand("if-goto",label,"")
    
    def writeCall(self, name, nArgs):
        writeCommand("call",name,int(nArgs))
    

    def writeFunction(self, name, nlocals):
        writeCommand("function",name,int(nlocals))


    def writeReturn(self):
        writeCommand("return","","")

    def writeCommand(self, cmd, arg1, arg2):

        f.write(cmd + " " + arg1 + " " + arg2 + "\n")

    def close(self):
        f.close()
    




