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
import pickle  # pickle used for serialization

start=clock()

# About code: 
# In this code, we use Federal Election data (accessable from
# http://classic.fec.gov/finance/disclosure/ftpdet.shtml )
# to find information about political donors. 
# Each line of the  output file lists every unique combination of date and 
# recipient from the input file and then the calculated total 
# contributions and median contribution for that combination of date and recipient.


 
#### part 1: Import data
# thename list shows the data columns' name. These names and related data 
# dictionary are available from:
# http://classic.fec.gov/finance/disclosure/metadata/DataDictionary\
#ContributionsbyIndividuals.shtml.

thename = ['CMTE_ID','AMNDT_IND','RPT_TP','TRANSACTION_PGI','IMAGE_NUM',\
'TRANSACTION_TP','ENTITY_TP','NAME','CITY','STATE','ZIP_CODE','EMPLOYER',\
'OCCUPATION','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID','TRAN_ID',\
'FILE_NUM','MEMO_CD','MEMO_TEXT','SUB_ID'
]


# CMTE_ID: identifies the flier, which is the recipient of this contribution
# ZIP_CODE: zip code of the contributor 
# TRANSACTION_DT: date of the transaction
# TRANSACTION_AMT: amount of the transaction
# OTHER_ID: a field that denotes if contribution came from a person or an entity

inputaddress = "./input/itcont.txt"     #'./input/itcont.txt'
df2 = pd.read_table(inputaddress, sep= '|', header=None, names=thename,
                  low_memory=False, usecols=['CMTE_ID','ZIP_CODE',\
                  'TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID'],
                   dtype={'CMTE_ID':str,'ZIP_CODE':str,'TRANSACTION_DT':str,\
                   'TRANSACTION_AMT':np.float32,'OTHER_ID':str},
                   error_bad_lines = False, iterator=True, chunksize=1000 )
df2 = pd.concat(df2,ignore_index=True)

time= clock() - start 
#print 'total time', time

#### part 2: Clean data
# Changing datatypes that helps to run the code faster:

df2['CMTE_ID'] = df2['CMTE_ID'].astype('category')
df2['TRANSACTION_DT'] = df2['TRANSACTION_DT'].astype('category')
df2['OTHER_ID'] = df2['OTHER_ID'].astype('category')



# using pickle to serialize the dataframe:
    
df2.to_pickle('pikpik')
df = pd.read_pickle('pikpik')



# if the "OTHER_ID" has the value, I drop that row because the identity of 
# donor shoule be private.

df.drop(df['OTHER_ID'].isnull(), inplace=True) 

# I check the rows to be sure that donor id, date of transaction, and zipcode
# have value. if not I drop them.

df.dropna(subset = ['CMTE_ID','TRANSACTION_DT','ZIP_CODE'], axis=0, inplace = True) 

# make a unique value of donor's id and zipcode:
    
list_of_IDs = sorted(df.CMTE_ID.unique())
list_of_zipcodes = sorted(df.ZIP_CODE.unique())



#### part 3: Main functions

mydict = {}

# In older version of python that I use, the dictionary automaticllay is sorted
# based on the key but I needed to keep th eorder becasue I want to have a
# sorted output based on my sorted input.

mydict = collections.OrderedDict(mydict)



# the inputs: 
    #a= recipiant id
    #b= transaction date
    # the dictionary to save the data(this is an optional)
# What does this function do?:
    # This function groups the CMTE_ID and the Dates of transactionans in order to 
    # calculate the median, number of transactions and the sum of total 
    # transcations for each of these groups.
# The output: at the end I will have a dictionary wich cointains all the
# median, number of transactions, and amount of transcations based on each 
# repiciant and 

time= clock() - start 
###print 'time', time
    
def func_calc(a,b,mydict):
       #print a
       general = df.loc[(df.CMTE_ID==a)& (df.TRANSACTION_DT==b),\
       'TRANSACTION_AMT']
       median_trans = int(round(general.median(),0))
       number_of_trans = general.count()
       total_amount_trans = int(round(general.sum(),0))
       mydict[tuple((a,b))] = (median_trans, number_of_trans,total_amount_trans)
       #return a,b,median_trans,number_of_trans,total_amount_trans
       return 
       
       

# the input of the function is a that is the participiant Id (CMTE_ID).   
# this function makes a list of dates that are correspond with each participent.
# the output of the function: this function runs the second function that is 
# caled func_clac, based on list of 
# sorted lists of the transaction dates. 
   
def calc_dates_array(a):
    dates_array = sorted(set(df.loc[df.CMTE_ID == a,'TRANSACTION_DT'].values))
    for x in dates_array:
       func_calc(a,x,mydict)
       time = clock()-start 
      # print 'total time', time
      
      
# I used map() to run the functions on the list of participents.  
# because I have a function inside a function, I actually run both functions
# using map().
    
map(calc_dates_array,list_of_IDs)
time = clock()-start 


 
#### Part 4: Print the results as a txt file.
# The format of the output will be Participant_ID|Date of transaction|
# Mean of contributions recieved by recipiant on that day|
# Total number of transactions recieved by recipiant on that date.

with open("./output/medianvals_by_date.txt","w") as f:  #./output/median_by_date.txt
    for k,v in mydict.items():
        data=str(k[0]),str(k[1]),str(v[0]),str(v[1]),str(v[2])
       # print data
        f.write("|".join(data)+"\n")
f.close()

#print mydict
time= clock() - start 
print 'total time', time

  