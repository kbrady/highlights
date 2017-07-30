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

dict_cols={"word": 1, "phrase":   2, "sentence": 3,  "sentence+phrase": 4, "paragraph": 5, "multiple_paragraphs": 6 }
dict_inv={1: "word", 2: "phrase", 3: "sentence",4:   "sentence+phrase", 5: "paragraph", 6: "multiple_paragraphs" }
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
#  Phrase 
#==============================================================================

for t in range(num_entries):
    word_index=int(frame_orig.loc[t,"word_index"])
    word_count=int(frame_orig.loc[t,"word_count"] )
    if word_count==0:
        continue
    sent_first_word=frame_words.loc[word_index,"in_sentence"]
    array_sentence_belong=np.array(frame_words["in_sentence"][word_index:word_index+word_count], dtype=int)
    min_sent=min(array_sentence_belong)
    max_sent=min(array_sentence_belong)
    if (min_sent == max_sent) and (word_count >1):
        #all words belong to the same sentence
        #print "Same sentence"
        
        if word_count==frame_sentence.loc[min_sent,"len_words"]:
            #full sentence
            frame_orig.loc[t,"sentence"]=1
        else:
            #phrase
            frame_orig.loc[t,"phrase"]=1
        
    elif (word_count==1):
        # only has one word        
        frame_orig.loc[t,"word"]=1
        
    elif (min_sent < max_sent):   
        
        array_par_belong=np.array(frame_words["in_paragraph"][word_index:word_index+word_count], dtype=int)
        min_par=min(array_par_belong)
        max_par=min(array_par_belong)
        
        if (min_par == max_par):
            #only one paragraph , all words belong to same paragraph 
            word_par=frame_parag.loc[min_par,"len_words"]
            if (word_par==word_count):
                # whole paragraph
                frame_orig.loc[t,"paragraph"]=1
            elif (word_par > word_count):
                #not whole paragraph
                frame_orig.loc[t,"sentence + phrase"]=1
        elif (min_par<max_par):    
        # multi paragraph
            frame_orig.loc[t,"multiple_paragraphs"]=1
        
        #whole paragraph
        
        
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






   