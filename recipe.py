#!/usr/bin/python

def makeRecipe(path):
    recipe = ""
    recipe += "g++ -c -std=c++11 %s;" % path
    return recipe


