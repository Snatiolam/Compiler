import os
import sys
import glob
from CompilationEngine import *

class JackComplier:

    def getJackFiles(direccion):
        files = []
        try:
            files = os.listdir(direccion.replace("\\","")) 
        except:
            files = os.listdir(direccion) 

        result = []

        if (files == []):
            print("Files not found")
            return result

        for f in files:

            if (f.find('.jack') != -1):
                result.append(f)

        return result

def main():
    if (len(sys.argv) == 1):
        print("Usage:python JackCompiler [filename.jack|directory]")
    else:
        fileInName = sys.argv[1]
        fileIn = ""
        carpeta = False
        try:
            fileIn = open(fileInName,'r')
        except:
            carpeta = True

        fileOutPath = ""

        fileOut = ""

        jackFiles = []

        if (not carpeta): 

            path = fileIn

            if (sys.argv[1].find(".jack") == -1): 
                print(".jack file is required!")

            jackFiles.append(fileIn)

        else:
            temp = sys.argv[1]
            jackFiles = JackComplier.getJackFiles(temp)

            if (len(jackFiles) == 0):
                print("No jack file in this directory")


        for f in jackFiles:
            fileOutPath = f[0:f.find('.jack')] + '.vm'
            fileOut = open(fileOutPath, 'w+')

            compilationEngine = CompilationEngine(f,fileOut)
            compilationEngine.compileClass()

            print("File created : " + fileOutPath)

if __name__ == "__main__": 
    main()

