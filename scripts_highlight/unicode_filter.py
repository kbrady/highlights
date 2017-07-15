#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:50:40 2017

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
file_input=get_name(line_list,"original:")

print "Input Name acquired ", file_input


#==============================================================================
# Output file name
#==============================================================================

file_filtered=get_name(line_list,"ascii:")

print "Output Name acquired ", file_filtered

#==============================================================================
# Here we clean up the input files from any extra blank characters 
#==============================================================================


line_list=get_lines(file_input)

size_data=len(line_list)

#==============================================================================
# Eliminate non ASCII
#==============================================================================
print "Eliminating non-ASCII"

data_clean=[""]*size_data

for t in range(size_data):
    s=line_list[t]
    s_unicode=s.decode('ascii', errors='ignore')
    s_ascii=s_unicode.encode('ascii')
    data_clean[t]=s_ascii

#==============================================================================
#  Output the cleaned file
#==============================================================================
fid_out=open(file_filtered,'w')
for t in range(size_data):
    fid_out.write(data_clean[t])
fid_out.close()    

print "Finished cleaning up non-ASCII characters"