#!/usr/bin/env python3
""" 
------------------------------------------------------------------------
  TODO

------------------------------------------------------------------------
"""

import csv
import glob
import os
import logging


import sys
import os
import glob
import subprocess

class ResponseFile(object):

    root='' 
    fileName=''
    Q1=''
    Q2_start=''
    Q2_end=''
    Q3=''

    def __init__(self,root,fileName,Q1,Q2_start,Q2_end,Q3):
        self.root = root
        self.fileName = fileName
        self.Q1 = Q1
        self.Q2_start = Q2_start
        self.Q2_end = Q2_end
        self.Q3 = Q3

def getAvgResponseTimeDuringQ1Q2Q3(responseFile):
    print('example/'+responseFile.fileName[:-4]+'.TextGrid-ResponseTime.txt')
    with open('example/'+responseFile.fileName[:-4]+'.TextGrid-ResponseTime.txt') as f:
        content = f.read().splitlines()
        Q1_sum=float(0)
        Q1_count = int(0)
        Q2_sum=float(0)
        Q2_count = int(0)
        Q3_sum=float(0)
        Q3_count = int(0)
        for line in content:
            #print(line)
            words=line.split()
            if (float(words[2]) >= float(responseFile.Q1) 
                and float(words[2]) < float(responseFile.Q2_start)):
                Q1_sum+= float(words[0])
                Q1_count+= int(1) 
                
            elif (float(words[2]) >= float(responseFile.Q2_start) 
                and float(words[2]) < float(responseFile.Q2_end)):
                Q2_sum += float(words[0]) 
                Q2_count+= int(1) 
            elif (float(words[2]) >= float(responseFile.Q3)):
                Q3_sum += float(words[0]) 
                Q3_count+= int(1)
        avg_list=[]
        #print(Q1_sum)
        #print(Q1_count)
        #print(Q2_sum)
        #print(Q2_count)
        #print(Q3_sum)
        #print(Q3_count)
        avg_list.append(float(Q1_sum/Q1_count))
        avg_list.append(float(Q2_sum/Q2_count))
        avg_list.append(float(Q3_sum/Q3_count))
        return avg_list
        

print('example/ResponseTimeIntervals - data.csv')
f = open('example/ResponseTimeIntervals - data.csv')
csv_f = csv.reader(f)
responseFileList=[]
for row in csv_f:
    responseFileList.append(ResponseFile(row[0],row[1],row[2],row[3],row[4],row[5]))
 
print('end') 
print(responseFileList)
responseFileList.pop(0)

with open('example/ResponseTimeIntervalsAverage.csv', 'a') as testfile:
    wr = csv.writer(testfile)
    for responseFile in responseFileList:
        avg_list = getAvgResponseTimeDuringQ1Q2Q3(responseFile)
        Q1_avg = avg_list[0]
        Q2_avg = avg_list[1]
        Q3_avg = avg_list[2]
        print(Q1_avg)
        print(Q2_avg)
        print(Q3_avg)
        row=[responseFile.root,Q1_avg,Q2_avg,Q3_avg,'']
        print(row)    
        wr.writerow(row)    
  


    
