#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:50:40 2017

@author: jorge
"""

import pylab
import sys
import os
import errno

import numpy as np
import pandas as pd

print "Begin of color highlighting procedure"

#==============================================================================
# Input files 
#==============================================================================


file_1 = '/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_1.md'
file_2 = '/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_2.md'
highlight_info = '/home/jorge/Downloads/highlights_files/highlights.csv'

file_words_csv='/home/jorge/Downloads/highlights_files/words.csv'


input_files=[file_1, file_2]
number_of_parts=len(input_files)

#==============================================================================
# Output files
#==============================================================================
  #root of output path
#file_color_highlights='/home/jorge/Downloads/highlights_files/'
file_color_highlights="/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/"

#==============================================================================
# Read the data from the word count file
#==============================================================================

data_words=pd.read_csv(file_words_csv)
size_data=len(data_words)



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
p=0
for p in range(number_of_parts):
    print p, input_files[p]
    file_lines[p]=get_lines(input_files[p])
    file_set[p]=get_clean_text_file(input_files[p])


#==============================================================================
#  Get maximum word count
#==============================================================================

words_per_part=[0]*number_of_parts
parts_array=np.array(data_words["Part"], dtype=int)
counts_array=np.array(data_words["hit_count"], dtype=int)
max_counts=max(counts_array)


#==============================================================================
#  Add colormap
#==============================================================================



size_colormap=max_counts


red_array=np.array([0]*size_colormap, dtype=int)
green_array=np.array([0]*size_colormap, dtype=int)
blue_array=np.array([0]*size_colormap, dtype=int)

python_cmap=pylab.cm.get_cmap("jet",size_colormap)

for t in range(python_cmap.N):
    red_array[t]=int(python_cmap(t)[0]*255)    
    green_array[t]=int(python_cmap(t)[1]*255  ) 
    blue_array[t]=int(python_cmap(t)[2]*255)   

    
 
#==============================================================================
#  Produce highlighted text
#==============================================================================




for p in range(number_of_parts):
    words_per_part[p]=sum(parts_array==p+1)

number_of_parts=2
for p in range(number_of_parts):
    if p==0 :
        word_index=0
    else:
        word_index=sum(words_per_part[:p])
  
    lines=file_lines[p]
    lines_out=lines
    num_lines=len(lines)
    for l in range(num_lines):
        line_l=lines[l]
        char_index=0
        word_array=line_l.split()        
        if len(word_array) >= 1 :
            for t in range(len( word_array)):
                word=word_array[t]                
                if data_words.loc[word_index,"words"]!=word :
                    print (data_words.loc[word_index,"words"]==word), data_words.loc[word_index,"words"] , word
                count=data_words.loc[word_index,"hit_count"]
                
                if count >0:                    
                    red=red_array[count-1]
                    green=green_array[count-1]
                    blue=blue_array[count-1]                      
                   # print red, green, blue
                    word_new='<span style="background-color: #%02.0X%02.0X%02.0X; color: #FFFFFF " > '%(red,green,blue)+ word+ ' </span >'
                  #  print word_new
                else:
                    word_new=word
                word_array[t]=word_new
                word_index=word_index+1
        line_rebuilt=" ".join(word_array)
        lines_out[l]=line_rebuilt
      #  print line_rebuilt, line_l     
    filename=file_color_highlights+"file_color_%d.md"%(p+1)    
    fid_highlight = open(filename, 'w')
    for l in range(num_lines):
        s=lines_out[l]+"\n"
        fid_highlight.write(s)
    fid_highlight.close()    
        
print "Finished"    
                