#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 05:32:51 2017

@author: jorge
"""

import sys
import os
import errno

import numpy as np
import pandas as pd
#auto plagiarism checker


#==============================================================================
# Error logs
#==============================================================================

file_error_log='error.log'
file_error_csv='error_condition_parag.csv'
file_error_sentences='error_parag.dat'

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
            s="Rows with problems: %d \n"%(num_error_rows)
            fid_error.write(s)
            s="A copy of problematic rows has been stored in: %s \n"%(location)
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
#  Read in lines routines
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
            str_wh=open(filename,'r').read()
        
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return str_wh

def get_clean_text_custom(str_full, delim_custom):
    #clean out any blank characters from input string    
    str_words=str_full.split(delim_custom) #removes any whitespaces and line feeds

    return str_words

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

def write_r(file_out,lines_out):    
    try:
        numpoints=len(lines_out)
        fid_wav = open(file_out, 'w')
        for j in range(0,numpoints):
            s=lines_out[j]
            fid_wav.write(s)
        fid_wav.close()    
        
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "Error reading {0} ".format(file_out)
        raise
        quit()
    except ValueError:
        print "Could not convert data to a number."
        raise
        quit()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
        quit()    
    return 0  

#==============================================================================
# Primary file
#==============================================================================

file_prim='/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_2.md'

#


#==============================================================================
# Secondary file
#==============================================================================


file_sec='/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_2_sentence.md'
file_temp='tempfile.dat'

#==============================================================================
#  Found sentence file
#==============================================================================

def name_sentences_file(file_sec):

    name_extract=os.path.split(file_sec)
    full_name=name_extract[1]
    name_root=os.path.splitext(full_name)[0]
    name_ext=os.path.splitext(full_name)[1]
    
    new_name=name_root+"_list.csv"
    file_sentences=new_name
    return file_sentences


def get_sentences(file_prim,file_sec):

    
    #==============================================================================
    # Get sentences     
    #==============================================================================
    file_sentences=name_sentences_file(file_sec)
    
    #==============================================================================
    #  Process the secondary file
    #==============================================================================
    
    lines_sec=get_lines(file_sec)
    
    #==============================================================================
    #  Replace empty lines with custom delimiter and save to a file
    #==============================================================================
    size_lines_sec=len(lines_sec)
    delim_custom="&&&& "
    k=0
    for t in range(size_lines_sec):
        s=lines_sec[t] 
        if s=="\n":
            k=k+1           
            s_new=delim_custom+"\n"
            lines_sec[t]=s_new
    write_r(file_temp, lines_sec)
    
    
    #==============================================================================
    #  Read in full file and split at custom delimiters
    #==============================================================================
    
    sec_text=read_whole(file_temp)
    list_parag=get_clean_text_custom(sec_text, delim_custom)
    
    #==============================================================================
    # Clean each line
    #==============================================================================
    size_parag=len(list_parag)
    parag_clean=[""]*size_parag
    for t in range(size_parag):
        parag_clean[t]=get_clean_text(list_parag[t])
    
    
    #==============================================================================
    # Load primary file 
    #==============================================================================
    str_prim=get_clean_text_file(file_prim)
    
    
    
    #==============================================================================
    #  Removing white spaces
    #==============================================================================
    
    parag_clean_nowhite=[ ]
    k=0
    for t in range(size_parag):
        s=parag_clean[t]
        if len(s)==0: 
            continue
           
        parag_clean_nowhite.append(parag_clean[t])
        k=k+1
 
    
    size_parag=len(parag_clean_nowhite)
    #==============================================================================
    # Search for matches of secondary inside primary
    #==============================================================================
    
    # verifies the detected setences are within the original text
    matches=[ ]
    k=0
    for t in range(size_parag):
        s=parag_clean_nowhite[t]
        if len(s)==0: 
            continue
        ind=str_prim.find(parag_clean_nowhite[t])
        if ind!=-1:        
            matches.append(parag_clean_nowhite[t])
            k=k+1

    
    num_matches=k
    
    if num_matches!=size_parag:
        print "Some sentences could not be identified within the text"
        raise
    
    ##==============================================================================
    ## Export sentences
    ##==============================================================================
    
    df_out=pd.DataFrame( {"local_index": range(num_matches), 
                          "sentence_text": np.array(matches,dtype=str),
                          "Part": [" "]*num_matches })
    
    df_out.to_csv(file_sentences, index=False)

    return file_sentences