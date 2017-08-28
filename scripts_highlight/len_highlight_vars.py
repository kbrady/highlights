#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 09:20:05 2017

@author: jorge
"""

import numpy as np
import pandas as pd

#==============================================================================
# Words sentences parag files
#==============================================================================

file_words_csv='words_list.csv'
file_sentence_csv='sentence_list.csv'
file_parag_csv='parag_list.csv'

file_orig='clean.csv'

file_out='data_augmented.csv'

#==============================================================================
#  Read file with "dictionary" or words, sentences, paragraphs and cleaned user data
#==============================================================================

frame_sentence=pd.read_csv(file_sentence_csv)
frame_parag=pd.read_csv(file_parag_csv)
frame_words=pd.read_csv(file_words_csv)
frame_orig=pd.read_csv(file_orig, na_filter=False, dtype=str)


#==============================================================================
#  Make columns ofr binary values 
#==============================================================================
frame_copy=frame_orig.copy()

dict_cols={"word": 1, "phrase":   2, "sentence": 3,  "sentence + phrase": 4, "paragraph": 5, "multiple_paragraphs": 6 }
dict_inv={1: "word", 2: "phrase", 3: "sentence",4:   "sentence + phrase", 5: "paragraph", 6: "multiple_paragraphs" }
frame_orig["word"]=np.array( [0]*len(frame_orig), dtype=int )
frame_orig["phrase"]=np.array( [0]*len(frame_orig), dtype=int )
frame_orig["sentence"]=np.array( [0]*len(frame_orig), dtype=int )
frame_orig["sentence + phrase"]=np.array( [0]*len(frame_orig), dtype=int )
frame_orig["paragraph"]=np.array( [0]*len(frame_orig), dtype=int )
frame_orig["multiple_paragraphs"]=np.array( [0]*len(frame_orig), dtype=int )


# word: only a single word
# phrase: more than one word but not the entire sentence
# sentence: its an entire sentence 
# sentence+phrase: more than one sentence
# paragraph: its an entire paragraph
# more then one paragraph

#==============================================================================
#  Single word
#==============================================================================
num_entries=len(frame_orig)


#==============================================================================
# Functions
#==============================================================================

def get_clean_text(str_full):
    #clean out any blank characters from input string    
    str_words=str_full.split() #removes any whitespaces and line feeds
    text_cleaned=" ".join(str_words) #this reinstates the whitespaces bewteen 
    #creates an array with all the words, no whitespaces or newlines    
    purged_text=text_cleaned.strip() #removes leading and trailing white spaces
    return purged_text


#==============================================================================
# Need number of words on each part
#==============================================================================
number_of_parts=2
size_words=[0]*number_of_parts
size_sent=[0]*number_of_parts
size_par=[0]*number_of_parts

#fill up word sizes
for p in range(number_of_parts ):
    logi_wordsp=np.array(frame_words.loc[:,"Part"]==(p+1), dtype=bool )
    num_words_p1=sum(logi_wordsp)
    size_words[p]=num_words_p1   

for p in range(number_of_parts ):
    logi_sentp=np.array(frame_sentence.loc[:,"Part"]==(p+1), dtype=bool )
    num_sent_p1=sum(logi_sentp)
    size_sent[p]=num_sent_p1   

for p in range(number_of_parts ):
    logi_parp=np.array(frame_parag.loc[:,"Part"]==(p+1), dtype=bool )
    num_par_p1=sum(logi_parp)
    size_par[p]=num_par_p1   


#==============================================================================
#  Phrase 
#==============================================================================
fid_debug=open("classification.out","w")
offset=0

for t in range(num_entries):
    word_index=int(frame_orig.loc[t,"word_index"])
    word_count=int(frame_orig.loc[t,"word_count"] )
    
    p=int(frame_orig.loc[t,"Part"])
    if p==2:
        offset=size_words[0]
        offset_sent=size_sent[0]
        offset_par=size_par[0]
    else:
        offset=0
        offset_sent=0
        offset_par=0
    
    fid_debug.write(  "Entry %d \n"%(t) )
    fid_debug.write(  "part= %d \n"%(p) )
    fid_debug.write(  "Text: %s \n"%(get_clean_text(frame_orig.loc[t,"Text"] ) ) )
    fid_debug.write(  "word count= %d \n"%(word_count) )
    
    if word_count==0:
        continue
    sent_first_word=frame_words.loc[word_index+offset,"in_sentence"]
    array_sentence_belong=np.array(frame_words["in_sentence"][word_index+offset:word_index+word_count+offset], dtype=int)
    min_sent=min(array_sentence_belong)
    max_sent=max(array_sentence_belong)
    
    fid_debug.write(  "sent min= %d sent_max= %d \n"%(min_sent, max_sent) )
    
    if (min_sent == max_sent) and (word_count >1):
        #all words belong to the same sentence
        #print "Same sentence"
        
        if word_count==frame_sentence.loc[min_sent+offset_sent,"len_words"]:
            #full sentence
            frame_orig.loc[t,"sentence"]=1
            fid_debug.write(  "Veredict: sentence \n" )    
            
        else:
            #phrase
            frame_orig.loc[t,"phrase"]=1
            fid_debug.write(  "Veredict: phrase \n" ) 
        
    elif (word_count==1):
        # only has one word        
        frame_orig.loc[t,"word"]=1
        fid_debug.write(  "Veredict: word \n" ) 
        
    elif (min_sent < max_sent):   
        
        array_par_belong=np.array(frame_words["in_paragraph"][word_index+offset:word_index+word_count+offset], dtype=int)
        min_par=min(array_par_belong)
        max_par=max(array_par_belong)
        fid_debug.write(  "par_min= %d par_max= %d \n"%(min_par, max_par) )
        
        if (min_par == max_par):
            #only one paragraph , all words belong to same paragraph 
            word_par=frame_parag.loc[min_par+offset_par,"len_words"]
            
            fid_debug.write(  "word par= %d \n"%(word_par) )
            
            if (word_par==word_count):
                # whole paragraph
                frame_orig.loc[t,"paragraph"]=1
                fid_debug.write(  "Veredict: paragraph \n" ) 
                
            elif (word_par > word_count):
                #not whole paragraph
                frame_orig.loc[t,"sentence + phrase"]=1
                fid_debug.write(  "Veredict: sentence + phrase \n" ) 
                
        elif (min_par<max_par):    
        # multi paragraph
            frame_orig.loc[t,"multiple_paragraphs"]=1
            fid_debug.write(  "Multiple paragraphs \n" ) 
        #whole paragraph
    fid_debug.write(  "\n \n" )     
        
        # more than one paragraph 
        
        
print "Single word count= ", sum(np.array(frame_orig["word"]))        
print "Phrase count= ", sum(np.array(frame_orig["phrase"]))   
print "Sentence count= ", sum(np.array(frame_orig["sentence"]))         
print "Sentence + phrase count= ", sum(np.array(frame_orig["sentence + phrase"]))  
print "Paragraph= ", sum(np.array(frame_orig["paragraph"]))  
print "Multiple paragraphs= ", sum(np.array(frame_orig["multiple_paragraphs"]))        

#==============================================================================
# Output block
#==============================================================================

frame_orig.to_csv(file_out, index=False)






   