#!/usr/bin/python

import os
import sys
import fileinput
import re
import subprocess
import configparser
import contextlib
import math

import Recipe
import FileUtils

def removeUnusedIncludes(path):
    for include in generateIncludeList(path):
        f = FileUtils.FileWithBackup(path)
        f.deleteLine(include)
        if not canCompileToObjectCode(path):
            f.restore()

def canCompileToObjectCode(path):
    return not subprocess.call(Recipe.makeRecipe(path), 
                       stderr=open(os.devnull, 'wb'), 
                       shell=True)

def generateIncludeList(path):
    includes = []
    for line in readFile(path).split('\n'):
        if re.match( r'^#include.*', line):
            includes.append(line)
    return includes

def readFile(path):
    fileContent = ""
    with open (path, 'r') as f:
        fileContent = f.read()
    return fileContent

@contextlib.contextmanager
def changeWorkingDir(path):
    startingDirectory = os.getcwd()
    os.makedirs(path, exist_ok=True)
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(startingDirectory)

def countFilesRecursively(path):
    count = 0
    for root, subdirs, files in os.walk(path):
        for filename in files:
            ext = os.path.splitext(filename)[-1].lower()
            if(ext == '.cpp'):
                count += 1
    return count

config = configparser.ConfigParser()
config.read('config.ini')
workingDirectory = config['DEFAULT']['WorkingDir']

processedFiles = 0
numberOfFiles = countFilesRecursively(workingDirectory)
progressLineLength = 25

for root, subdirs, files in os.walk(workingDirectory):
    if '.git' in subdirs:
        subdirs.remove('.git')

    for filename in files:
        file_path = os.path.join(root, filename)

        ext = os.path.splitext(filename)[-1].lower()
        if(ext == '.cpp'):
            removeUnusedIncludes(file_path);
            processedFiles += 1
            progress = math.floor(processedFiles / numberOfFiles * progressLineLength)
            print('total:\t[%s%s]' % ('#'*progress, ' '*(progressLineLength - progress)), end='\r')        

print('\nDONE!')
