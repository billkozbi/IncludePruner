#!/usr/bin/python

import os
import sys
import fileinput
import re
import subprocess
import configparser
import recipe
import contextlib

def removeUnusedIncludes(path):
    print('\t- file %s' % (path))
    
    for include in generateIncludeList(path):
        backup = readFile(path)
        deleteIncludeFromFile(path, include)
        if isIncludeNecessary(path):
            writeToFile(path, backup)
    return

def isIncludeNecessary(path):
    with changeWorkingDir():
        return subprocess.call(recipe.makeRecipe(path), 
                           stderr=open(os.devnull, 'wb'), shell=True)

def deleteIncludeFromFile(path, include):
    for line in fileinput.input(path, inplace=1):
        if not include == line.rstrip('\n'):
            sys.stdout.write(line)
    return

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

def writeToFile(path, content):
    with open(path, 'w') as f:
        f.write(content)
    return

@contextlib.contextmanager
def changeWorkingDir():
    objPath = './objs'
    startingDirectory = os.getcwd()
    os.makedirs(objPath, exist_ok=True)
    try:
        os.chdir(objPath)
        yield
    finally:
        os.chdir(startingDirectory)

config = configparser.ConfigParser()
config.read('config.ini')
for root, subdirs, files in os.walk(config['DEFAULT']['WorkingDir']):
    if '.git' in subdirs:
        subdirs.remove('.git')

    for filename in files:
        file_path = os.path.join(root, filename)

        ext = os.path.splitext(filename)[-1].lower()
        if(ext == '.cpp'):
            removeUnusedIncludes(file_path);
