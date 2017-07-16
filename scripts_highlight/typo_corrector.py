#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 18:14:45 2017

@author: jorge
"""

import csv
from collections import namedtuple

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
    try:
        line_list = []
        with open(filename, 'r') as open_file:
            line_list = [line for line in open_file]
    
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "Error reading {0} ".format(filename)
        raise
        quit()       
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

def write_whole(filename, content_str):
        file_inp=filename
        try:
            fid_out=open(filename,'w')
            fid_out.write(content_str)
            fid_out.close()
        
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return 0
   

#==============================================================================
#  Get input file name
#==============================================================================

file_names='names.dat'


line_list=get_lines(file_names)
file_input=get_name(line_list,"standard:")

print "Input Name acquired ", file_input


#==============================================================================
# Output file name
#==============================================================================

file_output=get_name(line_list,"spell_corrected:")

print "Output Name acquired ", file_output


#==============================================================================
# Load input file contents
#==============================================================================

input_str=read_whole(file_input)


#==============================================================================
#  Get spelling correction list
#==============================================================================
file_spelling='spelling.dat'

def load_correction_list(filename):
    # reads a file and reaturns its contents as a string    
    try:
        line_list = []
        with open(filename, 'r') as open_file:
            line_list = [line for line in open_file]
    except ValueError:
        print "Did not load %d properly"%(filename)
    
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "Did not find {0} ".format(filename)
        print "Skipping spell correction."
    return line_list

correction_list=load_correction_list(file_spelling)

number_of_corrections=len(correction_list)

def verify_delim(str_test, delim):
    try:
        beg=(str_test[0]==delim)
        ending=(str_test[-1]==delim)
        if beg==False or ending==False:
            raise ValueError
    
    except ValueError:
        print "The delimiter character %s could not be detected in %s"%(delim, str_test)
        raise        
    return True

def find_text(arr_line,num):
    #this will go through each line and return the nth nonblank string
    len_list=len(arr_line)    
    k=0
    for t in range(len_list):
        s=arr_line[t]
        ss=s.split()        
        len_elem=len(ss)
        #print "ss ",ss, "  s=", s, " t= ",t, " len_elem= ", len_elem
        if len_elem>0:
            k=k+1            
            #count a valid string
            if k==num:  #if its the match return
                return arr_line[t]    
        
    return " "

def correction_used(str_correction, old):
    #determines if a correction is actually needed
    try:
        str_correction.index(old)
    
    except ValueError:    
        print "Could not find '%s'"%(old)
        print "Correction not needed"
        return False
    return True

#==============================================================================
# 
#==============================================================================

delim="'"
skipped=0
not_needed=0
for t in range(number_of_corrections):
    
    line=correction_list[t].split(delim)
    if len( line )<2 :
        print "skipping correction #", t+1
        skipped=skipped+1
        continue
    print "Making correction %d of %d"%(t+1, number_of_corrections)
    old=find_text(line,1)    
    correction=find_text(line,2)
    
    used=correction_used(input_str,old)
    if used==False:
        not_needed=not_needed+1
    print "Replacing %s%s%s for %s%s%s"%(delim,old,delim,  delim, correction, delim)    
    
    input_str=input_str.replace(old, correction)
print "Skipped ", skipped, " corrections "
print "Unneccesary corrections : ", not_needed    
write_whole(file_output,input_str)    






    
    
    

