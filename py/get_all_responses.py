#!/usr/bin/env python3

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
    2016-03-02_14-03-04-887-I-RUTHEH.webm
    2016-03-02_14-03-04-887-W-Simplyme.webm
  
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

print("hello")


# check if the directory is specified, if not error msg

# is arg[1] actually a directory?

# get *.TextGrid files from directory 

# determine file pairs

# for each pair call deception.main java program



