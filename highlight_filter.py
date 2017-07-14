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


highlight_info = '/home/jorge/Downloads/highlights_files/full_paper_coding_for_Jorge_1_corrected.csv'

#==============================================================================
# Output files
#==============================================================================

file_out = '/home/jorge/Downloads/highlights_files/full_paper_coding_for_Jorge_1_corrected_noanot.csv'



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
        print "Error reading {0} ".format(input_file)
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


data_cop=data_original.copy()



size_data=len(data_cop)

#==============================================================================
#  Drop the lines that do not have a highlight
#==============================================================================
print "Getting rid of non-highlighted rows"
highlight_boolean=np.array(data_cop["highlight"], dtype=bool)

array_should_drop= np.logical_not(highlight_boolean)  #schedule them for elimination
data_new=data_cop.drop(data_cop[array_should_drop].index ) # drop the bad rows
#data_clean.reset_index(inplace=True)
count_nohighlight=sum(array_should_drop)

print "Finished cleanup"
#==============================================================================
# Output corrected csv
#==============================================================================

#col_list= ["ID", "Condition"]+[ "AOI_%d"%(t) for t in range(1,tot_aoi+1) ] 
data_new.to_csv(file_out, header=True )



