#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 02:39:00 2017

@author: jorge
"""
import pandas as pd
import sentence_funct

# gets the sentences declared in a file, assigns them a number and outputs


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

source_files=input_files

#==============================================================================
# Sentence source files 
#==============================================================================

file_sources='sources_sentence.dat'
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

source_sentence_files=input_files

#==============================================================================
# Primary
#==============================================================================
name_file_new=[0]*number_of_parts
for t in range(number_of_parts):
    prim=source_files[t]
    sec=source_sentence_files[t]
    name_file_new[t]=sentence_funct.get_sentences(prim,sec)
    print "Finished extracting sentences for ", sec
    

frame_sentence=pd.read_csv(name_file_new[0])
frame_sentence["Part"]="%d"%(1)
num_sentences_base=len(frame_sentence)
for t in range(1,number_of_parts):
    print "File is ", name_file_new[t]
    frame_temp=pd.read_csv(name_file_new[t])    
    frame_temp["Part"]="%d"%(t+1)
    frame_sentence=frame_sentence.append(frame_temp, ignore_index=True)
       

    