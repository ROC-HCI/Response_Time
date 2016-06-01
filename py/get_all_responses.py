#!/usr/bin/env python3
import sys
import os
import glob


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
    raise ValueError("No target diretcory inputted")
# is arg[1] actually a directory?
if(not os.path.isdir(sys.argv[1])):
    raise ValueError("Directory does not exist")

# get *.TextGrid files from directory 

grids = glob.glob(sys.argv[1] + '/*.TextGrid')

for g in grids:
    gSplit = g.split("-")
    assert(len(gSplit) >= 8)
    print(g)
   


# determine file pairs



# for each pair call deception.main java program



