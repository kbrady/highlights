#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 03:11:46 2017

@author: jorge
"""

import csv

import sys
import os
import errno

import numpy as np
import pandas as pd

#==============================================================================
# Input files 
#==============================================================================

aoi_filename="aoi_template.dat"

#==============================================================================
# Output files
#==============================================================================

file_out = 'aoi.csv'

file_aoi_text='text_aoi.dat'


#==============================================================================
# Process input files
# Here we clean up the input files from any extra blank characters 
#==============================================================================

print "Processing input files"

def get_lines(filename):
    #read a file and returns a list with its lines
    line_list = []
    try:
        with open(filename, 'r') as open_file:
            line_list = [line for line in open_file]
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "Error reading {0} ".format(filename)
        raise            
    except ValueError:
        print "Error processing %s"%(filename)
        raise
    return line_list

def read_whole(filename):
    # reads a file and reaturns its contents as a string
        file_inp=filename
        try:
            str=open(filename,'r').read()
        
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return str

def get_clean_text(str_full):
    #clean out any blank characters from input string    
    str_words=str_full.split() #removes any whitespaces and line feeds
    text_cleaned=" ".join(str_words) #this reinstates the whitespaces bewteen 
    #creates an array with all the words, no whitespaces or newlines    
    purged_text=text_cleaned.strip() #removes leading and trailing white spaces
    return purged_text

def get_clean_text_file(filename):
    #returns a text file as a single string, purged. 
    str_full=read_whole(filename)  #has the text in a human readable format    
    purged_text=get_clean_text(str_full) #removes leading and trailing white spaces
    return purged_text


#==============================================================================
# Source files loader
#==============================================================================

file_sources='sources.dat'
lines_source=get_lines(file_sources)

try:
    number_of_parts=int(lines_source[0])

except ValueError:
    print "Problem with the number of parts"
    raise

input_files=[""]*number_of_parts
for t in range(number_of_parts):
    s=lines_source[t+1]
    input_files[t]=s.strip()

print input_files

number_of_parts=len(input_files)


file_lines=[0]*number_of_parts
file_set=[0]*number_of_parts
t=0
for t in range(number_of_parts):
    print t, input_files[t]
    file_lines[t]=get_lines(input_files[t])
    file_set[t]=get_clean_text_file(input_files[t])
         

#==============================================================================
#  Read AOI (area of interest) file
#==============================================================================


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
        aoi_text=pd.Series([""]*tot_aoi)
        for t in range(tot_aoi):
            line_blank=fid_aoi.readline()   #ignores line
            
            line_aoi_head=fid_aoi.readline()           
            aoi_head=line_aoi_head.rsplit()            
            aoi_ID[t]=aoi_head[0]
            aoi_part[t]=aoi_head[1]
            aoi_name[t]=aoi_head[2]
            
            line_aoi_beg=fid_aoi.readline()  #begining 
            line_aoi_end=fid_aoi.readline()  #end 
        
            line_aoi_beg=line_header_remove(line_aoi_beg, "start")  #removes the start tag             
            line_aoi_end=line_header_remove(line_aoi_end, "end")  #removes the end tag  
            aoi_start[t]=get_clean_text(line_aoi_beg)
            aoi_end[t]=get_clean_text(line_aoi_end)
                    
            
        fid_aoi.close()
     
        aoi_frame=pd.DataFrame({"AOI_ID": aoi_ID, 
                                "Part": aoi_part, 
                                "name": aoi_name, 
                                "start": aoi_start, 
                                "end": aoi_end, 
                                "ind_start": aoi_ind_start, 
                                "ind_end": aoi_ind_end,
                                "text": aoi_text, 
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
    #this will search for a match and make output its uniquenss
    #the code will search for the fragment from the left and from the right. If its unique the positions will be the same
    ind_first=str_text.find(str_target)
    ind_last=str_text.rfind(str_target)
    match= (ind_first == ind_last) # true if its a unique fragment
    struct_find=[ind_first,match]
    if ind_first==-1 :
        raise ValueError
    return struct_find


aoi_frame=read_aoi(aoi_filename)
tot_aoi=len(aoi_frame["AOI_ID"])
print "We have a total of %d AOI \n"%(tot_aoi) 
print aoi_frame["name"]

for t in range(tot_aoi):
    part_num=aoi_frame["Part"][t]
    file_cleaned=" "
    file_cleaned= file_set[part_num-1]    
    str_start=aoi_frame["start"][t]  
        
    try:
        struct_find= unique_find(str_start,file_cleaned) 
    
    except ValueError:
        print "Could not locate AOI ", t+1 , " named ", aoi_frame.loc[t,"name"], " in part ", part_num
        raise    
    
    ind_start=struct_find[0]     
    if (struct_find[1] == False):
        print "Error. The  delimiting words are repeated in the text. Select a longer fragment "
        ind_start=-1
    aoi_frame.loc[t,"ind_start"]=ind_start
    str_end=aoi_frame["end"][t]    
    try:
        ind_end=file_cleaned.index(str_end,ind_start)   
    
    except ValueError:
        print "Could not locate AOI ", t+1 , " named ", aoi_frame.loc[t,"name"], " in part ", part_num
        raise
    
    aoi_frame.loc[t,"ind_end"]=ind_end+len(str_end)-1 #this sets the index at the last letter of the AOI
    aoi_frame.loc[t,"text"]=file_cleaned[aoi_frame.loc[t,"ind_start"]:aoi_frame.loc[t,"ind_end"]+1]
    

#==============================================================================
# Export AOIs to file
#==============================================================================

def write_aoi_text(filename):
    # reads a file and reaturns its contents as a string
        file_inp=filename
        try:
            fid_aoi_text=open(filename,'w')
            for t in range(tot_aoi):
                str_line=aoi_frame.loc[t,"text"]
                fid_aoi_text.write("AOI_%d :\n \n "%(t+1))
                fid_aoi_text.write(str_line)
                fid_aoi_text.write("\n \n ")
            fid_aoi_text.close()
        
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return 0

write_aoi_text(file_aoi_text)

aoi_frame.to_csv(file_out, header=True, index=False )