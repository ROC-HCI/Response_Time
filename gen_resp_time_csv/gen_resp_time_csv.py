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
    print(responseFile.fileName)
    print('example/'+responseFile.root+'-'+responseFile.fileName[24]+'-ResponseTime.txt')
    filepath=''
    if(responseFile.fileName.find('-T-') > int(-1)):
      filepath='example/'+responseFile.root+'-'+'T'+'-ResponseTime.txt'
    else:
      filepath='example/'+responseFile.root+'-'+'B'+'-ResponseTime.txt'
    with open(filepath) as f:
        content = f.read().splitlines()
        Q1_sum=float(0)
        Q1_count = int(0)
        Q2_sum=float(0)
        Q2_count = int(0)
        #Q3_sum=float(0)
        #Q3_count = int(0)
        for line in content:
            #print(line)
            words=line.split()
            if (float(words[2]) >= float(responseFile.Q1) 
                and float(words[2]) < float(responseFile.Q2_start)):
                Q1_sum+= float(words[0])
                Q1_count+= int(1)     
            if (float(words[2]) >= float(responseFile.Q2_start)):
                Q2_sum += float(words[0]) 
                Q2_count+= int(1) 
        
        avg_list=[]
        #print(Q1_sum)
        #print(Q1_count)
        #print(Q2_sum)
        #print(Q2_count)
        #print(Q3_sum)
        #print(Q3_count)
        if(float(Q1_count)>0):
            avg_list.append(float(Q1_sum/Q1_count))
        else:
            avg_list.append('nan')
        
        if(float(Q2_count)>0):
            avg_list.append(float(Q2_sum/Q2_count))
        else:
            avg_list.append('nan')        
        
        return avg_list
        

print('example/ResponseTimeIntervals-data.csv')
f = open('example/ResponseTimeIntervals-data.csv')
csv_f = csv.reader(f)
responseFileList=[]
for row in csv_f:
    responseFileList.append(ResponseFile(row[0],row[1],row[2],row[3],row[4],row[5]))
 
print('end') 
print(responseFileList)
responseFileList.pop(0)


with open('example/ResponseTimeIntervalsAverage.csv', 'a') as outFile:
    wr = csv.writer(outFile)
    for responseFile in responseFileList:
        avg_list = getAvgResponseTimeDuringQ1Q2Q3(responseFile)
        Q1_avg = avg_list[0]
        Q2_avg = avg_list[1]
        #Q3_avg = avg_list[2]
        print(Q1_avg)
        print(Q2_avg)
        #print(Q3_avg)
        row=[responseFile.root,Q1_avg,Q2_avg,'','']
        print(row)    
        wr.writerow(row)    
  


    
