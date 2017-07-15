#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 10:24:13 2017

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
#  Get input file name
#==============================================================================

file_names='names.dat'


line_list=get_lines(file_names)
file_input=get_name(line_list,"ascii:")

print "Input Name acquired ", file_input


#==============================================================================
# Output file name
#==============================================================================

file_output=get_name(line_list,"standard:")

print "Output Name acquired ", file_output

#==============================================================================
# Read the data from the participants file
#==============================================================================

data_original=pd.read_csv(file_input)
size_data=len(data_original)

#==============================================================================
#  Get column names
#==============================================================================

file_cols=list(data_original.columns.values)


#==============================================================================
# Name changes for some columns
#==============================================================================

if "Participant" in list(data_original):
    print "Renaming %s to %s"%("Participant", "Student ID")
    ddata_original=data_original.rename(columns={'Participant':'Student ID'})

if ("Section" in list(data_original))==True:
    print "Renaming %s to %s"%("section", "Part")
    data_original=data_original.rename(columns={'Section':'Part'})

file_cols=list(data_original.columns.values) #update column names

#==============================================================================
# Enforce required columns
#==============================================================================


req_cols=["Student ID", "Part", "Text"]

try:

    for col in req_cols:
        if (col in file_cols)== False:
            print col , " not in file and its a required column. "
            raise ValueError

except ValueError:
    print "Stopping script."
    print "Fix the column names to include the required ones"
    raise

dict_format_conv={"Student ID": "Participant", "part": "Part", "Part": "Part", "Highlight": "Text" }



#==============================================================================
#  Adding in a Condition by default if missing
#==============================================================================

if "Condition" in list(data_original):
    data_original.rename(columns={'Condition':'type'})

if "condition" in list(data_original):
    data_original.rename(columns={'condition':'type'})

file_condition="type.dat"
line=get_lines(file_condition)
type_from_file=line[0].rsplit()[0]

if ('type' in list(data_original)) == False :
    data_original["type"]=type_from_file
    print "Added condition '%s' from file"%(type_from_file)


#==============================================================================
#  Adding in columns with annotate 
#==============================================================================

if ('annotate' in list(data_original)) == False :
    data_original["annotate"]="0"
    data_original["note"]=" "
    print "Added 'annotate' and 'note' column."

#==============================================================================
#  Adding in columns with highlight
#==============================================================================

if ('highlight' in list(data_original)) == False :
    data_original["highlight"]="1"
    print "Added 'highlight' column."



#==============================================================================
# Routines for validating the ID
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


#==============================================================================
# Get rind of invalid ID
#==============================================================================
data_cop=data_original.copy()

size_data=len(data_cop)

data_cop=data_original.copy()

array_isdigit=check_valid(data_cop["Student ID"])
##detect all that do not have valid ID

array_should_drop= np.logical_not(array_isdigit)  #schedule them for elimination
data_valid_int=data_cop.drop(data_cop[array_should_drop].index ) # drop the bad rows

count_notnum=sum(array_should_drop)

print "Found ", count_notnum, " entries with an invalid ID"

array_inrange=check_int_range(data_valid_int,"Student ID", 1,sys.maxint)
array_should_drop= np.logical_not(array_inrange)  #schedule them for elimination
data_valid_ID=data_valid_int.drop(data_valid_int[array_should_drop].index ) # drop the bad rows

count_notrange=sum(array_should_drop)

print "Found ", count_notrange, " entries wth an ID out of range"

size_data=len(data_valid_ID)

data_clean=data_valid_ID
print "Finished cleanup"


#==============================================================================
#  Validate part number
#==============================================================================

array_part_inrange=check_int_range(data_clean,"Part",1,2)
if any(np.logical_not(array_part_inrange) ) == True :
    print "We have a Part number that is out of bounds."
    print "Stopping"
    raise

#==============================================================================
# Output corrected csv
#==============================================================================

#col_list= ["ID", "Condition"]+[ "AOI_%d"%(t) for t in range(1,tot_aoi+1) ] 
data_clean.to_csv(file_output, header=True )



