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

file_blank="blank.csv"

#==============================================================================
# Error logs
#==============================================================================

file_error_log='error.log'
file_error_csv='error_not_in_text.csv'


def write_error(filename,frame,motive, location):
    # reads a file and reaturns its contents as a string
        file_inp=filename
        try:
            num_error_rows=len(frame)
            if num_error_rows==0:
                return 0  #no error to output
            fid_error=open(filename,'a')      
            s="Error found \n"
            fid_error.write(s)
            s="Motive: %s \n"%(motive)
            fid_error.write(s)
            s="Rows discarded: %d \n"%(num_error_rows)
            fid_error.write(s)
            s="A copy of deleted rows has been stored in: %s \n"%(location)
            fid_error.write(s)
            s=" \n \n"
            fid_error.write(s)
            fid_error.close()
            
            
        except ValueError:
            print "Error writing to %s"%(filename)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return 0



#==============================================================================
# Words files
#==============================================================================

file_words='words.dat'
file_words_csv='words.csv'

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

def unique_find(str_target,str_text):
    #this will search for a match and make output its uniquenss
    #the code will search for the fragment from the left and from the right. If its unique the positions will be the same
    ind_first=str_text.find(str_target)
    ind_last=str_text.rfind(str_target)
    match= (ind_first == ind_last) # true if its a unique fragment
    struct_find=[ind_first,match]
    if ind_first==-1 :
        raise ValueError
    return match



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
array_blank=np.array([False]*size_data ,dtype=bool)
array_duplicate=np.array([False]*size_data ,dtype=bool)

t=0  
failure_count=0  #stores the number of highlights that were not located
for t in range(size_data):     
     #print "Checking row", t        
     high_of_row=get_clean_text(data_orig.loc[t,"Text"])
     try:
         usr_id=int(data_orig.loc[t,"Participant"])          
     
     except ValueError:
         print "Error at ",t,data_orig.loc[t,"Participant"]
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
         if len(high_of_row)==0: 
             # the highlight is blank             
             array_blank[t]=True
             data_orig.loc[t,"blank?"]="%d"%(1)   
             #ensure the fragment does not appear multiple times
         try:
            
             is_unique = unique_find(high_of_row,file_cleaned) 
             if is_unique== False:
                 #duplicate is present
                 array_duplicate[t]=True 
                 print "Duplicate in row ", t+1, " with text ", high_of_row
         except ValueError:
             print "Error looking for duplicate in row ", t+1 , " with text ", high_of_row
             
            
             
             
     highl_index_beg[t]=index
     highl_index_end[t]=index+len(high_of_row)-1
     data_orig.loc[t,"ind_start"]=highl_index_beg[t]
     data_orig.loc[t,"ind_end"]=highl_index_end[t]
    
    
    
print "We have %d highlights that were not located "%(failure_count)   

duplicate_count=sum(array_duplicate)
print "We have %d duplicates "%(duplicate_count)

print "Problematic rows will be dropped"     
print " \n"

#==============================================================================
# Export the blank entries
#==============================================================================
     

df_blank=data_orig[array_blank]
df_blank.to_csv(file_blank)    



#==============================================================================
#  Getting rid of bad text selections 
#==============================================================================
motive=" the selected text could not be located within the source files."
array_should_drop= np.logical_not(valid_highlights)  #schedule them for elimination

#copy bad rows and report error
df_bad=data_orig[array_should_drop]
if len(df_bad)>0:
    df_bad.to_csv(file_error_csv, header=True, index=True)
    write_error(file_error_log,df_bad,motive,file_error_csv)


data_clean=data_orig.drop(data_orig[array_should_drop].index ) # drop the bad rows
data_clean.reset_index(drop=True, inplace=True)     

print "Eliminated problem rows"


#==============================================================================
#  Make dataframe with words from file
#==============================================================================
total_words=[0]*number_of_parts
str_words=file_set[0].split()
index_local= np.array( range( len(str_words )))
words_frame=pd.DataFrame({"words": str_words, 
                        "Part": ["1"]*len(str_words),  
                        "index_local": index_local,
                        "hit_count": ["%d"%(0)]*len(str_words) }) 
total_words[0]=len(str_words )

    
for t in range(1,number_of_parts):   
    str_words=file_set[t].split()
    index_local= np.array( range( len(str_words )))
    words_temp=pd.DataFrame({"words": str_words, 
                        "Part": ["%d"%(t+1)]*len(str_words), 
                        "index_local": index_local,
                        "hit_count": ["%d"%(0)]*len(str_words) }) 
    words_frame=words_frame.append(words_temp, ignore_index=True)
    total_words[t]=len(str_words )




#==============================================================================
#  Get the word counts and indices
#==============================================================================
size_data=len(data_clean)
data_clean["word_index"]=["0"]*len(data_clean)
data_clean["word_count"]=["0"]*len(data_clean)

highl_index_beg=np.array(data_clean["ind_start"],dtype=int)
highl_index_end=np.array(data_clean["ind_end"],dtype=int)


for t in range(size_data):
    str_high=data_clean.loc[t,"Text"]
    data_clean.loc[t,"word_count"]=len(str_high.split())    
    prev_string=file_set[ int(data_clean.loc[t, "Part"])-1  ][: highl_index_beg[t]  ]
    #if the highlight is in the middle of a word we must shift it to the beginning of it
    if (len(prev_string) >= 1) and (prev_string[-1] !=" "):
        #looks for the nearest blank space and sets up the beginning on the character right after it 
        ind_corrected=prev_string.rfind(" ")
        str_adjusted=prev_string[: ind_corrected+1  ]
       # print ind_corrected,  highl_index_beg[t], str_adjusted[-4:], prev_string[-4:]
    else:
        str_adjusted=prev_string    
    word_index= len(str_adjusted.split())   
    data_clean.loc[t,"word_index"]= word_index
    part_number=int(data_clean.loc[t,"Part"])
    global_index=sum(total_words[:part_number-1])+word_index
   # print global_index, word_index
    number_of_words=data_clean.loc[t,"word_count"]
    #marks a hit for every time the word was highlighted
    for k in range(number_of_words):
        words_frame.loc[global_index+k,"hit_count"]=int( words_frame.loc[global_index+k,"hit_count"])+1  
    

words_frame.to_csv(file_words_csv, header=True )



#==============================================================================
# Add column with indicator for beginning of user
#==============================================================================
data_clean["1 to start"]=np.array( [" "]*len(data_clean), dtype=str )

old_entry=data_clean.loc[0,"Participant"]
data_clean.loc[0,"1 to start"]=1
for t in range(1, len( data_clean ) ):    
    new_entry=data_clean.loc[t,"Participant"]
    if new_entry!= old_entry:
        data_clean.loc[t,"1 to start"]=1
        old_entry=new_entry

#==============================================================================
# Save output
#==============================================================================

data_clean.to_csv(file_out, header=True , index=False)

print "Finished outputting cleaned highlights"



