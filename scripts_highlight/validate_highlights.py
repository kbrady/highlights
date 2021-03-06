#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:50:40 2017

@author: jorge
"""

import csv

import sys
import os
import errno

import numpy as np
import pandas as pd

const_end=99999999


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
file_input=get_name(line_list,"spell_corrected:")

print "Input Name acquired ", file_input

highlight_info=file_input

#==============================================================================
# Output file name
#==============================================================================

file_out=get_name(line_list,"clean:")

print "Output Name acquired ", file_out

file_blank="blank.csv"
file_multiplicity="multiplicity.csv"
file_bad_multiplicity="bad_multiplicity.csv"

#==============================================================================
# Error logs
#==============================================================================

file_error_log='error.log'
file_error_csv='error_not_in_text.csv'


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
            raise IOError
        return 0

def write_error_duplicate(filename,frame,motive, location):
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
            s="Rows with duplicates: %d \n"%(num_error_rows)
            fid_error.write(s)
            s="A copy of problem rows has been stored in: %s \n"%(location)
            fid_error.write(s)
            s=" \n \n"
            fid_error.write(s)
            fid_error.close()
            
            
        except ValueError:
            print "Error writing to %s"%(filename)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise IOError
        return 0

def write_error_duplicate_corrected(filename,frame,motive, location):
    # reads a file and reaturns its contents as a string
        file_inp=filename
        try:
            num_error_rows=len(frame)

            fid_error=open(filename,'a')      
            s="Multiplicity correction procedures finished. \n"
            fid_error.write(s)
            s="Motive: %s \n"%(motive)
            fid_error.write(s)
            s="Rows with duplicates: %d \n"%(num_error_rows)
            fid_error.write(s)
            s="A copy of problem rows has been stored in: %s \n"%(location)
            fid_error.write(s)
            s=" \n \n"
            fid_error.write(s)
            fid_error.close()
            
            
        except ValueError:
            print "Error writing to %s"%(filename)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise IOError
        return 0

#==============================================================================
# Words files
#==============================================================================

file_words='words.dat'
file_words_csv='words.csv'

#==============================================================================
# Source files 
#==============================================================================

file_sources='sources.dat'
lines_source=get_lines(file_sources)

try:
    number_of_parts=int(lines_source[0])

except ValueError:
    print "Problem with the number of parts"
    raise

input_files=[""]*number_of_parts
for t in range(number_of_parts):
    s=lines_source[t+1]
    input_files[t]=s.strip()

print input_files


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

def unique_find(str_target,str_text):
    #this will search for a match and make output its uniquenss
    #the code will search for the fragment from the left and from the right. If its unique the positions will be the same
    ind_first=str_text.find(str_target)
    ind_last=str_text.rfind(str_target)
    match= (ind_first == ind_last) # true if its a unique fragment
    struct_find=[ind_first,match]
    if ind_first==-1 :
        raise ValueError
    return match



#==============================================================================
# Read the data from the participants file
#==============================================================================
print "Reading data from participants"

data_orig=pd.read_csv(highlight_info, na_filter=False, dtype=str )
size_data=len(data_orig)

# =============================================================================
# Load correction data
# =============================================================================

def load_corrections():
    try:
        file_inp="bad_multiplicity_corrections.csv"
        df_man_cor=pd.read_csv(file_inp, na_filter=False, dtype=str, index_col=0)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "Error reading {0} ".format(file_inp)
        print "File with multiplicity corrections not found"
        return []
    return df_man_cor


def load_correction_digital():
    df_digital_correct=pd.read_csv("digital_corrections.csv", na_filter=False, dtype=str )
    
    
    return df_digital_correct


# =============================================================================
#  Correction routines
# =============================================================================


def correction_digital_scheme(t,df_dup, data_orig):
    index_corr_man=-1
    index_corrected=-1
    success_corr=False   
    try:
        userID=int(df_dup.loc[t,"Participant"])
        entry_index=df_dup.loc[t,"usr_entry_index"]
        df_digital_corr=load_correction_digital()
        arr_corr_dig=(df_digital_corr["Participant"]=="%d"%(userID))&(df_digital_corr["usr_entry_index"]=="%s"%(entry_index)) 
        df_corr_sel=df_digital_corr[arr_corr_dig]
        
        if len(df_corr_sel)==0:
            return -1
        
        index_corr_man=int(df_corr_sel.loc[df_corr_sel.index[0],"manual_correction"])                        
        
        index_corrected=index_corr_man       
        if index_corrected>=0:
            arr_corr_man_dup=(df_dup["Participant"]=="%d"%(userID))&(df_dup["usr_entry_index"]=="%s"%(entry_index))
            sel_entry=list(df_dup.index[arr_corr_man_dup])[0]   
            seltext=data_orig.loc[sel_entry,"Text"]
            data_orig.loc[sel_entry,"ind_start"]=index_corrected
            raw_text=data_orig.loc[sel_entry,"Text"]
            data_orig.loc[sel_entry,"ind_end"]=index_corrected+len(raw_text)
            df_dup.loc[sel_entry,"allocated_iter2"]="%d"%(index_corrected  )
            df_dup.loc[sel_entry,"corrected_manual"]=True
            print "sel_entry", sel_entry, t, index_corrected

        
        success_corr=True
        print index_corr_man
    except IOError:
        raise
        print " io error", userID, t
    except KeyError:
        raise
        print "key error", userID, t    
    except ValueError:
        raise
        print "value error", userID, t

   
    if success_corr==True:     
        pass
       #print "\n\n\n\n Correction t= %d index= %d \n\n"%(t, index_corr_man )
    else:
        print "\n\n\n\n"
        print "Cannot allocate entry. Will discard:", seltext, " for ", userID
        return -1

    return 0



#==============================================================================
# Validate highlights 
#==============================================================================
print "Validating highlights"

highl_index_beg=[0]*size_data
highl_index_end=[0]*size_data

array_highlight=np.array(data_orig["highlight"], dtype=int )
num_highlights=sum(array_highlight)

valid_highlights=np.array([0]*size_data, dtype=bool)
array_blank=np.array([False]*size_data ,dtype=bool)
array_duplicate=np.array([False]*size_data ,dtype=bool)

t=0  
failure_count=0  #stores the number of highlights that were not located
for t in range(size_data):     
     #print "Checking row", t        
     high_of_row=get_clean_text(data_orig.loc[t,"Text"])
     try:
         usr_id=int(data_orig.loc[t,"Participant"])          
     
     except ValueError:
         print "Error at ",t,data_orig.loc[t,"Participant"]
         valid_highlights[t]=False
         raise
     #print "Checking ID", usr_id
     file_index=np.int(data_orig.loc[t,"Part"])        
     file_cleaned = "" #cleanses the string, for security
     file_cleaned = file_set[file_index-1]
     index= file_cleaned.find(high_of_row)       
     if index == -1 :
         print "Problems in row %d , ID= %d , Text '%s' "%(t+1, usr_id ,high_of_row)
         failure_count=failure_count+1
         valid_highlights[t]=False
         
     else:
         valid_highlights[t]=True  
         if len(high_of_row)==0: 
             # the highlight is blank             
             array_blank[t]=True
             data_orig.loc[t,"blank?"]="%d"%(1)   
             #ensure the fragment does not appear multiple times
         try:
            
             is_unique = unique_find(high_of_row,file_cleaned) 
             if (is_unique== False) and (array_blank[t]==False):
                 #duplicate is present
                 array_duplicate[t]=True 
                 print "Duplicate in row ", t+1, " with text ", high_of_row
         except ValueError:
             print "Error looking for duplicate in row ", t+1 , " with text ", high_of_row
             
            
             
             
     highl_index_beg[t]=index
     highl_index_end[t]=index+len(high_of_row)-1
     data_orig.loc[t,"ind_start"]=highl_index_beg[t]
     data_orig.loc[t,"ind_end"]=highl_index_end[t]
    
    
    
print "We have %d highlights that were not located "%(failure_count)   
duplicate_count=sum(array_duplicate)
print "We have %d entries with multiplicities "%(duplicate_count)

print "Problematic rows will be dropped"     
print " \n"

import duplicate_handler

# =============================================================================
# Load duplicate corrections
# =============================================================================


file_condition="type.dat"
line=get_lines(file_condition)
type_from_file=line[0].rsplit()[0]



if type_from_file=="paper":
    df_multipl_correct=load_corrections()
    df_multipl_correct["context_before_index_beg"]= np.array([0]*len(df_multipl_correct) , dtype=int)
    df_multipl_correct["context_before_index_end"]= np.array([0]*len(df_multipl_correct) , dtype=int)
    
    df_multipl_correct["context_after_index_beg"]= np.array([0]*len(df_multipl_correct) , dtype=int)
    df_multipl_correct["context_after_index_end"]= np.array([0]*len(df_multipl_correct) , dtype=int)
    df_multipl_correct["context_before_valid"]= np.array([True]*len(df_multipl_correct) , dtype=bool)
    df_multipl_correct["context_after_valid"]= np.array([True]*len(df_multipl_correct) , dtype=bool)
    
    context_cols=["context_before_index_beg", "context_before_index_end", "context_after_index_beg", "context_after_index_end" ]
    
    
    
    for t in df_multipl_correct.index:
        print "checking problem", t
        Part_text=int(df_multipl_correct.loc[t, "Part" ]   )
        seltext_orig=df_multipl_correct.loc[t, "context_before"]
        seltext=get_clean_text( seltext_orig)
        if (seltext!=" ") and (seltext !="") :        
            text_from_file=file_set[Part_text-1]
            index_context=text_from_file.find(seltext)
            #list_instances=duplicate_handler.num_instances(seltext, file_set[Part_text-1])
            if index_context >=0:
                #multiple possible previous text choices
                
              
               # file_set[Part_text-1]
                df_multipl_correct.loc[t,"context_before_index_beg"]=index_context
                df_multipl_correct.loc[t,"context_before_index_end"]=index_context+len(seltext)
            elif index_context ==-1 :
                # only one entry for the previous text
                df_multipl_correct.loc[t,"context_before_index_beg"]=0
                df_multipl_correct.loc[t,"context_before_index_end"]=0
                df_multipl_correct.loc[t,"context_before_valid"]=False
        #context_after=df_multipl_correct.loc[t, "context_after"]
        else:
            df_multipl_correct.loc[t,"context_before_index_beg"]=0
            df_multipl_correct.loc[t,"context_before_index_end"]=0
            print "blank", t
            
        seltext_orig=df_multipl_correct.loc[t, "context_after"]
        seltext=get_clean_text( seltext_orig)        
        if (seltext!=" ") and (seltext !="") :        
            text_from_file=file_set[Part_text-1]
            index_context=text_from_file.find(seltext)
            #list_instances=duplicate_handler.num_instances(seltext, file_set[Part_text-1])
            if index_context >=0:
                #multiple possible previous text choices
                
                
               # file_set[Part_text-1]
                df_multipl_correct.loc[t,"context_after_index_beg"]=index_context
                df_multipl_correct.loc[t,"context_after_index_end"]=index_context+len(seltext)
            elif index_context ==-1 :
                # only one entry for the previous text
                df_multipl_correct.loc[t,"context_after_index_beg"]=const_end
                df_multipl_correct.loc[t,"context_after_index_end"]=const_end
                df_multipl_correct.loc[t,"context_after_valid"]=False
        #context_after=df_multipl_correct.loc[t, "context_after"]
        else:
            df_multipl_correct.loc[t,"context_after_index_beg"]=const_end
            df_multipl_correct.loc[t,"context_after_index_end"]=const_end
            print "blank", t
    
    
    df_multipl_correct["context_valid"]=(df_multipl_correct["context_before_valid"]&df_multipl_correct["context_after_valid"])
    
    df_bad_context=df_multipl_correct[~df_multipl_correct["context_valid"]   ]
    
    df_bad_context.to_csv("bad_context.csv")




#==============================================================================
# Export and correct duplicates
#==============================================================================



#figure out which entries are duplicate
df_dup=data_orig[array_duplicate].copy()
df_dup["new_beg"]=np.array( [0]*len(df_dup), dtype= int )
df_dup["new_end"]=np.array( [0]*len(df_dup), dtype= int )
df_dup["multiplicity"]=np.array( [0]*len(df_dup), dtype= int )
df_dup["appearances"]=np.array( [" "]*len(df_dup), dtype= str )
df_dup["allocated"]=np.array( [""]*len(df_dup), dtype= str )
df_dup["allocated_iter2"]=np.array( [""]*len(df_dup), dtype= str )
df_dup["repe"]=np.array( [0]*len(df_dup), dtype= int )
df_dup["repe_index"]=np.array( [""]*len(df_dup), dtype= str )
df_dup["usr_num_h"]=np.array( [0]*len(df_dup), dtype= int )
df_dup["rep_index"]=np.array( [0]*len(df_dup), dtype= int )
df_dup["corrected"]=np.array( [False]*len(df_dup), dtype= bool )

df_dup["context_before"]= np.array( [" "]*len(df_dup), dtype=str)
df_dup["context_after"]= np.array( [" "]*len(df_dup), dtype=str)

df_dup["corrected_manual"]= np.array( [False]*len(df_dup), dtype= bool )
df_dup["corrected_auto"]= np.array( [False]*len(df_dup), dtype= bool )

count_dup=0


print "Acquiring ID list with duplicates"

entries_with_dup=df_dup[["Participant","Part", "type", "Text"]]
entries_with_dup_unique= entries_with_dup.drop_duplicates(keep="first")
 
ID_dup_array=np.array(entries_with_dup_unique["Participant"], dtype=int)
type_dup_array=np.array(entries_with_dup_unique["type"], dtype=str)
part_dup_array=np.array(entries_with_dup_unique["Part"], dtype=int)


dict_duplicates={}
for t in range(len(ID_dup_array)):   
   userID=ID_dup_array[t]
   type_str=type_dup_array[t]
   part_dup=part_dup_array[t]
   
   ind_in_dup=entries_with_dup_unique.index[t]
   text_dup=get_clean_text( entries_with_dup_unique.loc[ind_in_dup, "Text"] )
   tup=tuple([userID, type_str, part_dup, text_dup])
   dict_duplicates[tup]=t

count_array=np.array([0]*len(ID_dup_array), dtype=int  )

fix_paper=0
k=-1

for t in df_dup.index:
    k+=1
    num_instances=0
    instances=[]
    seltext=get_clean_text(df_dup.loc[t,"Text"])
    p=int(df_dup.loc[t,"Part"])
    #print "index ", t
    if (seltext!=" ") and (seltext !="") :
        count_dup+=1
        list_instances=duplicate_handler.num_instances(seltext, file_set[p-1])
        list_inst_str= [ "%d"%(el) for el in list_instances ]
        num_instances=len(list_instances)
        str_appear=" ".join(list_inst_str)
        df_dup.loc[t,"appearances"]=str_appear
        df_dup.loc[t,"multiplicity"]=num_instances
        type_str=df_dup.loc[t,"type"]
        if df_dup.loc[t,"type"]=="website":        
            userID=int(df_dup.loc[t,"Participant"])
            
            Part_text=int(df_dup.loc[t,"Part"])
            
            str_alloc_prev=df_dup.loc[t,"allocated"]
            #num_prev=len(str_alloc_prev.split())
            
            tup=tuple([userID, type_str, Part_text, seltext])
            ind_dict=dict_duplicates[tup]            
            count_array[ind_dict]+=1
            
            num_prev=0
            try :
                correct_index=duplicate_handler.settle_duplicate_web(userID,Part_text,seltext, num_prev ,list_instances)
            
            except IOError:
                print "Catching IOError"
                fid_catch=open("catches_single.out","a")
                fid_catch.write("Caught exception for %d \n"%(userID))
                fid_catch.close()
                correct_index=-1
            if correct_index>0:
                str_alloc=df_dup.loc[t,"allocated"]+" "+"%d"%(correct_index)
                df_dup.loc[t,"allocated"]=str_alloc                
              #  print str_alloc, len(str_alloc.split())
            elif correct_index==-2:
                print "Case of multiple highlights for ", seltext, " userID=", userID
                df_dup.loc[t,"allocated"]="-2"
                 
            elif correct_index==-1:
              #  print "Cannot fix the selected duplicate ", t, seltext
                df_dup.loc[t,"allocated"]="-1"
               
               
        elif df_dup.loc[t,"type"]=="paper":
            userID=int(df_dup.loc[t,"Participant"])
            
            Part_text=int(df_dup.loc[t,"Part"])
            
            str_alloc_prev=df_dup.loc[t,"allocated"]
            #num_prev=len(str_alloc_prev.split())
            
            tup=tuple([userID, type_str, Part_text, seltext])
            ind_dict=dict_duplicates[tup]            
            count_array[ind_dict]+=1
            
            num_prev=0
            arr_usr_ser=(data_orig["Participant"]=="%d"%(userID)) & (data_orig["Part"]=="%d"%(Part_text))
            arr_usr_np=np.array(arr_usr_ser, dtype=bool)
            df_usr=data_orig[arr_usr_np].copy()
            df_usr.loc[:,"repe_index"]=np.array( [-1]*len(df_usr) , dtype=int )
            
            # setup dataframes with repeated entries 
            repe=sum(np.array( df_usr["Text"]==seltext ,dtype=bool  )) 
            
            row_highlight=df_usr[ ( df_usr["Text"]==seltext  )    ]
            df_dup.loc[t,"repe"]=repe
            df_dup.loc[t,"usr_num_h"]=len(df_usr)
            df_repe=df_usr[ ( df_usr["Text"]==seltext  )   ].copy()
            repe_list=df_repe.index.values
            conta=0
            for row_repe in repe_list:                
                df_usr.loc[row_repe,"repe_index"]=conta
                conta+=1
            ls=df_usr.index.values[(df_usr.index.values < t)]
            if (t>df_usr.index.values[0] ) :
                prev_index=t-1 
                pind=df_usr.loc[prev_index,"ind_end"]
            else:
                pind=0
            if (t<df_usr.index.values[-1]) :
                next_index=t+1 
                nind=df_usr.loc[next_index,"ind_start"]
            else:
                nind=const_end              
                
            str_app=df_dup.loc[t,"appearances"]    
            list_app=str_app.split()
            list_cand=[]
            for el_app in list_app:
                el_i=int(el_app)
                if ( el_i>pind) & (el_i<nind):
                    list_cand.append(el_i)
                    
            if len(list_cand)==1:
                print "Correction located for entry ", t, df_usr.loc[t,"ind_start"]
                fix_paper+=1
                raw_text=get_clean_text(data_orig.loc[t,"Text"])
                df_dup.loc[t,"ind_start"]=list_cand[0]
                df_dup.loc[t,"ind_end"]=list_cand[0]+len(raw_text)
                
                data_orig.loc[t,"ind_start"]=list_cand[0]
                data_orig.loc[t,"ind_end"]=list_cand[0]+len(raw_text)
                
                df_dup.loc[t,"corrected_auto"]=True
                
                
            else:
                #did not find a unique match within the presented annotations  
                df_dup.loc[t,"allocated"]="-2"
#                context_bef=df_multipl_correct.loc[t,"context_before"]
#                
#                context_aft=df_multipl_correct.loc[t,"context_after"]
#                
#                lowbound=df_multipl_correct.loc[t,"context_before_index_end"]
#                upbound=df_multipl_correct.loc[t,"context_after_index_beg"]
#               
#                for ind_middle_str in list_app:
#                    ind_middle=int(ind_middle_str)
#                    if (ind_middle > lowbound) and (ind_middle< upbound):                        
#                        print "Manual fix match", ind_middle, t
#                        raw_text=data_orig.loc[t,"Text"]
#                        df_dup.loc[t,"ind_start"]=ind_middle
#                        df_dup.loc[t,"ind_end"]=ind_middle+len(raw_text)
#                        
#                        data_orig.loc[t,"ind_start"]=ind_middle
#                        data_orig.loc[t,"ind_end"]=ind_middle+len(raw_text)
#                        df_dup.loc[t,"corrected"]=True
#                        df_dup.loc[t,"allocated"]+="%d"%(ind_middle)
#                
#                if df_dup.loc[t,"corrected"]!=True:
#                    df_dup.loc[t,"allocated"]="-2"

# second pass for correcting problems

visit_array=np.array( [0]*len(count_array)  , dtype=int)

count_realloc=0
k=-1
for t in df_dup.index:
    k+=1
    seltext=get_clean_text(df_dup.loc[t,"Text"])   
  
    if (seltext!=" ") and (seltext !="") :
        type_str=df_dup.loc[t,"type"]
        if df_dup.loc[t,"type"]=="website":        
            userID=int(df_dup.loc[t,"Participant"])        
            Part_text=int(df_dup.loc[t,"Part"])
            tup=tuple([userID, type_str, Part_text, seltext])
            ind_dict=dict_duplicates[tup]          
            num_count=count_array[ind_dict]
            if num_count==1:
                # correct the index
                index_corrected=int( df_dup.loc[t,"allocated"])
                if index_corrected>0:                
                    arr_sel=(data_orig["Participant"]=="%d"%(userID)) & (data_orig["Part"]=="%d"%(Part_text)) & \
                    (data_orig["Text"]== df_dup.loc[t,"Text"]  )
                    
                    arr_sel=np.array(arr_sel, dtype=bool)
                   # print "NZ ", np.nonzero(arr_sel)
                    NZ_list=list( np.nonzero(arr_sel)[0] )
                    sel_entry=NZ_list[0]
                    test_text=data_orig.loc[sel_entry,"Text"]
                    data_orig.loc[sel_entry,"ind_start"]=sel_entry
                    raw_text=data_orig.loc[sel_entry,"Text"]
                    data_orig.loc[sel_entry,"ind_end"]=sel_entry+len(raw_text)
                    df_dup.loc[t,"corrected_auto"]=True

                    print "Reallocated the index for entry ", sel_entry, "for user ", userID 
                    count_realloc+=1
                
                else:
                        res=correction_digital_scheme(t,df_dup, data_orig)
                        fid_disc=open("discarded_temp.out","a")
                        fid_disc.write("else_count >1 user=%d \t t=%d \t  text: %s \t %d\n"%(userID, t, test_text,res)   )
                        fid_disc.close()
                        
                
            elif num_count>1:
               # print "Multiple highlights"
                visit_num=visit_array[ind_dict]                
                visit_array[ind_dict]+=1
                str_appear=df_dup.loc[t,"appearances"]                
                arr_appear=list(np.array( str_appear.split(), dtype=int) )
               
                try:
                    list_index=duplicate_handler.settle_duplicate_web_multi(userID,Part_text,seltext, num_count, arr_appear)
                  
                
                except IOError:
                    print "Catching IOError"
                    fid_catch=open("catches_multiple.out","a")
                    fid_catch.write("Caught exception for %d \n"%(userID))
                    fid_catch.close()
                    list_index=[-1]
                err=-1
                if err in list_index:       
                    #last chance fix manual  
                    index_corr_man=-1
                    index_corrected=-1
                    success_corr=False
                    try:
                        entry_index=df_dup.loc[t,"usr_entry_index"]
                        df_digital_corr=load_correction_digital()
                        arr_corr_dig=(df_digital_corr["Participant"]=="%d"%(userID))&(df_digital_corr["usr_entry_index"]=="%s"%(entry_index)) 
                        df_corr_sel=df_digital_corr[arr_corr_dig]
                        
                        if len(df_corr_sel)==0:
                            raise CorrectionError("Cannot find correction in file ")
                        
                        index_corr_man=int(df_corr_sel.loc[df_corr_sel.index[0],"manual_correction"])                        
                        
                        index_corrected=index_corr_man       
                        if index_corrected>=0:
                            arr_corr_man_dup=(df_dup["Participant"]=="%d"%(userID))&(df_dup["usr_entry_index"]=="%s"%(entry_index))
                            sel_entry=list(df_dup.index[arr_corr_man_dup])[0]                           
                        
                            test_text=data_orig.loc[sel_entry,"Text"]
                            data_orig.loc[sel_entry,"ind_start"]=index_corrected
                            raw_text=data_orig.loc[sel_entry,"Text"]
                            data_orig.loc[sel_entry,"ind_end"]=index_corrected+len(raw_text)
                            df_dup.loc[sel_entry,"allocated_iter2"]="%d"%(index_corrected  )
                            df_dup.loc[sel_entry,"corrected_manual"]=True
                                                    
                        success_corr=True
                        print index_corr_man
                    except IOError:
                        raise
                        print " io error", userID, t
                    except KeyError:
                        raise
                        print "key error", userID, t    
                    except ValueError:
                        raise
                        print "value error", userID, t
                    except CorrectionError:
                        raise
                   
                    if success_corr==True:     
                        pass
                       #print "\n\n\n\n Correction t= %d index= %d \n\n"%(t, index_corr_man )
                    else:
                        
                        print "Cannot allocate entry. Will discard:", seltext, " for ", userID
                                        
                else:
                   # print t, seltext," ",str_appear, list_index, " index_dict ", ind_dict , "\n"
                    index_corrected=list_index[visit_num]
                    arr_sel=(data_orig["Participant"]=="%d"%(userID)) & (data_orig["Part"]=="%d"%(Part_text)) & \
                    (data_orig["Text"]== df_dup.loc[t,"Text"]  )
                    
                    arr_sel=np.array(arr_sel, dtype=bool)
 
                # print "NZ ", np.nonzero(arr_sel)                    
               
                    NZ_list=list( np.nonzero(arr_sel)[0] )                    
                    sel_entry=NZ_list[visit_num]
                    test_text=data_orig.loc[sel_entry,"Text"]
                    data_orig.loc[sel_entry,"ind_start"]=index_corrected
                    raw_text=data_orig.loc[sel_entry,"Text"]
                    data_orig.loc[sel_entry,"ind_end"]=index_corrected+len(raw_text)
                    df_dup.loc[t,"allocated_iter2"]="%d"%(index_corrected  )
                    df_dup.loc[t,"corrected_auto"]=True                   
                    
                    count_realloc+=1
                pass
                print "Multiple appearance index for entry ", sel_entry, "for user ", userID 
                
            else: 
                pass
                print "Entry has wrong number of appearances in text ", tup
                
                       

        elif df_dup.loc[t,"type"]=="paper":
            userID=int(df_dup.loc[t,"Participant"])            
            Part_text=int(df_dup.loc[t,"Part"])            
            str_alloc_prev=df_dup.loc[t,"allocated"]                        
            tup=tuple([userID, type_str, Part_text, seltext])
            ind_dict=dict_duplicates[tup]        
           
            if df_dup.loc[t,"allocated"]=="-2": 
                pass
                corrections_available=True
                if corrections_available==True:                    
                    context_bef=df_multipl_correct.loc[t,"context_before"]                
                    context_aft=df_multipl_correct.loc[t,"context_after"]                
                    lowbound=df_multipl_correct.loc[t,"context_before_index_end"]
                    upbound=df_multipl_correct.loc[t,"context_after_index_beg"]
                   
                    str_app=df_dup.loc[t,"appearances"]    
                    list_app=str_app.split()
                    
                    for ind_middle_str in list_app:
                        ind_middle=int(ind_middle_str)
                        if (ind_middle > lowbound) and (ind_middle< upbound):                        
                            print "Manual fix match", ind_middle, t
                            df_dup.loc[t,"allocated"]=" "
                            raw_text=data_orig.loc[t,"Text"]
                            df_dup.loc[t,"ind_start"]=ind_middle
                            df_dup.loc[t,"ind_end"]=ind_middle+len(raw_text)
                            
                            data_orig.loc[t,"ind_start"]=ind_middle
                            data_orig.loc[t,"ind_end"]=ind_middle+len(raw_text)
                            df_dup.loc[t,"corrected"]=True
                            df_dup.loc[t,"allocated"]+=" %d"%(ind_middle)
                            df_dup.loc[t,"corrected_manual"]=True
                if df_dup.loc[t,"corrected_manual"]!=True:
                    df_dup.loc[t,"allocated"]="-2"
        
        
        
df_dup["corrected"]=(df_dup["corrected_manual"]==True) | (df_dup["corrected_auto"]==True)     
        

multiple_missalloc=(df_dup["allocated"]=="-2") &(df_dup["allocated_iter2"]==""  )
single_missalloc=(df_dup["allocated"]=="-1")&(df_dup["allocated_iter2"]==""  )

array_not_corrected=np.logical_not( np.array( df_dup["corrected"],dtype=bool) )

total_missalloc= single_missalloc | multiple_missalloc | array_not_corrected
bad_realloc=np.array( total_missalloc , dtype=bool)

count_bad_realloc=sum(bad_realloc)
count_bad_mul=sum(multiple_missalloc)
count_bad_sin=sum(single_missalloc)




df_dup.to_csv(file_multiplicity)




arr_multip=np.array( df_dup["Text"], dtype=str)
list_mult= list( set( list(arr_multip) ) )

if count_dup>0:
    motive="Entries with multiple intances detected. A correction will be attempted. "
    write_error_duplicate(file_error_log,df_dup,motive,file_multiplicity)


df_bad_dup=df_dup[bad_realloc].copy()



df_bad_dup.to_csv( file_bad_multiplicity, index=True)

if len(df_bad_dup)>0:
    print "Logging error"
    motive="Some multiple instances could not be corrected. %d problems."%( len(df_bad_dup ) )
    write_error_duplicate(file_error_log,df_bad_dup,motive,file_bad_multiplicity)    
elif len(df_bad_dup)==0:
    print "Logging error and correction notification"
    motive="Correction successfull. Fixed all multiplicity problems."
    write_error_duplicate_corrected(file_error_log,df_bad_dup,motive,file_bad_multiplicity)    
    

array_bu=np.array( df_bad_dup["Participant"], dtype=int)
list_users_review=  list( set( list( array_bu ) ) ) 
list_users_review.sort()
fid=open("user_list_review.txt","w")
for u in range(len(list_users_review)):
    fid.write("%d \t %d \n"%(u+1,list_users_review[u]) )
fid.close()    

# marking bad entries

print "\n \n Reallocated ", count_realloc, "ambigous entries with multiple instances in the text."
print "Uncorrectable entries ", count_bad_realloc, "will be dropped."

index_bad_realloc=df_bad_dup.index.values
valid_highlights[index_bad_realloc]=False

print "Finished with duplicates.. for now"

#==============================================================================
# Export the blank entries
#==============================================================================
     

df_blank=data_orig[array_blank].copy()
df_blank.to_csv(file_blank)    



#==============================================================================
#  Getting rid of bad text selections 
#==============================================================================
motive=" the selected text could not be located within the source files."
array_should_drop= np.logical_not(valid_highlights)  #schedule them for elimination

#copy bad rows and report error
df_bad=data_orig[array_should_drop]
if len(df_bad)>0:
    df_bad.to_csv(file_error_csv, header=True, index=True)
    write_error(file_error_log,df_bad,motive,file_error_csv)


data_clean=data_orig.drop(data_orig[array_should_drop].index ) # drop the bad rows
data_clean.reset_index(drop=True, inplace=True)     

print "Eliminated problem rows"


#==============================================================================
#  Make dataframe with words from file
#==============================================================================
total_words=[0]*number_of_parts
str_words=file_set[0].split()
index_local= np.array( range( len(str_words )))
words_frame=pd.DataFrame({"words": str_words, 
                        "Part": ["1"]*len(str_words),  
                        "index_local": index_local,
                        "hit_count": ["%d"%(0)]*len(str_words) }) 
total_words[0]=len(str_words )

    
for t in range(1,number_of_parts):   
    str_words=file_set[t].split()
    index_local= np.array( range( len(str_words )))
    words_temp=pd.DataFrame({"words": str_words, 
                        "Part": ["%d"%(t+1)]*len(str_words), 
                        "index_local": index_local,
                        "hit_count": ["%d"%(0)]*len(str_words) }) 
    words_frame=words_frame.append(words_temp, ignore_index=True)
    total_words[t]=len(str_words )




#==============================================================================
#  Get the word counts and indices
#==============================================================================
size_data=len(data_clean)
data_clean["word_index"]=["0"]*len(data_clean)
data_clean["word_count"]=["0"]*len(data_clean)

highl_index_beg=np.array(data_clean["ind_start"],dtype=int)
highl_index_end=np.array(data_clean["ind_end"],dtype=int)


for t in range(size_data):
    str_high=data_clean.loc[t,"Text"]
    data_clean.loc[t,"word_count"]=len(str_high.split())    
    prev_string=file_set[ int(data_clean.loc[t, "Part"])-1  ][: highl_index_beg[t]  ]
    #if the highlight is in the middle of a word we must shift it to the beginning of it
    if (len(prev_string) >= 1) and (prev_string[-1] !=" "):
        #looks for the nearest blank space and sets up the beginning on the character right after it 
        ind_corrected=prev_string.rfind(" ")
        str_adjusted=prev_string[: ind_corrected+1  ]
       # print ind_corrected,  highl_index_beg[t], str_adjusted[-4:], prev_string[-4:]
    else:
        str_adjusted=prev_string    
    word_index= len(str_adjusted.split())   
    data_clean.loc[t,"word_index"]= word_index
    part_number=int(data_clean.loc[t,"Part"])
    global_index=sum(total_words[:part_number-1])+word_index
   # print global_index, word_index
    number_of_words=data_clean.loc[t,"word_count"]
    #marks a hit for every time the word was highlighted
    for k in range(number_of_words):
        words_frame.loc[global_index+k,"hit_count"]=int( words_frame.loc[global_index+k,"hit_count"])+1  
    

words_frame.to_csv(file_words_csv, header=True )


#==============================================================================
# Setthe issues with duplicates 
#==============================================================================


#print "Ambiguity must be solved"
#
#
#
##figure out which entries are duplicate
#df_dup=data_orig[array_duplicate]
#df_dup["new_beg"]=np.array( [0]*len(df_dup), dtype= int )
#df_dup["new_end"]=np.array( [0]*len(df_dup), dtype= int )
#
#print "Problematic rows will be dropped"     
#print " \n"


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
# Save output
#==============================================================================

data_clean.to_csv(file_out, header=True , index=False)

print "Finished outputting cleaned highlights"



