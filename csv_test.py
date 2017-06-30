#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 16:07:13 2017

@author: jorge
"""


import csv
from collections import namedtuple

import sys
import os
import errno

import numpy as np
import pandas as pd


file_1 = '/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_1.md'
file_2 = '/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_2.md'
highlight_info = '/home/jorge/Downloads/highlights_files/highlights.csv'

def get_lines(filename):
    line_list = []
    with open(filename, 'r') as open_file:
        line_list = [line for line in open_file]
    return line_list

def read_whole(filename):
        file_inp=filename
        try:
            str=open(filename,'r').read()
        
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return str

file_1_lines = get_lines(file_1)
file_2_lines = get_lines(file_2)


def get_clean_text(str_full):
    #we now read in the whole text as a string into str_full and clean out any blank characters    
    str_words=str_full.split() #removes any whitespaces and line feeds
    text_cleaned=" ".join(str_words) #this reinstates the whitespaces bewteen 
    #creates an array with all the words, no whitespaces or newlines    
    purged_text=text_cleaned.strip() #removes leading and trailing white spaces
    return purged_text

def get_clean_text_file(filename):
    #we now read in the whole text as a string into str_full and clean out any blank characters
    str_full=read_whole(filename)  #has the text in a human readable format    
    purged_text=get_clean_text(str_full) #removes leading and trailing white spaces
    return purged_text



file_1_clean=get_clean_text_file(file_1)
file_2_clean=get_clean_text_file(file_2)

file_set=[file_1_clean, file_2_clean]



data = []

with open(highlight_info, 'r') as input_file:
    reader = csv.reader(input_file, delimiter=',', quotechar='"')
    row_class = None
    for row in reader:
        if row_class is None:
            row_class = namedtuple('row_class', row)
            continue
        try:
            data.append(row_class(*tuple(row)))
        except Exception as e:
            print row
            raise e

def to_key(x):
    return (int(x.Participant), x.Condition, int(x.Part))

keys = set([to_key(x) for x in data])

data_dict = {}
for k in keys:
    data_dict[k] = [x.Highlight for x in data if to_key(x) == k]

highl_index_beg=[0]*len(data)
highl_index_end=[0]*len(data)

t=0  
failure_count=0  #stores the number of highlights that were not located
for x in data:
     t=t+1
     num_highlights=len(x.Highlight)     
     high_of_row=get_clean_text(x.Highlight)     
     file_index=np.int(x.Part)   
     #file_cleaned = file_1_clean if file_index == 1 else file_2_clean
     file_cleaned = ""
     file_cleaned = file_set[file_index-1]
     index= file_cleaned.find(high_of_row)       
     if index == -1 :
         print "Problems in row %d , %s"%(t, high_of_row)
         failure_count=failure_count+1
     highl_index_beg[t-1]=index
     highl_index_end[t-1]=index+len(high_of_row)-1
   
print "We have %d highlights that were not located "%(failure_count)        
print " \n"


line_tag=["start:", "end:"]
mode_dict={"start": 0, "end": 1}

def line_header_remove(input_line,mode):
    tag = input_line.rsplit()[0]  
    tag_ref=line_tag[mode_dict[mode]]    
    if  tag != tag_ref :
        raise  ValueError('Line has incorrect format at the begining.', "Review %s"%(input_line) )
    temp_line=input_line.rsplit()[1:]  
    joint_line=" ".join(temp_line)
    purged_line=joint_line.strip()    
    return purged_line

line_header_remove("start: 12 13 14","start")


def read_aoi(input_file):    
    # this takes the AOI configuration files and returns a dataframe with its contents
    try:
        fid_aoi = open(input_file, 'r')  

        aoi_header_line = fid_aoi.readline() 
        tot_aoi=int(aoi_header_line.rsplit()[0]) #total number of aoi
        aoi_ID=pd.Series( [0]*tot_aoi )
        aoi_part=pd.Series( [0]*tot_aoi )
        aoi_name=pd.Series( [0]*tot_aoi )       
        aoi_start=pd.Series( [0]*tot_aoi )
        aoi_end=pd.Series( [0]*tot_aoi )
        aoi_ind_start=pd.Series( [0]*tot_aoi )
        aoi_ind_end=pd.Series( [0]*tot_aoi )                
        aoi_hitcount=pd.Series( [0]*tot_aoi )
        
        for t in range(tot_aoi):
            line_blank=fid_aoi.readline()   #ignores line
            
            line_aoi_head=fid_aoi.readline()
            print line_aoi_head
            aoi_head=line_aoi_head.rsplit()
            print "part, ", aoi_head[1]
            aoi_ID[t]=aoi_head[0]
            aoi_part[t]=aoi_head[1]
            aoi_name[t]=aoi_head[2]
            
            line_aoi_beg=fid_aoi.readline()  #begining 
            line_aoi_end=fid_aoi.readline()  #end 
        
            line_aoi_beg=line_header_remove(line_aoi_beg, "start")  #removes the start tag             
            line_aoi_end=line_header_remove(line_aoi_end, "end")  #removes the end tag  
            aoi_start[t]=line_aoi_beg
            aoi_end[t]=line_aoi_end
            
        fid_aoi.close()
     
        aoi_frame=pd.DataFrame({"ID": aoi_ID, 
                                "part": aoi_part, 
                                "name": aoi_name, 
                                "start": aoi_start, 
                                "end": aoi_end, 
                                "ind_start": aoi_ind_start, 
                                "ind_end": aoi_ind_end,
                                "hit_count": aoi_hitcount }) 
    
    
    
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "Error reading {0} ".format(input_file)
        raise
        quit()
    except ValueError:
        print "Could not convert data ."
        raise
        quit()     
    return aoi_frame  

def unique_find(str_target,str_text):
    ind_first=str_text.find(str_target)
    ind_last=str_text.rfind(str_target)
    match= (ind_first == ind_last) 
    struct_find=[ind_first,match]
    return struct_find

aoi_frame=read_aoi("aoi_template.dat")
tot_aoi=len(aoi_frame["ID"])
print "We have a total of %d AOI \n"%(tot_aoi) 
print aoi_frame["name"]

for t in range(tot_aoi):
    part_num=aoi_frame["part"][t]
    file_cleaned= file_set[part_num-1]    
    str_start=aoi_frame["start"][t]    
    struct_find= unique_find(str_start,file_cleaned)
    ind_start=struct_find[0]    
    print ind_start
    #ind_start=file_cleaned.find(str_start) 
    if (struct_find[1] == False):
        print "Error. The area of interest delimeing words are repeated in the text. Select a longer "
        ind_start=-1
    aoi_frame.loc[t,"ind_start"]=ind_start
    str_end=aoi_frame["end"][t]    
    ind_end=file_cleaned.find(str_end,ind_start)    
    aoi_frame.loc[t,"ind_end"]=ind_end+len(str_end)-1 #this sets the index at the last letter of the AOI
    
    
# count hits    
t=0
for x in data:
     t=t+1
     for k in range(tot_aoi):
         beg_in_range=(highl_index_beg[t-1] >= aoi_frame.loc[k,"ind_start"]) and (highl_index_beg[t-1] <= aoi_frame.loc[k,"ind_end"])
         end_in_range=(highl_index_end[t-1] >= aoi_frame.loc[k,"ind_start"]) and (highl_index_end[t-1] <= aoi_frame.loc[k,"ind_end"])
         if beg_in_range or end_in_range:
             aoi_frame.loc[k,"hit_count"]=aoi_frame.loc[k,"hit_count"]+1
             print t, "is a hit", beg_in_range, end_in_range
             
        
     
         
   


