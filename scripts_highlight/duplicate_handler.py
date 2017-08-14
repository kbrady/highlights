#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 13:28:24 2017

@author: jorge
"""


import re

def num_inst_regex(seltext, full_text):
    
    arr=[m.start() for m in re.finditer(seltext, full_text) ]

    num_matches=len(arr)
    
    return num_matches

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