import os
import sys
import fileinput
import re
import subprocess

walk_dir = sys.argv[1]

def removeUnusedIncludes(path):
    print('\t- file %s' % (path))
    
    fileSize = os.path.getsize(path)
    with open (path, 'r') as f:
        fileContent = f.read()

    for lineContent in fileContent.split('\n'):
        if re.match( r'^#include.*', lineContent):
            with open(path, 'r') as f:
                backup = f.read();
            for lineFromWorkingCopy in fileinput.input(path, inplace=1):
                if not lineContent == lineFromWorkingCopy.rstrip('\n'):
                    sys.stdout.write(lineFromWorkingCopy)
            subprocess.call("g++ -E -std=c++11  " + path + " >preproc_out", shell=True);
            if os.path.getsize("preproc_out") < fileSize: 
                if subprocess.call("g++ -c -std=c++11 " + path, shell=True):
                    with open(path, 'w') as f:
                        f.write(backup)

    return

for root, subdirs, files in os.walk(walk_dir):
    if '.git' in subdirs:
        subdirs.remove('.git')

    for filename in files:
        file_path = os.path.join(root, filename)

        ext = os.path.splitext(filename)[-1].lower()
        if(ext == '.cpp'):
            removeUnusedIncludes(file_path);
