import os
import sys

class JackComplier:

    def getJackFiles(self, direccion):
        files = []
        for root, dirs, files in os.walk(direccion):
            for filename in files:
                files.append(filename)

        print(files)
        result = []

        if (files == []):
            print("Files not found")
            return result

        for f in files:

            if (f.find('.jack') != -1):
                result.append(f)

        return result

    if __name__ == "__main__": 
         
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
                jackFiles = JackComplier(str(sys.argv[1]))

                if (len(jackFiles) == 0):
                    print("No jack file in this directory")


            for f in jackFiles:

                fileOutPath = f.getAbsolutePath().substring(0, f.getAbsolutePath().lastIndexOf(".")) + ".vm"
                fileOut = File(fileOutPath)

                compilationEngine = CompilationEngine(f,fileOut)
                compilationEngine.compileClass()

                print("File created : " + fileOutPath)

