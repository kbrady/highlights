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

import time
#==============================================================================
# Error log for typos
#==============================================================================

#general log file
file_error_log='error.log'

file_error_spelling='error_spelling.csv'
file_spelling_log='error_spelling.dat'

def write_error_text(filename, motive, location):    
        file_inp=filename
        try:
            fid_error=open(filename,'a')    
            s="Applying correction # %d  \n"%(location+1)
            fid_error.write(s)
            s="Action: %s \n"%(motive)
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

def initialize_error(filename):    
        file_inp=filename
        try:
            now = time.strftime('%c')
            fid_error=open(filename,'w')           
            s=""          
            fid_error.write(s)
            fid_error.close()
            
            
        except ValueError:
            print "Error writing to %s"%(filename)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return 0


def write_error(filename,motive, location):
    # reads a file and reaturns its contents as a string
        file_inp=filename
        try:

            fid_error=open(filename,'a')    
            s="Error found \n"
            fid_error.write(s)
            s="Motive: %s \n"%(motive)
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


initialize_error(file_spelling_log)



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
copy_input=input_str
delim="'"
skipped=0
not_needed=0
num_corrected=0
for t in range(number_of_corrections):
    
    line=correction_list[t].split(delim)
    if len( line )<2 :
        print "skipping correction #", t+1
        skipped=skipped+1
        continue
    print "Making correction %d of %d"%(t+1, number_of_corrections)
    old=find_text(line,1)    
    correction=find_text(line,2)
    
    used=correction_used(copy_input,old)
    if used==False:
        not_needed=not_needed+1
        action_str="No action because the correction is not neded."
        write_error_text(file_spelling_log, action_str,t)
    else:     
        print "Replacing %s%s%s for %s%s%s"%(delim,old,delim,  delim, correction, delim)    
        num_corrected=num_corrected+1
        copy_input=copy_input.replace(old, correction)
        action_str="Replaced %s%s%s for %s%s%s"%(delim,old,delim,  delim, correction, delim)  
        write_error_text(file_spelling_log, action_str,t)
    
    
print "Skipped ", skipped, " corrections that could not be read from file"
print "Unneccesary corrections : ", not_needed  
print "Total corrections = ", num_corrected
  
write_whole(file_output,copy_input)    
if num_corrected > 0:
    motive="A total of %d typos were corrected. See %s"%(num_corrected, file_spelling_log)
    write_error(file_error_log,motive,0)










    
    
    

