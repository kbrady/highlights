#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 23:02:40 2017

@author: jorge
"""


import re
import numpy as np
import sys 
import pandas as pd
import os


def user_list_frame(df):
    ls=list(np.array(  df["Participant"] ,dtype=int )  )    
    unique_list=list(set(ls))    
    unique_list.sort()
    return unique_list

# =============================================================================
# Read in files
# =============================================================================

#file_paper="/home/jorge/Downloads/highlights_files/file_paper/full_paper_coding_355.csv"

file_source="/home/jorge/Downloads/highlights_files/file_paper/bad_multiplicity_corrections.csv"
file_target="bad_multiplicity.csv"
file_fixed="bad_multiplicity_corrections.csv"


data_source=pd.read_csv(file_source, na_filter=False, dtype=str , index_col=0)
size_source=len(data_source)

data_target=pd.read_csv(file_target, na_filter=False, dtype=str, index_col=0 )
size_target=len(data_target)


# =============================================================================
# 
# =============================================================================
cols_source=list(data_source.columns.values)
cols_target=list(data_target.columns.values)

in_tar_not_source=[]
for elem in cols_target:
    if (elem in cols_source)==False:
        in_tar_not_source.append(elem)

copy_cols=["context_before", "context_after"]
list_diff=[]
copied=0
for t in range( len(data_source ) ):
    ind=data_target.index[t]
    if (data_source.index[t]==ind) :
     if (data_source.loc[ind,"Participant"]==data_target.loc[ind,"Participant"] ) & (data_source.loc[ind,"Text"]==data_target.loc[ind,"Text"] ) :
        for col in copy_cols:
            data_target.loc[ind,col]=data_source.loc[ind,col]
        print "same ", t, ind
        l=True
        copied+=1
    else:
        print "different ", t , ind
        l=False
        list_diff.append(t)

missing=len(data_target)-copied
first_err=list_diff[0]  
sel_arr=np.array( [False]*len(data_target ) , dtype=bool ) 
sel_arr[copied:]=True

# =============================================================================
#  Add in highlight number      
# =============================================================================

data_source["highlight_index"]=0
data_target["highlight_index"]=0

list_of_list=[]    

#assign a number to each highlight
df_sets=[data_source, data_target]

for df_sel in df_sets:    
    df=df_sel
    unique_ID=user_list_frame(df)    
    list_of_list.append(unique_ID)
    for ID in unique_ID:
        sel_part=(df["Participant"]=="%d"%(ID))
        ln=len(df.loc[sel_part, "highlight_index"])
        df.loc[sel_part, "highlight_index"]=range(0,ln)
        
        
#create a dictionary entry for each highlight with the index
        
dict_target={}
df=data_target
for t in df.index: 
    ID=int(df.loc[t,"Participant"] )
    text=df.loc[t,"Text"]
    hl_index=df.loc[t,"highlight_index"]            
    tup=tuple([ID,text,hl_index])
    dict_target[tup]=t

df=data_source
for t in df.index: 
    ID=int(df.loc[t,"Participant"] )
    text=df.loc[t,"Text"]
    hl_index=df.loc[t,"highlight_index"]            
    tup=tuple([ID,text,hl_index])
    try:
        ind=dict_target[tup]

    except KeyError:
        print "Key Error" ,tup
        arr_ex=(data_target["Participant"]=="%d"%(ID)) & ( data_target["Text"]==text )
        df_ex=data_target[arr_ex]
        if len(df_ex)>0:
            ind=df_ex.index[0]       
        else:
            ind=-1
    if ind>-1:        
        for col in copy_cols:
            data_target.loc[ind,col]=data_source.loc[t,col]    
    
    #for col in copy_cols:
         #   data_target.loc[ind,col]=data_source.loc[t,col]
    
#dict_duplicates={}
#for t in range(len(ID_dup_array)):   
#   userID=ID_dup_array[t]
#   type_str=type_dup_array[t]
#   part_dup=part_dup_array[t]
#   
#   ind_in_dup=entries_with_dup_unique.index[t]
#   text_dup=get_clean_text( entries_with_dup_unique.loc[ind_in_dup, "Text"] )
#   tup=tuple([userID, type_str, part_dup, text_dup])
#   dict_duplicates[tup]=t


data_target.to_csv(file_fixed, index=True)

#data_paper=pd.read_csv(file_paper, na_filter=False, dtype=str )
#size_paper=len(data_paper)



#data=purge_unicode("bad_multiplicity_completed_unicode.csv", "bad_multiplicity_corrections.csv")
