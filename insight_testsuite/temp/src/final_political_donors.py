# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 22:14:18 2017

@author: sepid
"""

#Import required packages and libraries
import os
import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
from time import clock
import csv
import collections
from collections import OrderedDict
#import timeit
import pickle  # pickle helps to 

start=clock()
 

thename= ['CMTE_ID','AMNDT_IND','RPT_TP','TRANSACTION_PGI','IMAGE_NUM','TRANSACTION_TP','ENTITY_TP','NAME','CITY','STATE','ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID','TRAN_ID','FILE_NUM','MEMO_CD','MEMO_TEXT','SUB_ID'
]

df2= pd.read_table('C:\\tt\\itcont3.txt', sep= '|', header=None, names=thename,
                  low_memory=False, usecols=['CMTE_ID','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID'],
                   dtype={'CMTE_ID':str,'ZIP_CODE':str,'TRANSACTION_DT':str,'TRANSACTION_AMT':np.float32,'OTHER_ID':str},
                   error_bad_lines = False, iterator=True, chunksize=1000 )
df2 = pd.concat(df2, ignore_index=True)
time= clock()-start
#print 'reading df', time

# I chnaged the dataype to category that is more efficient than str because it helps code to run faster.
df2['CMTE_ID'] = df2['CMTE_ID'].astype('category')
df2['TRANSACTION_DT'] = df2['TRANSACTION_DT'].astype('category')
df2['OTHER_ID'] = df2['OTHER_ID'].astype('category')
df2.to_pickle('pikpik')
df=pd.read_pickle('pikpik')



#print pd.CMTE_ID
#print df.TRANSACTION_AMT
#yy=df[df.CMTE_ID=='C00618140']
#print yy

df.drop(df['OTHER_ID'].isnull(), inplace=True) #this works perfectly
df.dropna(subset=['CMTE_ID','TRANSACTION_DT','ZIP_CODE'] ,axis=0, inplace=True) 


list_of_IDs= sorted(df.CMTE_ID.unique())

      
        
#print list_of_IDs
#list_of_zipcodes= sorted(df.ZIP_CODE.unique().tolist())
list_of_zipcodes= sorted(df.ZIP_CODE.unique())
#print list_of_zipcodes
#global mylist
mydict={}
mydict = collections.OrderedDict(mydict)##what s this line. I older version of python, the dictionary automaticllay is sorted based on the key but I needed to keep th eorder becasue I want to have a sorted output based on my sorted input.
def func_calc(a,b,mydict):
       print a
       #general= df.groupby(df.CMTE_ID==a)& (df.TRANSACTION_DT==b)[df.TRANSACTION_AMT]
       general=df.loc[(df.CMTE_ID==a)& (df.TRANSACTION_DT==b),'TRANSACTION_AMT']
       median_trans=int(round(general.median(),0))
       number_of_trans=general.count()
       total_amount_trans= int(round(general.sum(),0))
       mydict[tuple((a,b))]=(median_trans, number_of_trans,total_amount_trans)
       #time= clock()-start 
       #print 'middle times', time
       return a,b,median_trans, number_of_trans,total_amount_trans

def calc_ziparray(a):
    dates_array=sorted(set(df.loc[df.CMTE_ID==a,'TRANSACTION_DT'].values))
    #print zip_array
    for x in dates_array:
       func_calc(a,x,mydict)
    #count=count+1
   # print 'run for 1 recipient', count   
    #timeit.Timer(calc_ziparray).timeit(number=NUMBER) 
       time= clock()-start 
       print 'total time', time
map(calc_ziparray,list_of_IDs)

time= clock()-start 
#print 'after running function', time
 
#print mydict 
with open("/insight_testsuite/tests/test_1/output/medianvals_by_date.txt","w") as f:
    for k,v in mydict.items():
        data=str(k[0]),str(k[1]),str(v[0]),str(v[1]),str(v[2])
       # print data
        f.write("|".join(data)+"\n")
f.close()

print mydict
#time= clock()-start 
#print 'total time', time

  