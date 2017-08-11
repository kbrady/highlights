#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:18:04 2017

@author: jorge
"""

#from parse import *


import re
import numpy as np

print "This will parse the html file for student IDs"

file_out='ID_list_digital.dat'

filename="/home/jorge/Downloads/mass_down/ID_files/Hypo_ID_mess.html"



def read_whole(filename):
    # reads a file and reaturns its contents as a string
        file_inp=filename
        try:
            str=open(filename,'r').read()
        
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error reading {0} ".format(file_inp)
            raise IOError
        return str


input_str=read_whole(filename)

#seq_id='?s_id='
seq_id=r'.s_id='
full_seq=seq_id+r'(\d+)'
#seq_id="test."
#input_str="test ?test 4test1"
lseq=len(seq_id)
numlen=6


arr=[m.start() for m in re.finditer(full_seq, input_str) ]

num_matches=len(arr)
t=-1

ID_array_rep=[0]*num_matches
for elem in arr:
    t+=1
    s=input_str[elem:elem+12]
    search_res=re.search(r'\d+',s)
    numID=search_res.group(0)
    ID_array_rep[t]=numID
    print s, "     ", numID


ID_array=np.array( list( set(ID_array_rep) ) ,dtype=int )
ID_array.sort()
num_ID_unique=len(ID_array)

fid=open(file_out,"w")
fid.write("%d \n"%(num_ID_unique))
for t in range(num_ID_unique):
    s="%d %d \n"%(t+1, ID_array[t])
    fid.write(s)
fid.close()

#==============================================================================
# Make output for minning
#==============================================================================

root=r"http://localhost:8000/womens_suffrage_2_A.html?s_="
file_mine="ID_URL_mine.dat"

fid=open(file_mine,"w")
fid.write("%d \n"%(num_ID_unique))
for t in range(num_ID_unique):
    ID=ID_array[t]
    s_url=root+"%d "%(ID)
    s="%d %d %s \n"%(t+1, ID_array[t], s_url )
    fid.write(s)
fid.close()


