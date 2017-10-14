#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 09:57:01 2017

@author: jorge
"""


import re
import numpy as np
import sys 
import pandas as pd
import os


valid_types={"b": 1, "a": 2}
inv_valid_types={ 1: "b", 2: "a"}


file_invest=pd.read_csv("investigation_summary.csv", na_filter=False, dtype=str)

blank=(file_invest["Redcap_id"]=="")

df_ids=file_invest[ np.logical_not(blank)  ].copy()


# =============================================================================
#  Add in part number
# =============================================================================
#df_ids["Part"]=0

cond_list=list(df_ids["condition"])
list_parts=[]
for cond in cond_list:
    list_parts.append( valid_types[cond]   )

df_ids["Part"]=np.array(list_parts, dtype=int)

#for t in df_ids.index:
#    df_ids.loc[t,"Part"]= valid_types[ df_ids.loc[t,"condition"] ]


redcap= list( np.array( df_ids["Redcap_id"]  ,dtype=int) )
highlights_id=np.array( df_ids["highlights_id"]  , dtype=int)


#df_ids= df_ids_str[["Redcap_id","highlights_id" ]].apply(pd.to_numeric)

diff_id_array=(df_ids["Redcap_id"]!=df_ids["highlights_id"])

df_problem=df_ids[diff_id_array].copy()

df_problem.to_csv("differing_ids.csv",columns=["Redcap_id", "highlights_id"], index=False)

print df_problem["highlights_id"], df_problem["Redcap_id"]

