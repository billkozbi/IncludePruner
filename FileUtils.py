#!/usr/bin/python

import fileinput
import sys

class FileWithBackup:
    def __init__(self, path):
        self.path = path
        self.backup = ""
        with open (self.path, 'r') as f:
            self.backup = f.read()

    def restore(self):
        with open (self.path, 'w') as f:
            f.write(self.backup)

    def deleteLine(self, lineContent):
        for line in fileinput.input(self.path, inplace=1):
            if not lineContent == line.rstrip('\n'):
                sys.stdout.write(line)

def readFile(path):
    fileContent = ""
    with open (path, 'r') as f:
        fileContent = f.read()
    return fileContent

