#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:50:40 2017

@author: jorge
"""


import sys
import os
import errno

import numpy as np
import pandas as pd

#==============================================================================
# Input files 
#==============================================================================

aoi_filename="aoi_template.dat"
file_1 = '/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_1.md'
file_2 = '/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_2.md'
highlight_info = '/home/jorge/Downloads/highlights_files/highlights.csv'
#highlight_info = '/home/jorge/Downloads/highlights_files/digital_highlights.csv'

input_files=[file_1, file_2]
number_of_parts=len(input_files)

#==============================================================================
# Output files
#==============================================================================

file_words='/home/jorge/Downloads/highlights_files/words.dat'
file_words_csv='/home/jorge/Downloads/highlights_files/words.csv'

#==============================================================================
# Process input files
# Here we clean up the input files from any extra blank characters 
#==============================================================================

def get_lines(filename):
    #read a file and returns a list with its lines
    line_list = []
    with open(filename, 'r') as open_file:
        line_list = [line for line in open_file]
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

file_lines=[0]*number_of_parts
file_set=[0]*number_of_parts
t=0
for t in range(number_of_parts):
    print t, input_files[t]
    file_lines[t]=get_lines(input_files[t])
    file_set[t]=get_clean_text_file(input_files[t])

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
# Read the data from the participants file
#==============================================================================

data_original=pd.read_csv(highlight_info)
size_data=len(data_original)



#==============================================================================
# Filtering data of participants
#==============================================================================

def check_int_range(inp_array, name_field , low_bound, up_bound):  
    try:
        #returns an elementwise range check for inp_array
        array= np.array(inp_array[name_field] ,dtype=int)
        check_low=(array >= low_bound)
        check_high=(array <= up_bound)
        res_array=np.logical_and(check_low  , check_high )
    except ValueError:
        print "Could not convert data ."         
    return res_array


def check_isnum(inp_array, name_field):
    try:
        #returns an elementwise range check for inp_array
        array_isdig=np.array(inp_array[name_field].str.isdigit(), dtype=bool)          
        res_array=array_isdig
    
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
      #  print "Error reading {0} ".format(input_file)
        raise       
    except ValueError:
        print "Could not convert data ."   
        raise
    return res_array


def check_valid(inp_array):
    array=[False]*len(inp_array)
    for t in range(len(inp_array)):
        temp=inp_array[t]
        
        try:
            res_conv=int(temp)
            res_bool=True  #valid typecast
            
        except ValueError:
            res_bool=False
        array[t]=res_bool    
            
    return array


data_clean=data_original.copy()

array_isdigit=check_valid(data_clean["Student ID"])
##detect all that do not have valid ID

array_should_drop= np.logical_not(array_isdigit)  #schedule them for elimination
data_clean.drop(data_clean[array_should_drop].index, inplace=True ) # drop the bad rows
data_clean.reset_index(inplace=True)
count_notnum=sum(array_should_drop)

print "Found ", count_notnum, " entries with an invalid ID"

array_inrange=check_int_range(data_clean,"Student ID", 1,sys.maxint)
array_should_drop= np.logical_not(array_inrange)  #schedule them for elimination
data_clean.drop(data_clean[array_should_drop].index, inplace=True ) # drop the bad rows
data_clean.reset_index(inplace=True)
count_notrange=sum(array_should_drop)

print "Found ", count_notrange, " entries wth an ID out of range"



size_data=len(data_clean)


#==============================================================================
# Validate highlights 
#==============================================================================


highl_index_beg=[0]*size_data
highl_index_end=[0]*size_data

t=0  
failure_count=0  #stores the number of highlights that were not located
for t in range(size_data):     
     num_highlights=len(data_clean.loc[t,"Highlight"])     
     high_of_row=get_clean_text(data_clean.loc[t,"Highlight"])
     try:
         usr_id=int(data_clean.loc[t,"Student ID"])          
     
     except ValueError:
         print "Error at ",t,data_clean.loc[t,"Student ID"]
         raise
     
     file_index=np.int(data_clean.loc[t,"Part"])        
     file_cleaned = "" #cleanses the string, for security
     file_cleaned = file_set[file_index-1]
     index= file_cleaned.find(high_of_row)       
     if index == -1 :
         print "Problems in row %d , ID= %d , Highlight '%s' "%(t+1, usr_id ,high_of_row)
         failure_count=failure_count+1
     highl_index_beg[t]=index
     highl_index_end[t]=index+len(high_of_row)-1
   
print "We have %d highlights that were not located "%(failure_count)        
print " \n"


#==============================================================================
#  Get the word counts and indices
#==============================================================================
data_clean["word_index"]=["0"]*len(data_clean)
data_clean["word_count"]=["0"]*len(data_clean)

for t in range(size_data):
    str_high=data_clean.loc[t,"Highlight"]
    data_clean.loc[t,"word_count"]=len(str_high.split())    
    prev_string=file_set[ int(data_clean.loc[t, "Part"])-1  ][: highl_index_beg[t]  ]
    #if the highlight is in the middle of a word we must shift it to the beginning of it
    if (len(prev_string) >= 1) and (prev_string[-1] !=" "):
        #looks for the nearest blank space and sets up the beginning on the character right after it 
        ind_corrected=prev_string.rfind(" ")
        str_adjusted=prev_string[: ind_corrected+1  ]
        print ind_corrected,  highl_index_beg[t], str_adjusted[-4:], prev_string[-4:]
    else:
        str_adjusted=prev_string    
    word_index= len(str_adjusted.split())   
    data_clean.loc[t,"word_index"]= word_index
    part_number=int(data_clean.loc[t,"Part"])
    global_index=sum(total_words[:part_number-1])+word_index
    print global_index, word_index
    number_of_words=data_clean.loc[t,"word_count"]
    #marks a hit for every time the word was highlighted
    for k in range(number_of_words):
        words_frame.loc[global_index+k,"hit_count"]=int( words_frame.loc[global_index+k,"hit_count"])+1  
    

words_frame.to_csv(file_words_csv, header=True )


