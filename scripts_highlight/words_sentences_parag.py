#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 07:53:33 2017

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
# Words sentences parag files
#==============================================================================

file_words_csv='words_list.csv'
file_sentence_csv='sentence_list.csv'
file_parag_csv='parag_list.csv'





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

file_set=input_files



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
#  Make dataframe with words from file
#==============================================================================
total_words=[0]*number_of_parts
str_words=file_set[0].split()
index_local= np.array( range( len(str_words )))
words_frame=pd.DataFrame({"words": str_words, 
                        "Part": ["1"]*len(str_words),  
                        "index_local": index_local, 
                        "in_sentence":  [" "]*len(str_words),
                        "in_paragraph":  [" "]*len(str_words) }) 
total_words[0]=len(str_words )

    
for t in range(1,number_of_parts):   
    str_words=file_set[t].split()
    index_local= np.array( range( len(str_words )))
    words_temp=pd.DataFrame({"words": str_words, 
                        "Part": ["%d"%(t+1)]*len(str_words), 
                        "index_local": index_local, 
                        "in_sentence":  [" "]*len(str_words),
                        "in_paragraph":  [" "]*len(str_words) }) 
    words_frame=words_frame.append(words_temp, ignore_index=True)
    total_words[t]=len(str_words )



import sentence_extractor

sent=sentence_extractor.frame_sentence

frame_sentence=pd.read_csv(sentence_extractor.name_file_new[0])
frame_sentence["Part"]="%d"%(1)

for t in range(1,number_of_parts):
    print "File is ", sentence_extractor.name_file_new[t]
    frame_sentence_file=pd.read_csv(sentence_extractor.name_file_new[t])
    frame_sentence_file["Part"]="%d"%(t+1)
    frame_sentence=frame_sentence.append(frame_sentence_file, ignore_index=True)

num_sentences=len(frame_sentence)

#==============================================================================
# Get the sentence index for each word
#==============================================================================

k=0
offset=0
for t in range(num_sentences):
    sentence=frame_sentence.loc[t,"sentence_text"]
    sentence_array=sentence.split()
    len_sent=len(sentence_array)
    words_array=list(words_frame["words"][offset:len_sent+offset])
    #words_np=np.array(words_frame["words"][offset:len_sent+offset],dtype=str)
    
    match=(words_array==sentence_array)
    if match==True:
        words_frame.loc[offset:len_sent+offset,"in_sentence"]="%d"%(k)
        k=k+1
        offset=offset+len_sent
    else:
        print match, "Problem at sentence", t
        print words_array
        print sentence_array 
        raise
print "A total of %d sentences were allocated"%(k)

#==============================================================================
#  Extract the paragraphs
#==============================================================================

import parag_extractor

frame_parag=pd.read_csv(parag_extractor.name_file_new[0])
frame_parag["Part"]="%d"%(1)

for t in range(1,number_of_parts):
    print "File is ", parag_extractor.name_file_new[t]
    frame_parag_file=pd.read_csv(parag_extractor.name_file_new[t])
    frame_parag_file["Part"]="%d"%(t+1)
    frame_parag=frame_parag.append(frame_parag_file, ignore_index=True)

num_parag=len(frame_parag)


#==============================================================================
#  Get the paragraph index for each word
#==============================================================================

k=0
offset=0
for t in range(num_parag):
    parag=frame_parag.loc[t,"sentence_text"]
    parag_array=parag.split()
    len_parag=len(parag_array)
    words_array=list(words_frame["words"][offset:len_parag+offset])
    #words_np=np.array(words_frame["words"][offset:len_sent+offset],dtype=str)
    
    match=(words_array==parag_array)
    if match==True:
        words_frame.loc[offset:len_parag+offset,"in_paragraph"]="%d"%(k)
        k=k+1
        offset=offset+len_parag
    else:
        print match, "Problem at sentence", t
        print words_array
        print parag_array 
        raise
print "A total of %d paragraphs were allocated"%(k)


#==============================================================================
#  Export dataframe with words
#==============================================================================

words_frame.to_csv(file_words_csv, header=True )
frame_sentence.to_csv(file_sentence_csv, header=True )





