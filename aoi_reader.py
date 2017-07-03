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

file_1 = '/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_1.md'
file_2 = '/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_2.md'
highlight_info = '/home/jorge/Downloads/highlights_files/highlights.csv'
#highlight_info = '/home/jorge/Downloads/highlights_files/digital_highlights.csv'

file_out = '/home/jorge/Downloads/highlights_files/output.csv'
file_aoi_out = '/home/jorge/Downloads/highlights_files/aoi_stat.csv'

file_aoi_by_ID = '/home/jorge/Downloads/highlights_files/aoi_by_ID.csv'

input_files=[file_1, file_2]
number_of_parts=len(input_files)
#==============================================================================
# Process input files
# Here we clean up the input files from any extra blank characters 
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
            str=open(filename,'r').read()
        
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return str

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
#file_1_lines = get_lines(file_1)
#file_2_lines = get_lines(file_2)



#file_1_clean=get_clean_text_file(file_1)
#file_2_clean=get_clean_text_file(file_2)

#file_set=[file_1_clean, file_2_clean]  #this string contains the enite text
                                         

#==============================================================================
#  Read AOI (area of interest) file
#==============================================================================


line_tag=["start:", "end:"]
mode_dict={"start": 0, "end": 1}

def line_header_remove(input_line,mode):
    tag = input_line.rsplit()[0]  
    tag_ref=line_tag[mode_dict[mode]]    
    if  tag != tag_ref :
        raise  ValueError('Line has incorrect format at the begining.', "Review %s"%(input_line) )
    temp_line=input_line.rsplit()[1:]  
    joint_line=" ".join(temp_line)
    purged_line=joint_line.strip()    
    return purged_line


def read_aoi(input_file):    
    # this takes the AOI configuration files and returns a dataframe with its contents
    try:
        fid_aoi = open(input_file, 'r')  

        aoi_header_line = fid_aoi.readline() 
        tot_aoi=int(aoi_header_line.rsplit()[0]) #total number of aoi
        aoi_ID=pd.Series( [0]*tot_aoi )
        aoi_part=pd.Series( [0]*tot_aoi )
        aoi_name=pd.Series( [0]*tot_aoi )       
        aoi_start=pd.Series( [0]*tot_aoi )
        aoi_end=pd.Series( [0]*tot_aoi )
        aoi_ind_start=pd.Series( [0]*tot_aoi )
        aoi_ind_end=pd.Series( [0]*tot_aoi )                
        aoi_hitcount=pd.Series( [0]*tot_aoi )
        aoi_text=pd.Series([""]*tot_aoi)
        for t in range(tot_aoi):
            line_blank=fid_aoi.readline()   #ignores line
            
            line_aoi_head=fid_aoi.readline()           
            aoi_head=line_aoi_head.rsplit()            
            aoi_ID[t]=aoi_head[0]
            aoi_part[t]=aoi_head[1]
            aoi_name[t]=aoi_head[2]
            
            line_aoi_beg=fid_aoi.readline()  #begining 
            line_aoi_end=fid_aoi.readline()  #end 
        
            line_aoi_beg=line_header_remove(line_aoi_beg, "start")  #removes the start tag             
            line_aoi_end=line_header_remove(line_aoi_end, "end")  #removes the end tag  
            aoi_start[t]=get_clean_text(line_aoi_beg)
            aoi_end[t]=get_clean_text(line_aoi_end)
                    
            
        fid_aoi.close()
     
        aoi_frame=pd.DataFrame({"ID": aoi_ID, 
                                "Part": aoi_part, 
                                "name": aoi_name, 
                                "start": aoi_start, 
                                "end": aoi_end, 
                                "ind_start": aoi_ind_start, 
                                "ind_end": aoi_ind_end,
                                "text": aoi_text, 
                                "hit_count": aoi_hitcount }) 
    
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "Error reading {0} ".format(input_file)
        raise
        quit()
    except ValueError:
        print "Could not convert data ."
        raise
        quit()     
    return aoi_frame  

def unique_find(str_target,str_text):
    #this will search for a match and make output its uniquenss
    ind_first=str_text.find(str_target)
    ind_last=str_text.rfind(str_target)
    match= (ind_first == ind_last) # true if its a unique fragment
    struct_find=[ind_first,match]
    if ind_first==-1 :
        raise ValueError
    return struct_find

aoi_frame=read_aoi("aoi_template.dat")
tot_aoi=len(aoi_frame["ID"])
print "We have a total of %d AOI \n"%(tot_aoi) 
print aoi_frame["name"]

for t in range(tot_aoi):
    part_num=aoi_frame["Part"][t]
    file_cleaned=" "
    file_cleaned= file_set[part_num-1]    
    str_start=aoi_frame["start"][t]  
        
    try:
        struct_find= unique_find(str_start,file_cleaned) 
    
    except ValueError:
        print "Could not locate AOI ", t+1 , " named ", aoi_frame.loc[t,"name"], " in part ", part_num
        raise    
    
    ind_start=struct_find[0]     
    if (struct_find[1] == False):
        print "Error. The  delimiting words are repeated in the text. Select a longer fragment "
        ind_start=-1
    aoi_frame.loc[t,"ind_start"]=ind_start
    str_end=aoi_frame["end"][t]    
    try:
        ind_end=file_cleaned.index(str_end,ind_start)   
    
    except ValueError:
        print "Could not locate AOI ", t+1 , " named ", aoi_frame.loc[t,"name"], " in part ", part_num
        raise
    
    aoi_frame.loc[t,"ind_end"]=ind_end+len(str_end)-1 #this sets the index at the last letter of the AOI
    aoi_frame.loc[t,"text"]=file_cleaned[aoi_frame.loc[t,"ind_start"]:aoi_frame.loc[t,"ind_end"]+1]



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


data_clean=data_original.copy()

array_isdigit=check_valid(data_clean["Student ID"])
##detect all that do not have valid ID

array_should_drop= np.logical_not(array_isdigit)  #schedule them for elimination
data_clean.drop(data_clean[array_should_drop].index, inplace=True ) # drop the bad rows
data_clean.reset_index(inplace=True)
count_notnum=sum(array_should_drop)

print "Found ", count_notnum, " entries with an invalid ID"

array_inrange=check_int_range(data_clean,"Student ID", 1,sys.maxint)
array_should_drop= np.logical_not(array_inrange)  #schedule them for elimination
data_clean.drop(data_clean[array_should_drop].index, inplace=True ) # drop the bad rows
data_clean.reset_index(inplace=True)
count_notrange=sum(array_should_drop)

print "Found ", count_notrange, " entries wth an ID out of range"



size_data=len(data_clean)
#==============================================================================
# Append column with AOI membership data
#==============================================================================

aoi_belong_series=pd.Series( [ " " ]*size_data )
data_clean["aoi"]=aoi_belong_series


#==============================================================================
# Validate highlights 
#==============================================================================


highl_index_beg=[0]*size_data
highl_index_end=[0]*size_data

t=0  
failure_count=0  #stores the number of highlights that were not located
for t in range(size_data):     
     num_highlights=len(data_clean.loc[t,"Highlight"])     
     high_of_row=get_clean_text(data_clean.loc[t,"Highlight"])
     try:
         usr_id=int(data_clean.loc[t,"Student ID"])          
     
     except ValueError:
         print "Error at ",t,data_clean.loc[t,"Student ID"]
         raise
     
     file_index=np.int(data_clean.loc[t,"Part"])        
     file_cleaned = "" #cleanses the string, for security
     file_cleaned = file_set[file_index-1]
     index= file_cleaned.find(high_of_row)       
     if index == -1 :
         print "Problems in row %d , ID= %d , Highlight '%s' "%(t+1, usr_id ,high_of_row)
         failure_count=failure_count+1
     highl_index_beg[t]=index
     highl_index_end[t]=index+len(high_of_row)-1
   
print "We have %d highlights that were not located "%(failure_count)        
print " \n"


#==============================================================================
# Check each highlight and find to which AOI it belongs
#==============================================================================
#tot_aoi=2
t=0
for t in range(size_data):  
     hit_list=[]
     for k in range(tot_aoi):         
         part_aoi= int(aoi_frame.loc[k,"Part"]) 
         part_data=int(data_clean.loc[t,"Part"])
         if part_aoi != part_data : 
            # print "continue ", part_aoi,  part_data, t,k
             continue
         
             #print "pass"
         #print "after"
         x1=highl_index_beg[t]
         x2=highl_index_end[t]
         y1=int(aoi_frame.loc[k,"ind_start"])
         y2=int(aoi_frame.loc[k,"ind_end"])
         
         no_overlap=(x2<y1 or x1 > y2)  # no overlap
         is_overlap=not no_overlap
        # print x1, x2, y1, y2, "overlap =", is_overlap, " for highlight ", t

         if is_overlap==True:   
             aoi_frame.loc[k,"hit_count"]=int(aoi_frame.loc[k,"hit_count"])+1
            
            # print "Highlight:",data_clean.loc[t,"Highlight"]
            # print "aoi: ",aoi_frame.loc[k,"text"]
            # print "Highlight index beg: ", highl_index_beg[t], "Highlight index end", highl_index_end[t]
            # print " "
             hit_list=hit_list +[aoi_frame.loc[k, "ID"]]             
            # print hit_list
             data_clean.loc[t,"aoi"]= " ".join( str(s) for s in hit_list )
     

data_clean.to_csv(file_out, columns=["Student ID", "Part" , "aoi", "Highlight"])


aoi_frame.to_csv(file_aoi_out)

#==============================================================================
# Detect the type of condition
#==============================================================================

# Condition guide: A= paper part 1, then Website.part 2 

def condition_detect( part_var, web_or_paper ):
    if ((part_var==1) and (web_or_paper=="paper")):
        cond_letter="A"
    elif (part_var==1) and (web_or_paper=="website"):
        cond_letter="B"
    elif (part_var==2) and (web_or_paper=="paper"):
        cond_letter="B"     
    elif (part_var==2) and (web_or_paper=="website"):   
        cond_letter="A"
    else: 
        cond_letter="unkown"        
    return cond_letter

valid_cond_let={"A", "B"}
dict_web_or_paper={ "website": "website", "Web": "website" ,  "Paper": "paper" , "paper" : "paper"  }
#==============================================================================
#  Adding extra output matrix
#==============================================================================

ID_unique_array=list( set( np.array(data_clean["Student ID"], dtype=int) ) )
ID_unique_array.sort()
num_ID_unique= len(ID_unique_array)
series_condition=[" "]*num_ID_unique

aoi_results=pd.DataFrame( { "ID": ID_unique_array , "Condition": [" "]*num_ID_unique } )


dict_ID_to_index={}
pairs_ID_index=zip(ID_unique_array, range(0,num_ID_unique))
for ID, index_ID in pairs_ID_index:
    dict_ID_to_index[ID]=index_ID

aoi_blank_series=pd.Series( [0 ]*num_ID_unique )

parts_taken=pd.DataFrame( {"ID": ID_unique_array,  "Condition_letter": [" "]*num_ID_unique,  
                         "website":  ["0"]*num_ID_unique, "paper": ["0"]*num_ID_unique,
                         "tot_parts": ["0"]*num_ID_unique } ) 
                        
for t in range(0,tot_aoi):
    col_label="AOI_%d"%(t+1)
    aoi_results[col_label]=aoi_blank_series

count_cond_inconsistent=0
for t in range(size_data):
    ID_var=int(data_clean.loc[t,"Student ID"])
    index=dict_ID_to_index[ID_var]
    
    part_var=int(data_clean.loc[t,"Part"])
    cond_input=data_clean.loc[t,"Condition"]
    parts_taken.loc[index,dict_web_or_paper[ cond_input  ] ]= data_clean.loc[t, "Part"] 

    parts_taken.loc[index,"tot_parts"]= int( int(parts_taken.loc[index,"website"]) > 0  ) + int( int(parts_taken.loc[index,"paper"]) > 0  )
    cond_letter=condition_detect(part_var,cond_input) 
    print cond_letter
    parts_taken.loc[index,"Condition"]=cond_letter
    

    aoi_results.loc[index,"Condition"]=cond_letter
    
    hit_str=data_clean.loc[t,"aoi"]
    hit_list=hit_str.split()
    hit_len=len(hit_list)
    for x in hit_list:
        y=int(x)
        if y>tot_aoi:
            continue
        col_name="AOI_%d"%( y )
        aoi_results.loc[index,col_name]= int(aoi_results.loc[index,col_name])+1

for t in range(num_ID_unique):
    par_taken_var=parts_taken.loc[t,"tot_parts"] 
    if par_taken_var < number_of_parts :
        print "ID = ", parts_taken.loc[t,"ID"] ," is missing a part of the test."        
        aoi_results.loc[t,"Condition"]= aoi_results.loc[t,"Condition"] + "  Incomplete"

col_list= ["ID", "Condition"]+[ "AOI_%d"%(t) for t in range(1,tot_aoi+1) ] 
aoi_results.to_csv(file_aoi_by_ID, header=True,columns= col_list )




