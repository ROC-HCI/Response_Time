import csv
import glob
import os
import logging
import sys
import os
import glob
import subprocess
import math
import glob

def isNumber(s):
    try:
        float(s)
        if(math.isnan(float(s))):
            return False
        return True
    except ValueError:
        return False

def findAverage(fileName,q1,q2):
    f_in = open(fileName)
    csv_f = csv.reader(f_in)
    first_row=next(csv_f)
    num_col=len(first_row)
    sum_array_q1=[0]*num_col
    count_array_q1=[0]*num_col
    average_array_q1=[0]*num_col
    sum_array_q2=[0]*num_col
    count_array_q2=[0]*num_col
    average_array_q2=[0]*num_col    
    f_out=open('output/out_avg.csv','a')
    wr=csv.writer(f_out)
    for row in csv_f:
        for i in range(num_col):
            if(i>len(row)-1):
                break
            if(isNumber(row[i])):
                if(float(row[0])<float(q2)):                    
                    sum_array_q1[i]+=float(row[i])
                    count_array_q1[i]+=float(1)
                else:
                    sum_array_q2[i]+=float(row[i])
                    count_array_q2[i]+=float(1)                 
                                     
    for i in range(num_col):
        if (count_array_q1[i]==0):
            average_array_q1[i]='nan'
        else:
            average_array_q1[i]=float(sum_array_q1[i])/float(count_array_q1[i])
            
    for i in range(num_col):
        if (count_array_q2[i]==0):
            average_array_q2[i]='nan'
        else:
            average_array_q2[i]=float(sum_array_q2[i])/float(count_array_q2[i])
            
    average_array_q1.insert(0,fileName)
    average_array_q1[1]='Q1'
    average_array_q2.insert(0,fileName)
    average_array_q2[1]='Q2'
    wr.writerow(average_array_q1)
    wr.writerow(average_array_q2)    
    f_in.close()
    f_out.close()
    
def findAbsoluteChanges(fileName,q1,q2):
    f_in = open(fileName)
    csv_f = csv.reader(f_in)
    first_row=next(csv_f)
    num_col=len(first_row)
    sum_array_q1=[0]*num_col
    count_array_q1=[0]*num_col
    average_array_q1=[0]*num_col
    sum_array_q2=[0]*num_col
    count_array_q2=[0]*num_col
    average_array_q2=[0]*num_col
    prev_val_array=[0]*num_col
    f_out=open('output/out_abs.csv','a')
    wr=csv.writer(f_out)
    for row in csv_f:
        for i in range(num_col):
            if(i>len(row)-1):
                break
            if(isNumber(row[i])):
                if(float(row[0])<float(q2)):
                    if(prev_val_array[i]==0):
                        prev_val_array[i]=row[i]
                    else:
                        sum_array_q1[i]+=abs(float(row[i])-float(prev_val_array[i]))
                        count_array_q1[i]+=float(1)
                        prev_val_array[i]=row[i]
                else:
                    if(prev_val_array[i]==0):
                        prev_val_array[i]=row[i]
                    else:
                        sum_array_q2[i]+=abs(float(row[i])-float(prev_val_array[i]))
                        count_array_q2[i]+=float(1)
                        prev_val_array[i]=row[i]
                                     
    for i in range(num_col):
        if (count_array_q1[i]==0):
            average_array_q1[i]='nan'
        else:
            average_array_q1[i]=float(sum_array_q1[i])/float(count_array_q1[i])
            
    for i in range(num_col):
        if (count_array_q2[i]==0):
            average_array_q2[i]='nan'
        else:
            average_array_q2[i]=float(sum_array_q2[i])/float(count_array_q2[i])
            
    average_array_q1.insert(0,fileName)
    average_array_q1[1]='Q1'
    average_array_q2.insert(0,fileName)
    average_array_q2[1]='Q2'
    wr.writerow(average_array_q1)
    wr.writerow(average_array_q2)    
    f_in.close()
    f_out.close()    

def writeColumnNamesToOutputFile(fileName):
    f_in = open(fileName)
    csv_f = csv.reader(f_in)    
    first_row=next(csv_f)
    first_row.insert(0,'fileName')
    f_out_avg=open('output/out_avg.csv','w')
    f_out_abs=open('output/out_abs.csv','w')
    wr_avg=csv.writer(f_out_avg)
    wr_abs=csv.writer(f_out_abs)
    wr_avg.writerow(first_row)
    wr_abs.writerow(first_row)
    f_in.close()
    f_out_avg.close()
    f_out_abs.close()

def generateHashMapforQ1Q2WithKeyRootFileName(fileName):
    f_in = open(fileName)
    csv_f = csv.reader(f_in)
    next(csv_f)
    q1_map={}
    q2_map={}
    for row in csv_f:
        q1_map[row[0]]=row[2]
        q2_map[row[0]]=row[3]
    return q1_map,q2_map
 
 
        
q1_map,q2_map = generateHashMapforQ1Q2WithKeyRootFileName('ResponseTimeIntervals-data.csv')    
csv_file_name_list = glob.glob("example/*.csv")
#print(q1_map)
#print(q2_map)
writeColumnNamesToOutputFile(csv_file_name_list[0])
for csv_file_name in csv_file_name_list:
    rootName=csv_file_name[csv_file_name.find('/')+1:csv_file_name.rfind('-')]
    if rootName in q1_map:
        findAverage(csv_file_name,q1_map[rootName],q2_map[rootName])
        findAbsoluteChanges(csv_file_name,q1_map[rootName],q2_map[rootName])
    else:
        print(rootName)
if isNumber('0.0018'):
    print('number')
else:
    print('not number')

