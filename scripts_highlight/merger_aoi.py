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



#==============================================================================
# Output files
#==============================================================================

file_out = 'aoi_merged.csv'


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


file_sources='aoi_merge_list.dat'
lines_source=get_lines(file_sources)

try:
    number_of_parts=int(lines_source[0])

except ValueError:
    print "Problem with the number of parts to merge"
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



#==============================================================================
#  Read file
#==============================================================================

len_frames=[0]*number_of_parts

#frame_aois=pd.read_csv(input_files[0], na_filter=False, dtype=str )


for t in range(0,number_of_parts):
    frame_temp=pd.read_csv(input_files[t], na_filter=False, dtype=str )
    len_frames[t]=len(frame_temp)
    frame_temp["origin_file"]="%d"%(t)
    if t==0:
        frame_aois=frame_temp.copy()       
    else: 
        frame_aois=frame_aois.append(frame_temp,ignore_index=True)



#==============================================================================
#  Unique IDs
#==============================================================================
print "Output statistics by ID"

ID_unique_array=list( set( np.array(frame_aois["ID"], dtype=int) ) )
ID_unique_array.sort()
num_ID_unique= len(ID_unique_array)
series_condition=[" "]*num_ID_unique

aoi_results=pd.DataFrame( { "ID": ID_unique_array , "Condition": [" "]*num_ID_unique } )


lettercond=["A","B"]
dict_ID_to_index={}
dict_index_to_ID={}

t=0
for ID in ID_unique_array:    
    for letter in lettercond:        
        pairs_ID_letter=[ID, letter]
        pair=tuple(pairs_ID_letter)               
        dict_ID_to_index[pair]=t
        dict_index_to_ID[t]=pair
        t=t+1    
        
num_comp_array=t    



#==============================================================================
# Making new frame
#==============================================================================

head_list=list(frame_aois)
head_list_reduced=head_list[:]
head_list_reduced.remove("ID")

merged_aoi= pd.DataFrame( { "ID": [""]*num_comp_array  }  )   

for head in head_list_reduced:    
    merged_aoi[head]=np.array([""]*num_comp_array, dtype=str )



#==============================================================================
# Adding
#==============================================================================
def is_incomplete(entry_frame):
    str_condition=entry_frame  
    try:
        index_incom=str_condition.index("incomplete")
    except ValueError:         
        return False            
    return True

#==============================================================================
# filling up merged frame
#==============================================================================

print "filling up frame"
num_merged=len(frame_aois)
for t in range(num_merged):
    entry_ID=int(frame_aois.loc[t,"ID"])
    letter_str=(frame_aois.loc[t,"Condition"])
    
    letter=(letter_str.split())[0]
     
    try:
        pair=tuple([entry_ID,letter])
        row=dict_ID_to_index[pair]        
    except KeyError:
        print "Error processing row %d, not in set of valid ID"%(t)
        print pair
        raise       
    
    
    
   # incom_orig=is_incomplete(frame_aois.loc[t,"Condition"]  )
   # incom_merged=is_incomplete(frame_aois.loc[t,"Condition"]  )
   
 #   str_condition=frame_aois.loc[t,"Condition"]    
  #  index_incom=str_condition.find("Incomplete")
    
    merged_aoi.loc[row,:]=frame_aois.loc[t,:]    

        
    
    
print "no problem"    
raise 

#==============================================================================
#  Error report
#==============================================================================


motive="Entries with incomplete conditions detected"
array_should_drop= np.logical_not(array_good_condition)  #schedule them for elimination
num_bad_conditions=sum(array_should_drop)


#copy bad rows and report error
df_bad=parts_taken[array_should_drop]
if len(df_bad)>0:
    df_bad.to_csv(file_error_csv, header=True, index=True)
    write_error(file_error_log,df_bad,motive,file_error_csv)
    
size_bad=len(df_bad)
fid_missing=open(file_error_missing, 'w')

for t in range(size_bad):
    s="ID: %s \t missing: %s \n"%(df_bad.loc[t,"ID"], df_bad.loc[t,"missing"])
    fid_missing.write(s)
fid_missing.close()    
    
    
    
    
