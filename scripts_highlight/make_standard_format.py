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

import time

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
# Error logs
#==============================================================================

#general log file
file_error_log='error.log'

#specific error log files
file_error_ID='error_badID.csv'
file_error_part='error_part.csv'
file_error_an='error_part.csv'
file_error_type='error_type_test.csv'

set_error_names=[file_error_ID, file_error_part, file_error_an, file_error_type ]

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

def initialize_error(filename):
    # reads a file and reaturns its contents as a string
        file_inp=filename
        try:
            now = time.strftime('%c')
            fid_error=open(filename,'w')           
            s="Error log file created on %s \n \n"%(now)           
            fid_error.write(s)
            fid_error.close()
            
            
        except ValueError:
            print "Error writing to %s"%(filename)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return 0

def initialize_blank(filename):
    # reads a file and reaturns its contents as a string
        file_inp=filename
        try:            
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

initialize_error(file_error_log)

for file_name_err in set_error_names:
    initialize_blank(file_name_err)



#==============================================================================
# Read the data from the participants file
#==============================================================================

data_original=pd.read_csv(file_input, na_filter=False, dtype=str)
size_data=len(data_original)

#==============================================================================
#  Get column names
#==============================================================================

file_cols=list(data_original.columns.values)


#==============================================================================
# Name changes for some columns
#==============================================================================

if "Participant" in list(data_original):
    print "Renaming %s to %s"%("Participant", "Participant")
    ddata_original=data_original.rename(columns={'Participant':'Participant'})

if ("Section" in list(data_original))==True:
    print "Renaming %s to %s"%("section", "Part")
    data_original=data_original.rename(columns={'Section':'Part'})

file_cols=list(data_original.columns.values) #update column names

#==============================================================================
# Enforce required columns
#==============================================================================


req_cols=["Participant", "Part", "Text"]

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
    data_original["type"]= [type_from_file]*len(data_original)
    print "Added condition '%s' from file"%(type_from_file)


#==============================================================================
#  Adding in columns with annotate 
#==============================================================================

if ('annotate' in list(data_original)) == False :
    data_original["annotate"]=["0"]*len(data_original)
    data_original["note"]=[" "]*len(data_original)
    print "Added 'annotate' and 'note' column."

data_original["annotate"]=np.array(data_original["annotate"], dtype=int)
#==============================================================================
#  Adding in columns with highlight
#==============================================================================

if ('highlight' in list(data_original)) == False :
    data_original["highlight"]=["1"]*len(data_original)
    print "Added 'highlight' column."

data_original["highlight"]=np.array(data_original["highlight"], dtype=int)


#==============================================================================
#  Adding note in blank
#==============================================================================
if ('note' in list(data_original)) == False :
    data_original["note"]=["1"]*len(data_original)
    #initialize the empty strings to a blank value
for t in range(len(data_original)):
    s=data_original.loc[t,"note"]
    if s=="" :        
        data_original.loc[t,"note"]="  "


#==============================================================================
#  Adding in columns with index for beginning and end
#==============================================================================

if ('ind_start' in list(data_original)) == False :
    data_original["ind_start"]=["0"]*len(data_original)
    print "Added 'beg' column."

if ('ind_end' in list(data_original)) == False :
    data_original["ind_end"]=["0"]*len(data_original)
    print "Added 'end' column."



#==============================================================================
#  Adding in columns with belonging counts
#==============================================================================



dict_len_high={"word": 1, "phrase":   2, "sentence": 3,  "sentence + phrase": 4, "paragraph": 5, "multiple_paragraphs": 6 }
dict_len_high_inv={1: "word", 2: "phrase", 3: "sentence",4:   "sentence + phrase", 5: "paragraph", 6: "multiple_paragraphs" }

for name_of_col in dict_len_high:
    if (name_of_col in list(data_original)) == False :
        data_original[name_of_col]=np.array(["0"]*len(data_original), dtype=str)
        print "Adding ", name_of_col  


#==============================================================================
#  Adding in columns for 
#==============================================================================

if ('blank?' in list(data_original)) == False :
    data_original["blank?"]=["0"]*len(data_original)
    print "Added blank? column."




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
       # print "Error reading {0} ".format(input_file)
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

array_isdigit=check_valid(data_cop["Participant"])
##detect all that do not have valid ID

array_should_drop= np.logical_not(array_isdigit)  #schedule them for elimination

#copy bad rows and report error
motive=" ID is invalid "
file_error_csv=file_error_ID
df_bad=data_cop[array_should_drop]
if len(df_bad)>0:
    df_bad.to_csv(file_error_csv, header=True, index=True)
    write_error(file_error_log,df_bad,motive,file_error_csv)


data_valid_int=data_cop.drop(data_cop[array_should_drop].index ) # drop the bad rows

count_notnum=sum(array_should_drop)

print "Found ", count_notnum, " entries with an invalid ID"

array_inrange=check_int_range(data_valid_int,"Participant", 1,sys.maxint)
array_should_drop= np.logical_not(array_inrange)  #schedule them for elimination
data_valid_ID=data_valid_int.drop(data_valid_int[array_should_drop].index ) # drop the bad rows

data_valid_ID=data_valid_ID.reset_index(drop=True)
count_notrange=sum(array_should_drop)

print "Found ", count_notrange, " entries wth an ID out of range"

size_data=len(data_valid_ID)




#==============================================================================
#  Validate part number
#==============================================================================

array_part_inrange=check_int_range(data_valid_ID,"Part",1,2)
if any(np.logical_not(array_part_inrange) ) == True :
    print "We have a Part number that is out of bounds."
    #print "Stopping"
    


array_should_drop= np.logical_not(array_part_inrange)  #schedule them for elimination

#copy bad rows and report error
motive=" Part number is not valid "
file_error_csv=file_error_part
df_bad=data_valid_ID[array_should_drop]
if len(df_bad)>0:
    df_bad.to_csv(file_error_csv, header=True, index=True)
    write_error(file_error_log,df_bad,motive,file_error_csv)



sum_badparts=sum(array_should_drop)


data_valid_part=data_valid_ID.drop(data_valid_ID[array_should_drop].index ) # drop the bad rows
data_valid_part.reset_index(drop=True, inplace=True)  

print "Found ", sum_badparts, " entries wth a bad part number"

#==============================================================================
# Validate annotation and highlight indicators
#=============================================================================

array_inrange_annot=check_int_range(data_valid_part,"annotate", 0,1)
array_inrange_high=check_int_range(data_valid_part,"highlight", 0,1)
array_inrange_annot_high=np.logical_and( array_inrange_annot , array_inrange_high )

array_should_drop= np.logical_not(array_inrange_annot_high)  #schedule them for elimination

#copy bad rows and report error
motive=" Annotation or highlight flags are invalid "
file_error_csv=file_error_an
df_bad=data_valid_part[array_should_drop]
if len(df_bad)>0:
    df_bad.to_csv(file_error_csv, header=True, index=True)
    write_error(file_error_log,df_bad,motive,file_error_csv)



data_valid_annot=data_valid_part.drop(data_valid_part[array_should_drop].index ) # drop the bad rows

data_valid_annot.reset_index(drop=True, inplace=True)  
count_not_annot=sum(array_should_drop)

print "Found ", count_not_annot, " entries wth a bad flag for highlight or indicator"

size_data=len(data_valid_annot)




#==============================================================================
#  Validate type of test
#==============================================================================
dict_web_or_paper={ "website": "website", "Web": "website" ,  "Paper": "paper" , "paper" : "paper"  }


array_valid_type=np.array( [0]*size_data ,dtype=bool)
for t in range(size_data):
    type_test=data_valid_annot.loc[t,"type"]
    val=(type_test in dict_web_or_paper)
    if val== False:
        array_valid_type[t]=False
        
    else:
        array_valid_type[t]=True
        data_valid_annot.loc[t,"type"]=dict_web_or_paper[type_test] #makes writting uniform
        
        
array_should_drop= np.logical_not(array_valid_type)  #schedule them for elimination

#copy bad rows and report error
motive=" Invalid type of test. Must be website or paper. "
file_error_csv=file_error_type
df_bad=data_valid_annot[array_should_drop]
if len(df_bad)>0:
    df_bad.to_csv(file_error_csv, header=True, index=True)
    write_error(file_error_log,df_bad,motive,file_error_csv)

data_valid_type=data_valid_annot.drop(data_valid_annot[array_should_drop].index ) # drop the bad rows

data_valid_type.reset_index(drop=True, inplace=True)        
        
data_clean=data_valid_type
print "Finished cleanup"

#==============================================================================
# Add column with indicator for beginning of user
#==============================================================================
data_clean["1 to start"]=np.array( [" "]*len(data_clean), dtype=str )

old_entry=data_clean.loc[0,"Participant"]
data_clean.loc[0,"1 to start"]=1
for t in range(1, len( data_clean ) ):    
    new_entry=data_clean.loc[t,"Participant"]
    if new_entry!= old_entry:
        data_clean.loc[t,"1 to start"]=1
        old_entry=new_entry



#==============================================================================
# Output corrected csv
#==============================================================================


data_clean.to_csv(file_output, header=True, index=False )



