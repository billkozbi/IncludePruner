#!/usr/bin/python

import os

class Reciper:
    def __init__(self, pathToPrintedMakefile):
        self.pathToPrintedMakefile = pathToPrintedMakefile
        self.prefix = "cd %s; " % os.path.dirname(pathToPrintedMakefile)

    def generateRecipeForFile(self, pathToCppFile):
        recipe = ""
        recipe += self.prefix
        recipe += self.__getRecipeFromPrintedMakefile(pathToCppFile)
        return recipe

    def __getRecipeFromPrintedMakefile(self, pathToCppFile):
        line = ""
        with open(self.pathToPrintedMakefile, 'r') as f:
            for line in f:
                if pathToCppFile in line:
                    return line
        return line

