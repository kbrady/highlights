#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:50:40 2017

@author: jorge
"""

import csv

import sys
import os
import errno

import numpy as np
import pandas as pd




#==============================================================================
#  Line capture routine
#==============================================================================

def get_lines(filename):
    #read a file and returns a list with its lines
    line_list = []
    with open(filename, 'r') as open_file:
        line_list = [line for line in open_file]
    return line_list

def get_name(lines, target_name):
    #retrieves the respective name from the file, determine dby target_name
    try:
        num_lines=len(lines)
        for t in range(num_lines):
            line_temp=lines[t]
            line_title=line_temp.rsplit()[0]
            line_file=line_temp.rsplit()[1]
            if line_title==target_name:
                return line_file

        raise ValueError       
    except ValueError:
        print "Could not find name of file for '%s'."%(target_name)
        raise
 
        
    return " "


#==============================================================================
#  Get input file name
#==============================================================================

file_names='names.dat'


line_list=get_lines(file_names)
file_input=get_name(line_list,"spell_corrected:")

print "Input Name acquired ", file_input

highlight_info=file_input

#==============================================================================
# Output file name
#==============================================================================

file_out=get_name(line_list,"clean:")

print "Output Name acquired ", file_out

#==============================================================================
# Source files 
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


#==============================================================================
# Process input files
# Here we clean up the input files from any extra blank characters 
#==============================================================================

print "Processing input files"

def read_whole(filename):
    # reads a file and reaturns its contents as a string
        file_inp=filename
        try:
            str_w=open(filename,'r').read()
        
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return str_w

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

file_lines=[0]*number_of_parts
file_set=[0]*number_of_parts
t=0
for t in range(number_of_parts):
    print t, input_files[t]
    file_lines[t]=get_lines(input_files[t])
    file_set[t]=get_clean_text_file(input_files[t])




#==============================================================================
# Read the data from the participants file
#==============================================================================
print "Reading data from participants"

data_orig=pd.read_csv(highlight_info, na_filter=False, dtype=str )
size_data=len(data_orig)



#==============================================================================
# Validate highlights 
#==============================================================================
print "Validating highlights"

highl_index_beg=[0]*size_data
highl_index_end=[0]*size_data

array_highlight=np.array(data_orig["highlight"], dtype=int )
num_highlights=sum(array_highlight)

valid_highlights=np.array([0]*size_data, dtype=bool)

t=0  
failure_count=0  #stores the number of highlights that were not located
for t in range(size_data):     
     #print "Checking row", t        
     high_of_row=get_clean_text(data_orig.loc[t,"Text"])
     try:
         usr_id=int(data_orig.loc[t,"Student ID"])          
     
     except ValueError:
         print "Error at ",t,data_orig.loc[t,"Student ID"]
         valid_highlights[t]=False
         raise
     #print "Checking ID", usr_id
     file_index=np.int(data_orig.loc[t,"Part"])        
     file_cleaned = "" #cleanses the string, for security
     file_cleaned = file_set[file_index-1]
     index= file_cleaned.find(high_of_row)       
     if index == -1 :
         print "Problems in row %d , ID= %d , Text '%s' "%(t+1, usr_id ,high_of_row)
         failure_count=failure_count+1
         valid_highlights[t]=False
     else:
         valid_highlights[t]=True    
     highl_index_beg[t]=index
     highl_index_end[t]=index+len(high_of_row)-1
     data_orig.loc[t,"ind_start"]=highl_index_beg[t]
     data_orig.loc[t,"ind_end"]=highl_index_end[t]
    
print "We have %d highlights that were not located "%(failure_count)   
print "Problematic rows will be dropped"     
print " \n"

#==============================================================================
#  Getting rid of bad text selections 
#==============================================================================

array_should_drop= np.logical_not(valid_highlights)  #schedule them for elimination
data_clean=data_orig.drop(data_orig[array_should_drop].index ) # drop the bad rows
data_clean.reset_index(drop=True, inplace=True)     

print "Eliminated problem rows"
#==============================================================================
# Save output
#==============================================================================

data_clean.to_csv(file_out, header=True , index=False)

print "Finished outputting cleaned highlights"



