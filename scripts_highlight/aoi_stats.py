#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 03:53:54 2017

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
file_input=get_name(line_list,"clean:")

print "Input Name acquired ", file_input

highlight_info=file_input

#==============================================================================
# Output file name
#==============================================================================

file_aoi_out="aoi_stat_csv"

file_aoi_by_ID = 'aoi_by_ID.csv'



#==============================================================================
# Get number of parts
#==============================================================================

number_of_parts=int(get_lines("sources.dat")[0])
print "We have %d parts."%(number_of_parts)

#==============================================================================
# Read the data from the participants file
#==============================================================================
print "Reading data from participants"

data_clean=pd.read_csv(highlight_info, na_filter=False, dtype=str )
size_data=len(data_clean)

highl_index_beg=np.array(data_clean["ind_start"], dtype=int)
highl_index_end=np.array(data_clean["ind_end"], dtype=int)


#==============================================================================
# Read the data from the AOI
#==============================================================================

print "Reading data from AOI"

file_aoi='aoi.csv'
aoi_frame=pd.read_csv(file_aoi, na_filter=False, dtype=str )
tot_aoi=len(aoi_frame)





#==============================================================================
# Check each highlight and find to which AOI it belongs
#==============================================================================

data_clean["aoi"]=[" "]*size_data

t=0
for t in range(size_data):  
     hit_list=[]
     for k in range(tot_aoi):         
         part_aoi= int(aoi_frame.loc[k,"Part"]) 
         part_data=int(data_clean.loc[t,"Part"])
         if part_aoi != part_data : 
            # print "continue ", part_aoi,  part_data, t,k
             continue

         x1=highl_index_beg[t]
         x2=highl_index_end[t]
         y1=int(aoi_frame.loc[k,"ind_start"])
         y2=int(aoi_frame.loc[k,"ind_end"])
         
         no_overlap=(x2<y1 or x1 > y2)  # no overlap
         is_overlap=not no_overlap

         if is_overlap==True:   
             aoi_frame.loc[k,"hit_count"]=int(aoi_frame.loc[k,"hit_count"])+1
            

             hit_list=hit_list +[aoi_frame.loc[k, "ID"]]             
            # print hit_list
             data_clean.loc[t,"aoi"]= " ".join( str(s) for s in hit_list )
     
print "Finished filling up the AOI data." 
data_clean.to_csv(file_aoi_out, columns=["Student ID", "Part" , "aoi", "Text"], index=False)


aoi_frame.to_csv(file_aoi_out, index=False)


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
        cond_letter="unknown"        
    return cond_letter

valid_cond_let={"A", "B"}
dict_web_or_paper={ "website": "website",  "paper" : "paper"  }

#==============================================================================
#  Adding in a Condition by default if missing
#==============================================================================
if ('Condition' in list(data_clean)) == False:
    data_clean["Condition"]=" "

#==============================================================================
#  Adding extra output matrix
#==============================================================================
print "Output statistics by ID"

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
    type_input=data_clean.loc[t,"type"]
    parts_taken.loc[index,dict_web_or_paper[ type_input  ] ]= data_clean.loc[t, "Part"] 

    parts_taken.loc[index,"tot_parts"]= int( int(parts_taken.loc[index,"website"]) > 0  ) + int( int(parts_taken.loc[index,"paper"]) > 0  )

    
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
    
    cond_letter=condition_detect(  int(parts_taken.loc[t,"website"]), "website" )
    parts_taken.loc[t,"Condition_letter"]=cond_letter
    if par_taken_var < number_of_parts :
        print "ID = ", parts_taken.loc[t,"ID"] ," is missing a part of the test." 
        web_part=int(parts_taken.loc[t,"website"])
        paper_part=int(parts_taken.loc[t,"paper"])
        if  web_part >0:
            cond_letter=condition_detect(web_part,"website")
            #website taken
        else:
            cond_letter=condition_detect(paper_part,"paper")
        aoi_results.loc[t,"Condition"]= cond_letter + "  Incomplete"
        parts_taken.loc[t,"Condition_letter"]= cond_letter + "  Incomplete"
        
col_list= ["ID", "Condition"]+[ "AOI_%d"%(t) for t in range(1,tot_aoi+1) ] 
aoi_results.to_csv(file_aoi_by_ID, header=True,columns= col_list, index=False )


 #   parts_taken.loc[index,"Condition"]=cond_letter
    

  #  aoi_results.loc[index,"Condition"]=cond_letter









