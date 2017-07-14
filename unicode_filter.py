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
# Input files 
#==============================================================================


file_input = '/home/jorge/Downloads/highlights_files/full_paper_coding_for_Jorge_1.csv'

#==============================================================================
# Output files
#==============================================================================

file_filtered = '/home/jorge/Downloads/highlights_files/full_paper_coding_for_Jorge_1_ascii.csv'


#==============================================================================
# Here we clean up the input files from any extra blank characters 
#==============================================================================

def get_lines(filename):
    #read a file and returns a list with its lines
    line_list = []
    with open(filename, 'r') as open_file:
        line_list = [line for line in open_file]
    return line_list

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

