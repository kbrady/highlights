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
# functions for path
#==============================================================================

def get_path_aoi(file_sec):
    name_extract=os.path.split(file_sec)
    new_name="aoi.csv"    
    file_aoi=os.path.join(name_extract[0],new_name)
    return file_aoi

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

path_aoi=get_path_aoi(input_files[0])


#==============================================================================
# Read file with aoi definitions
#==============================================================================

aoi_def=pd.read_csv(path_aoi, na_filter=False, dtype=str)

col_list_aoi=[0]*number_of_parts
sel_list_aoi=[0]*number_of_parts
for p in range(number_of_parts):    
    arr_sel_par=np.array( (aoi_def["Part"][:]=="%d"%(p+1) ), dtype=bool)
    selection=aoi_def[arr_sel_par]
    sel_list_temp=list(selection["ID"])
    list_temp=[]
    for sel in sel_list_temp:
        str_sel="AOI_%d"%( int(sel))
        list_temp.append([str_sel])
    col_list_aoi[p]=list_temp



#==============================================================================
#  Read file with results
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
print "Reading the IDs of participants"

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
    #pairs_ID_letter=[ID, letter]
    #pair=tuple(pairs_ID_letter)               
    dict_ID_to_index[ID]=t
    dict_index_to_ID[t]=ID
    t=t+1    
        
num_comp_array=t    



#==============================================================================
# Making new frame
#==============================================================================

head_list=list(frame_aois)
head_list_reduced=head_list[:]
head_list_reduced.remove("ID")

merged_aoi= pd.DataFrame( { "ID": ID_unique_array }  )   

for head in head_list_reduced:    
    merged_aoi[head]=np.array([""]*num_comp_array, dtype=str )

merged_aoi["count"]= np.array([0]*num_comp_array , dtype=int) 



head_aoi=head_list[:]
for h in head_list:
    ind=h.find("AOI")
    if ind ==-1:
        head_aoi.remove(h)
print "Found the following AOI:"
print head_aoi

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


def is_zero_or_blank(field):
    if ( field=="%d"%(0) ) or (field==""):
        return True
    
    return False

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
        #pair=tuple([entry_ID,letter])
        row=dict_ID_to_index[entry_ID]        
    except KeyError:
        print "Error processing row %d, not in set of valid ID"%(t) 
        raise       

       
    if merged_aoi.loc[row,"count"]==0:
       
        for col in head_aoi: 
            merged_aoi.loc[row,col]="%d"%(int(frame_aois.loc[t,col]) )  
                
    else:       
        for col in head_aoi: 
            has_zero= ( is_zero_or_blank( merged_aoi.loc[row,col] ) or is_zero_or_blank(frame_aois.loc[t,col]) )
            if has_zero==True :                          
                merged_aoi.loc[row,col]="%d"%(int(frame_aois.loc[t,col]) )
                     
                #print "true", t, has_zero                
            else:
               # print "overriding attempt ", t, merged_aoi.loc[row,col], frame_aois.loc[t,col], row, col
                continue
            
    merged_aoi.loc[row,"origin_file"]=frame_aois.loc[t,"origin_file"]        
    merged_aoi.loc[row,"count"]+=1
    str_cond=frame_aois.loc[t,"Condition"]
    merged_aoi.loc[row,"Condition"]=str_cond.strip()[0]
    
print "All done with merging the data"    
 
#==============================================================================
# Checking extra counts 
#==============================================================================

for t in range( len(merged_aoi )   ):
    val_count=merged_aoi.loc[t,"count"]
    if val_count>number_of_parts:
        print "Big problem in", t

array_exceeded= np.array(merged_aoi["count"]>number_of_parts, dtype=bool)
error_frame=merged_aoi[array_exceeded]

array_missing= np.array(merged_aoi["count"]<number_of_parts, dtype=bool)

merged_aoi.loc[array_missing,"Condition"]="incomplete"

error_exceed=merged_aoi[array_exceeded]

error_frame=merged_aoi[array_missing]

print "We found ", len(error_frame), " incomplete entries."

fid=open("not_found.dat","w")
s=("%d \n")%len(error_frame)
fid.write(s)
fid.close()

#==============================================================================
#  Error report
#==============================================================================


error_frame.to_csv("merger_error.csv")
error_exceed.to_csv("overcount_error.csv")

    
    
    
    
