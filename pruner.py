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
    
    with open (path, 'r') as f:
        fileContent = f.read()

    for lineContent in fileContent.split('\n'):
        if re.match( r'^#include.*', lineContent):
            with open(path, 'r') as f:
                backup = f.read();
            for lineFromWorkingCopy in fileinput.input(path, inplace=1):
                if not lineContent == lineFromWorkingCopy.rstrip('\n'):
                    sys.stdout.write(lineFromWorkingCopy)
            with changeWorkingDir():
                if subprocess.call(recipe.makeRecipe(path), stderr=open(os.devnull, 'wb'), shell=True):
                    with open(path, 'w') as f:
                        f.write(backup)
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
