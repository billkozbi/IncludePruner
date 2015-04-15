#!/usr/bin/python

import os
import sys
import fileinput
import re
import subprocess
import configparser
import contextlib
import math

import FileUtils
import Recipe

class Pruner:
    def __init__(self, path, recipe):
        self.pathToFile = path
        self.recipeToCompilePath = recipe

    def removeUnusedIncludes(self):
        for include in self.__generateIncludeList():
            f = FileUtils.FileWithBackup(self.pathToFile)
            f.deleteLine(include)
            if not self.__canCompileToObjectCode():
                f.restore()

    def __canCompileToObjectCode(self):
        return not subprocess.call(self.recipeToCompilePath, 
                                   stderr=open(os.devnull, 'wb'), 
                                   shell=True)

    def __generateIncludeList(self):
        includes = []
        for line in FileUtils.readFile(self.pathToFile).split('\n'):
            if re.match( r'^#include.*', line):
                includes.append(line)
        return includes

    
@contextlib.contextmanager
def changeWorkingDir(path):
    startingDirectory = os.getcwd()
    os.makedirs(path, exist_ok=True)
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(startingDirectory)

def countFilesRecursively(path, filenameFilter=None):
    if filenameFilter is None:
        filenameFilter = ".*"
    count = 0
    for root, subdirs, files in os.walk(path):
        for filename in files:
            filenameFilterRegex = r"%s" % filenameFilter
            if re.match(filenameFilterRegex, filename):
                count += 1
    return count

config = configparser.ConfigParser()
config.read('config.ini')

workingDirectory = config['DEFAULT']['WorkingDir']
processedFiles = 0
numberOfFiles = countFilesRecursively(workingDirectory, ".*\.cpp")
progressLineLength = 25

for root, subdirs, files in os.walk(workingDirectory):
    if '.git' in subdirs:
        subdirs.remove('.git')

    for filename in files:
        path = os.path.join(root, filename)

        ext = os.path.splitext(filename)[-1].lower()
        if(ext == '.cpp'):
            p = Pruner(path, "g++ -c %s" % path)
            p.removeUnusedIncludes()
            processedFiles += 1
            progress = math.floor(processedFiles / numberOfFiles * progressLineLength)
            print('total:\t[%s%s]' % ('#'*progress, ' '*(progressLineLength - progress)), end='\r')        

print('\nDONE!')
