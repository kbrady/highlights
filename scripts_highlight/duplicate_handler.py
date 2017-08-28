#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 13:28:24 2017

@author: jorge
"""
import numpy as np
import os
import re

from bs4 import BeautifulSoup
from pythonds.basic.stack import Stack

def num_inst_regex(seltext, full_text):
    
    arr=[m.start() for m in re.finditer(seltext, full_text) ]

    num_matches=len(arr)
    
    return num_matches

def inst_regex(seltext, full_text):
    
    arr=[m.start() for m in re.finditer(seltext, full_text) ]

    num_matches=len(arr)
    
    return arr

def num_instances(seltext, full_text):
    list_index=[]
    index=0
    remain=True #keep on searching
    text=full_text
    lensel=len(seltext)
#    lenfull=len(full_text)
    while (remain ==True):        
        index= text.find(seltext,index)
        if index==-1 :
            remain=False
            
        else:
            remain=True                
            list_index.append(index) #store
            #print "going ", seltext , index, lenfull, 
            index=index+lensel #shifts the starting point

    
    num_matches=len(list_index)   
    return list_index


def read_whole(filename):
    # reads a file and reaturns its contents as a string
        file_inp=filename
        try:
            str_wh=open(filename,'r').read()
        
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise
        return str_wh

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


def load_stored_file(file_paths,part,letter,ID):
    lines_source=get_lines(file_paths)

    try:
        number_of_parts=int(lines_source[0])
    
    except ValueError:
        print "Problem with the number of parts"
        raise ValueError
    
    input_path=[""]*number_of_parts
    for t in range(number_of_parts):
        s=lines_source[t+1]
        input_path[t]=s.strip()
    filename="womens_suffrage_%d_%s_%d.html"%(part,letter,ID)    
    full_path=os.path.join(input_path[0],filename  )
    print full_path
    text=read_whole(full_path)
    return text

def get_clean_text(str_full):
    #clean out any blank characters from input string    
    str_words=str_full.split() #removes any whitespaces and line feeds
    text_cleaned=" ".join(str_words) #this reinstates the whitespaces bewteen 
    #creates an array with all the words, no whitespaces or newlines    
    purged_text=text_cleaned.strip() #removes leading and trailing white spaces
    return purged_text

#==============================================================================
# Tets recovery for data
#==============================================================================

def test_recovery():
    file_paths="digital_storage.inp"
    part=2
    ID=3191
    letter="A"
 #_1_B_7564.html
    part=1
    #ID=7564
    ID=9706
    letter="B" 
 
    text=load_stored_file(file_paths,part,letter,ID)
    seltext='<hypothesis-highlight class="annotator-hl">'
    a=inst_regex(seltext,text)
    
    return text

def do_recovery(part,ID):
    file_paths="digital_storage.inp"
    part=2
    ID=3191
    dict_letter={1:"B", 2:"A"}
    letter=dict_letter[part]

 
    text=load_stored_file(file_paths,part,letter,ID)
    seltext='<hypothesis-highlight class="annotator-hl">'
    a=inst_regex(seltext,text)
    
    return text


#html=test_recovery()
#soup = BeautifulSoup(html, 'html.parser')


#print(soup)
#elem = soup.findAll('hypothesis-highlight')
#for sel in elem:
#    print sel

#clean_text=soup.get_text()

#==============================================================================
# tagChecker
#==============================================================================

def tagChecker(symbolString, open_tag, close_tag, status_res):
    s = Stack()
    list_enclosed=[]
    is_balanced=False
    balanced = True
    index = 0
    while index < len(symbolString) and balanced:
        symbol = symbolString[index:index+len(open_tag)]
       # print "acquired :", "#%s#"%(symbol)
        if symbol == open_tag:
         #   print "open tag"
            s.push(index)
            index=index+len(open_tag)-1
        else:
            #print "symbol", symbol
            if s.isEmpty() and (symbolString[index:index+len(close_tag)]==close_tag):
                balanced = False
            elif symbolString[index:index+len(close_tag)]==close_tag:
              #  print "else ", symbolString[index]
                ind_open=s.pop()
                ind_close=index+len(close_tag)-1
                par_open_close=[ind_open,ind_close]
                list_enclosed.append(par_open_close)
             #   print "interval ", symbolString[ind_open:ind_close]
                index = index + len(close_tag) -1
        index = index + 1

#    print "list", list_enclosed[:], len(list_enclosed)
#    for pair in list_enclosed:
#        ind_open=pair[0]
#        ind_close=pair[1]
#        print symbolString[ind_open:ind_close+1]

    if balanced and s.isEmpty():
        is_balanced= True
    else:
        is_balanced= False
    status_res[0]=is_balanced
    
    return list_enclosed

#==============================================================================
#  Removes the annotation tags
#==============================================================================

def hypothesis_tag_remove(annot_text):
    correction_list=[    ['</hypothesis-highlight>',''], 
                     ['<hypothesis-highlight class="annotator-hl">', '']
                     ]
    number_of_corrections=len(correction_list)
    copy_input=annot_text
    
    skipped=0
    not_needed=0
    num_corrected=0
    for t in range(number_of_corrections):
        
        line=correction_list[t]
        if len( line )<2 :
   #         print "skipping correction #", t+1
            skipped=skipped+1
            continue
   #     print "Making correction %d of %d"%(t+1, number_of_corrections)
        old=line[0]    
        correction=line[1]
        
        used=(copy_input.find(old)!=-1)
        if used==False:
            not_needed=not_needed+1
  #          action_str="No action because the correction is not neded."
   #         print action_str
        else:     
 #           print "Replacing %s for $%s$"%(old, correction)    
            num_corrected=num_corrected+1
            copy_input=copy_input.replace(old, correction)        
        
#    print "Skipped ", skipped, " corrections that could not be read from file"
 #   print "Unneccesary corrections : ", not_needed  
 #   print "Total corrections = ", num_corrected
  
    return copy_input    

#==============================================================================
# text purger
#==============================================================================

def text_purger(trim):
    #removes html tags and corrects other small issues to ensure the text matches the md file
    line_prob='<p class=" centered"><img alt="Suffrage advocates threw the very first white house picket protest. For 2 1/2 years, six days a week, they held up signs saying &quot;How long must women wait for liberty?&quot; and &quot;Mr. President, what will you do for woman suffrage?&quot;" src="womens_suffrage_2_A_3191_files/gettyimages-3087724.png">'
    line_less_prob='![Suffrage advocates threw the very first white house picket protest. For 2 1/2 years, six days a week, they held up signs saying "How long must women wait for liberty?" and "Mr. President, what will you do for woman suffrage?"](http://images.mentalfloss.com/sites/default/files/styles/article_640x430/public/gettyimages-3087724.png)'
    
    line_prob1="The 19th Amendment was ratified in 1920, after decades of campaigning by the women's suffrage movement."
    line_less_prob1="> The 19th Amendment was ratified in 1920, after decades of campaigning by the women's suffrage movement."
    
    line_prob1_2=r'<img alt="Elizabeth Cady Stanton and Susan B. Anthony" src="womens_suffrage_1_B_9706_files/tyread8_passage_img2.jpg" title="Elizabeth Cady Stanton and Susan B. Anthony">'
    line_less_prob1_2=r'![Elizabeth Cady Stanton and Susan B. Anthony](https://www.nationsreportcard.gov/subject/reading_2011/images/tyread8_passage_img2.jpg "Elizabeth Cady Stanton and Susan B. Anthony")'
    
    
    correction_list=[ [line_prob1_2, line_less_prob1_2],
                     ["<p>", "\n"], ["</p>", "\n"], ["</div>", " "], 
                     ['<div id="content" class="container-fluid">', " "],
                     ["<h1>", "# "], ["<h3>", "### "], ["</h1>", " "], ["</h3>", " "], 
         #            ['</hypothesis-highlight>',''], ['<hypothesis-highlight class="annotator-hl">', ''],
                     ['<p class=" boxed"><em>', '*'], ['</em>', '*'], [line_prob, line_less_prob],
                     ['<blockquote>', " "],['</blockquote>', " "], ['<p class=" centered">',''],
                     [line_prob1, line_less_prob1]
                     ]
    number_of_corrections=len(correction_list)
    copy_input=trim
    
    skipped=0
    not_needed=0
    num_corrected=0
    for t in range(number_of_corrections):
        
        line=correction_list[t]
        if len( line )<2 :
   #         print "skipping correction #", t+1
            skipped=skipped+1
            continue
  #      print "Making correction %d of %d"%(t+1, number_of_corrections)
        old=line[0]    
        correction=line[1]
        
        used=(copy_input.find(old)!=-1)
        if used==False:
            not_needed=not_needed+1
            action_str="No action because the correction is not neded."
   #         print action_str
        else:     
    #        print "Replacing %s for $%s$"%(old, correction)    
            num_corrected=num_corrected+1
            copy_input=copy_input.replace(old, correction)
        
        
 #   print "Skipped ", skipped, " corrections that could not be read from file"
 #   print "Unneccesary corrections : ", not_needed  
 #   print "Total corrections = ", num_corrected
  
    return copy_input

#==============================================================================
# Tag generator
#==============================================================================
def get_end_tag(part,ID):
    
    if part==2:
        modelA_raw=r'<a alt="" href="http://localhost:8000/womens_post_test_A.html?'
        modelA= modelA_raw+'s_id=%d">'%(ID)
        end_tag=modelA
    elif part==1:
        modelB_raw=r'<a alt="paper_B.html" href="http://localhost:8000/paper_B.html?'  
        modelB=modelB_raw+'s_id=%d">'%(ID)
        end_tag=modelB
    else:
        print "Bad part"
        raise ValueError
    
    #end_tagA='<a alt="" href="http://localhost:8000/womens_post_test_A.html?s_id=3191">Next</a>'
    #end_tagB='<a alt="paper_B.html" href="http://localhost:8000/paper_B.html?s_id=1049">Next</a>'
        
    return end_tag

#==============================================================================
# 
#==============================================================================

#print(parChecker('((( a s  )))'))

#result=tagChecker(test_recovery(), open_tag, close_tag,status_res)
#print result


def get_text_with_annot(part,ID):

    initial_tag='<div id="content" class="container-fluid">'        
    text=do_recovery(part,ID)
    index_ini=text.index(initial_tag)    
    # get end tag position
    end_tag=get_end_tag(part,ID)    
    index_end=text.index(end_tag)
    trim=text[index_ini:index_end]    
    purged=text_purger(trim)    
    text_annot=purged   

    return purged

#==============================================================================
# Verify that the text obtained matches the original one in the md file
#==============================================================================

def verify_with_original(text,part):
    arr_purged=text.split()
    if part==2:
        orig=read_whole("/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_2.md")
    elif part==1:
        orig=read_whole("/home/jorge/Documents/highlights/TIPs_middle_school_stimuli/content/womens_suffrage_1.md")
    orig_clean=orig.split()
    array_comp=np.array( [False]*len(orig_clean) ,dtype=bool)
    for t in range( len(orig_clean)):
        array_comp[t]= (orig_clean[t]==arr_purged[t])
        if (array_comp[t]==False): 
            print "False at ", t, orig_clean[t], " $$$ ", arr_purged[t]
    if ( sum(array_comp)==len(array_comp ) ):
        print "Verification complete: passed"
        return True
    else:
        print "Verification failed"
        return False

#==============================================================================
# Procedures
#==============================================================================

status_res=[0]
open_tag='<hypothesis-highlight class="annotator-hl">'
close_tag='</hypothesis-highlight>'

requested_str="1920"
part=2
ID=3191
def retrieve_annotations_digital(part, ID):
    text_annot=get_text_with_annot(part,ID)    
    annot=tagChecker(text_annot,open_tag,close_tag,status_res)
    num_annot=len(annot)    
    set_of_annot=[]
    set_of_annot_clean=[]
    word_index_set=[]
    for elem in annot:
        ind_ini=elem[0]
        ind_fin=elem[1]
        an_text=text_annot[ind_ini:ind_fin+1]
        set_of_annot.append(an_text)
        text_not_clean=hypothesis_tag_remove(an_text)
        text_clean=get_clean_text(text_not_clean)
        set_of_annot_clean.append( text_clean )
        prec_text=an_text=hypothesis_tag_remove(text_annot[:ind_ini])
        word_array=prec_text.split()
        word_index=len(word_array)
        word_index_set.append(word_index)    
    
    results=[]
    results.append(set_of_annot)
    results.append(set_of_annot_clean)
    results.append(word_index_set)

    return results
res_retrieved=retrieve_annotations_digital(part,ID)

retr_annot_tag=np.array( res_retrieved[0] ,dtype=str)
retr_annot=np.array( res_retrieved[1] , dtype=str)
retr_index=np.array(res_retrieved[2], dtype=int)

num_annot=len(retr_annot)
ismatch=np.array( [False]*num_annot, dtype=bool  )
for t in range(num_annot):
    str_annot=retr_annot[t]
    ismatch[t]=(str_annot==requested_str)

match_index=retr_index[ismatch]

#par1=annot[0]
#selec=text_annot[par1[0] : par1[1]+1]
#selec_noa=hypothesis_tag_remove(selec)

verify_with_original(text_noa,part)







print "Finished"