#!/usr/bin/env python3
import sys
import os
import glob
import subprocess



# Helper classes/methods 
class pair:
    interrogator = None
    witness = None
    
    def __init__(self, interrogator, witness):
        self.interrogator = interrogator
        self.witness = witness
        
    def __str__(self):
        return "Interrogator: " + interrogator + "\nWitness: " + witness

#Returns true if files match, returns false if they do not
def isMatch(fileA, fileB):
    fileA = fileA.split("-")
    fileB = fileB.split("-")
    
    assert(len(fileA) >= 8) 
    assert(len(fileB) >= 8) 
    
    for i in range(6):
        if(fileA[i] != fileB[i]):
            return False
    
    return True

def getInterrogator(fileA, fileB):
    fileASplit = fileA.split("-")
    fileBSplit = fileB.split("-") 
    if(fileASplit[6] == "I"):
        return fileA
    if(fileBSplit[6] == "I"):
        return fileB
    else:
        raise ValueError("Neither file is interrogator")
    
def getWitness(fileA, fileB):
    fileASplit = fileA.split("-")
    fileBSplit = fileB.split("-") 
    if(fileASplit[6] == "W"):
        return fileA
    if(fileBSplit[6] == "W"):
        return fileB
    else:
        raise ValueError("Neither file is witness")    

def getOutputName(file):
    name = sys.argv[1] + '/'
    
    file = file.split("/")
    file = file[len(file) - 1]
    file = file.split("-")
    for i in range(6):
        name += file[i] + "-"
    
    name += "ResponseTime.txt"
    return name
    

"""
-------------------------------------------------------------------------------
  ./get_all_responses <directory>

  ./get_all_responses example

-------------------------------------------------------------------------------
  Script for automatically calling Response_time java program for all 
  TextGrids.

  Input is a directory of *.TextGrid file pairs. 
  Interrogator and Witness pairs are determined by the initial substring.

  example file pair:
    2016-03-02_14-03-04-887-I-RUTHEH.TextGrid
    2016-03-02_14-03-04-887-W-Simplyme.TextGrid
  
  The "2016-03-02_14-03-04-887-" substring indicates the pair.
  The "-W-" and "-I-" indicate whether file is for interrogator or witness.

  The substring format should be preserved.


  -----------------
  The script takes the steps of:
    create list all files in directory specified by arg[1]
    first determines a list of all file pairs
    next calls deception.main for each pair of files

"""
# TODO
# TODO







# check if the directory is specified, if not error msg

if(len(sys.argv) < 2):
    raise ValueError("No target directory inputted")
# is arg[1] actually a directory?
if(not os.path.isdir(sys.argv[1])):
    raise ValueError("Directory does not exist")

# get *.TextGrid files from directory 

grids = glob.glob(sys.argv[1] + '/*.TextGrid')
   


# determine file pairs
pairs = []

grids.sort()

for fileA in grids:
    for fileB in grids:
        if(isMatch(fileA, fileB) and (fileA != fileB)): #find match
            interrogator = getInterrogator(fileA, fileB) #identify interrogator 
            witness = getWitness(fileA, fileB) #identify witness 
            pairs.append(pair(interrogator, witness)) #add pair to list
            #Remove files from grids
            grids.remove(fileA)
            grids.remove(fileB)
   
       

# for each pair call deception.main java program


for p in pairs:
    os.system("javac ../src/deception/*.java")
    os.system("java -cp ../src deception.main " + p.interrogator + " " + p.witness + " " + getOutputName(p.witness))  
