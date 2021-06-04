import os
import sys
import glob
from CompilationEngine import *

class JackComplier:

    def getJackFiles(direccion):
        files = []
        try:
            prueba = os.listdir(direccion.replace("\\","")) 
            for dirpath,_,filenames in os.walk(direccion.replace("\\","")):
                for f in filenames:
                    files.append(os.path.abspath(os.path.join(dirpath, f)))
        except:
            #files = os.listdir(direccion) 
            for dirpath,_,filenames in os.walk(direccion):
                for f in filenames:
                    files.append(os.path.abspath(os.path.join(dirpath, f)))

        result = []
        if (files == []):
            print("Files not found")
            return result

        for f in files:

            if (f.find('.au') != -1):
                result.append(f)
        return result


if __name__ == "__main__": 
    if (len(sys.argv) == 1):
        print("Usage:python AuCompiler [filename.au|directory]")
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

        auFiles = []

        if (not carpeta): 

            path = fileIn

            if (sys.argv[1].find(".au") == -1): 
                print(".au file is required!")

            auFiles.append(fileIn)

        else:
            temp = sys.argv[1]
            auFiles = JackComplier.getJackFiles(temp)

            if (len(auFiles) == 0):
                print("No Au file in this directory")


        for f in auFiles:
            
            fileOutPath =  f[0:f.find('.au')] + '.vm'
            fileOut = open(fileOutPath, 'w+')
            compilationEngine = CompilationEngine(f,fileOut)
            compilationEngine.compileClass()
            
            print("File created : " + fileOutPath)

