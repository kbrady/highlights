#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:07:49 2017

@author: jorge
"""

# regenerate the digital highlight csv file

import re
import numpy as np
import sys 
import pandas as pd
import os




# =============================================================================
#  Routines
# =============================================================================


def get_lines(filename):
    #read a file and returns a list with its lines
    line_list = []
    with open(filename, 'r') as open_file:
        line_list = [line for line in open_file]
    return line_list

#def clean_df(df_dirty, df_blank,col_clean):
#    df_clean=df_blank.copy()
#    df_clean_final=pd.DataFrame({})
#    for k in range(len(df_dirty)):
#        for col in df_dirty.columns.values:
#            if col in col_clean:
#                df_clean.loc[0,col]= int( df_dirty.loc[ df_dirty.index[k], col   ])
#            else: 
#                df_clean.loc[0,col]= df_dirty.loc[ df_dirty.index[k], col   ]
#        df_clean_final.append(df_clean)
#    return df_clean_final


file_list_mine="/home/jorge/Downloads/mass_down/consolidated/ID_list_digital.dat"

file_digital_highlights="/home/jorge/Downloads/highlights_files/file_digital/digital_highlights_final_withadditions_updated_corrected.csv"


data_file=pd.read_csv(file_digital_highlights, na_filter=False, dtype=str )
size_data=len(data_file)

dig_usr=np.array( data_file["Participant"], dtype=int ) 
dig_part=np.array( data_file["Part"], dtype=int ) 
dig_text=np.array( data_file["Text"], dtype=str )
dig_note=np.array( data_file["Note"], dtype=str )
data_orig=pd.DataFrame( { "Participant": dig_usr,
                             "Part": dig_part,
                             "Text": dig_text,
                             "Note": dig_note }   )
 
    
# =============================================================================
# Substitute for correct ID    
# =============================================================================

def replace_IDs(data_or ):    
    import import_investigation 
    old_id=list(np.array( import_investigation.df_problem["Redcap_id"], dtype=int ) )
    new_id=list(np.array( import_investigation.df_problem["highlights_id"] ,  dtype=int   )  )
    
    dict_ID_change={}
    pairs_ID_index=zip(old_id, new_id)
    for old, new in pairs_ID_index:
        dict_ID_change[old]=new
    
    count_ex=0
    count_rep=0
    for t in data_or.index:
        try:
            newval= dict_ID_change[ data_or.loc[t,"Participant"] ] 
            count_rep+=1
        except KeyError:
            newval=data_or.loc[t,"Participant"]
          #  print "Except ", t
            count_ex+=1
        data_or.loc[t,"Participant"]=newval
    print "count ex", count_ex   , count_rep, len(data_or) 
    return data_or 

# =============================================================================
#  Retrieve master list
# =============================================================================

def get_master_list( ):
    import import_investigation 
    master_list=import_investigation.highlights_id
    
    return master_list

master_list=get_master_list()

def get_list_parts():
    import import_investigation
    list_parts=import_investigation.list_parts
    return list_parts

# =============================================================================
# 
# =============================================================================


participant_digital_orig=np.array( data_orig["Participant"], dtype=int)

participant_digital=list( set( list(participant_digital_orig)) )

participant_digital.sort()

# get the dowloaded Participant ID

lines=get_lines(file_list_mine)
num_entries=int(lines[0])

list_ID_download=[]
list_parts=[]
for t in range(1,num_entries+1):
    arr_line=lines[t].split()
    list_ID_download.append( int( arr_line[1] ) )
    list_parts.append(  int(arr_line[2][0])  )

# find the items downloaded but not in the file
not_in_file=[]
for down_elem in list_ID_download:
    if (down_elem in participant_digital)==False :
        not_in_file.append(down_elem)
            
    
#find the items in the digital file but not downloaded (Kate's rescued data presumably)


not_in_downloads=[]
for elem_digital in participant_digital:
    if (elem_digital in list_ID_download)==False:
        not_in_downloads.append(elem_digital)          
    


total_digital_users=num_entries+len(not_in_downloads)

# =============================================================================
#  Sweep through downloaded files and retrieve annotations
# =============================================================================

import duplicate_handler


entry_frame=pd.DataFrame({"Participant": [0], 
                                "Part": [0], 
                                "Text": [""],
                                "Note": [""] ,
                                "Source": [""]}) 
    
df_blank=pd.DataFrame({"Participant": [0], 
                                "Part": [0], 
                                "Text": [""],
                                "Note": [""] ,
                                "Source": [""]})     
col_clean=["Participant", "Part"]


df_empty=pd.DataFrame({})
    
regen_frame=pd.DataFrame({ }) 
    
Part_text=2
userID=1024 

for t in range(num_entries):
    userID=list_ID_download[t]
    Part_text=list_parts[t]
    
    recup=duplicate_handler.retrieve_annotations_digital(Part_text,userID)
    annot=recup[1]
    
    num_annot=len(annot)
    
    for k in range(num_annot):
        entry_frame.loc[0,"Participant"]=list_ID_download[t]
        entry_frame.loc[0,"Part"]=list_parts[t]
        entry_frame.loc[0,"Text"]=annot[k]
        entry_frame.loc[0,"Source"]="Downloaded"
       # regen_frame.loc[4,:]=entry_frame.loc[0,:]
        regen_frame=regen_frame.append(entry_frame, ignore_index=True)






ID_mined=np.array( regen_frame["Participant"], dtype=int)
participant_mined=list( set( list(ID_mined)) )
num_mined=len(participant_mined)
    
# =============================================================================
#  Add in entries with notes to final 
# =============================================================================

array_notes=np.array(data_orig["Note"]!="", dtype=bool)
num_notes=sum(array_notes)

df_notes=data_orig[array_notes].copy()
df_notes["Source"]="file_annot"

regen_frame=regen_frame.append(df_notes, ignore_index=True)

# =============================================================================
# Auditing differences in users 
# =============================================================================

# unique ID final

unique_ID_final=list( set( list( np.array(regen_frame["Participant"], dtype=int) ) ) )
unique_ID_final.sort()
print len(unique_ID_final)


unique_notes=list( set( list( np.array(df_notes["Participant"], dtype=int) ) ) )
unique_notes.sort()

print "unique notes"
print unique_notes

print "not downloaded"
print not_in_downloads

print "not in file"
print not_in_file


# =============================================================================
#  Add in other users that still do not show up
# =============================================================================
list_ID_regen=list(regen_frame["Participant"])
not_in_regen=[]
for elem_digital in participant_digital:
    if (elem_digital in list_ID_regen)==False:        
        not_in_regen.append(elem_digital)          
    
df_other=df_empty.copy()
for user_new in not_in_regen:
    arr=  (data_orig["Participant"]==(user_new) )

    df_sel= data_orig[ arr ].copy()
    df_sel["Source"]="digital_from_video"
    
    df_other=df_other.append(df_sel, ignore_index=True)
    

regen_frame=regen_frame.append(df_other, ignore_index=True)

# =============================================================================
#  Fix user numbers
# =============================================================================


regen_rep=replace_IDs(regen_frame)


# =============================================================================
# Sort and get information on IDS present
# =============================================================================

cols_df=["Participant", "Part", "Text", "Note", "Source"]

regen_sorted=regen_rep.sort_values("Participant", kind="mergesort")


unique_ID_sorted=list( set( list( np.array(regen_sorted["Participant"], dtype=int) ) ) )


master_list=get_master_list()
list_parts_master=get_list_parts()

new_frame=pd.DataFrame(columns=cols_df)

for t in range( len( master_list ) ) :
    elem=master_list[t]
    if (elem in unique_ID_sorted)==False:
        #if no text if found add in a blank entry line
        
        new_frame=pd.DataFrame(columns=cols_df)
        new_frame.loc[0,"Participant"]=int(elem)
        
          
        new_frame.loc[0,"Part"]=list_parts_master[t]
        new_frame.loc[0,"Text"]=""
        new_frame.loc[0,"Note"]=""
        new_frame.loc[0,"Source"]="Blank_dig"
        regen_sorted=regen_sorted.append(new_frame, ignore_index=True)
  
        
        
regen_final=regen_sorted.sort_values("Participant",kind="mergesort")


# =============================================================================
# Check if there is any missing or extras
# =============================================================================
unique_ID_final=list( set( list( np.array(regen_final["Participant"], dtype=int) ) ) )

in_final_not_master=[]
for ID in unique_ID_final:
    if (ID in master_list)==False:
        in_final_not_master.append(ID)

in_master_not_final=[]
for ID in master_list:
    if (ID in unique_ID_final)==False:
        in_master_not_final.append(ID)


regen_final.to_csv("regenerated_digital.csv", columns=["Participant", "Part", "Text", "Note", "Source"] , index=False)

# =============================================================================
# count blank
# =============================================================================

blanks_count=sum(np.array(regen_final["Source"]=="Blank_dig", dtype=bool))


