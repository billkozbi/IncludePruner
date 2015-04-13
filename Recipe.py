#!/usr/bin/python

def makeRecipe(path):
    recipe = ""
    recipe += "cd /home/bill/programming/IncludePruner/objs; g++ -c -std=c++11 %s;" % path
    return recipe


