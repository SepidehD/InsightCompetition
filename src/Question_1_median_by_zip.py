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
import statistics

from time import clock

# About code: 
# In this code, we use Federal Election data (accessable from
# http://classic.fec.gov/finance/disclosure/ftpdet.shtml )
# to find information about political donors.

# The code processes each line of the input file. For each input file line, 
# calculate the running median of contributions, total number of transactions
# and total amount of contributions for that recipient and zip code.



# part 1: Import data
# thename list shows the data columns' name. These names and related data 
# dictionary are available from:
# http://classic.fec.gov/finance/disclosure/metadata/DataDictionary\
#ContributionsbyIndividuals.shtml


# CMTE_ID: identifies the flier, which is the recipient of this contribution
# ZIP_CODE: zip code of the contributor 
# TRANSACTION_DT: date of the transaction
# TRANSACTION_AMT: amount of the transaction
# OTHER_ID: a field that denotes if contribution came from a person or an entity

start=clock()
thename= ['CMTE_ID','AMNDT_IND','RPT_TP','TRANSACTION_PGI','IMAGE_NUM','TRANSACTION_TP','ENTITY_TP','NAME','CITY','STATE','ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID','TRAN_ID','FILE_NUM','MEMO_CD','MEMO_TEXT','SUB_ID'
]

df= pd.read_table('./input/itcont.txt', sep = '|', header = None, names = thename,
                  low_memory = False, usecols=['CMTE_ID','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID'],
                   dtype={'CMTE_ID':object,'ZIP_CODE':str,'TRANSACTION_DT':str,'TRANSACTION_AMT':np.float64,'OTHER_ID':str},
                   error_bad_lines = False, iterator = True, chunksize = 1000 )

df = pd.concat(df, ignore_index = True)

##########part 2: Clean and prepare data

#subset to 5 characters:

df.ZIP_CODE = df.ZIP_CODE.str[:5] 

# this says if a other-id col hase value, drop it!:
    
df.drop(df['OTHER_ID'].isnull(), inplace = True)  

# drop rows which have null values in one the three col:
    
df.dropna(subset = ['ZIP_CODE' , 'CMTE_ID' ,'TRANSACTION_AMT'] ,axis=0, inplace = True) 


df.to_pickle('pikpik')
df2=pd.read_pickle('pikpik')


#### Part 3: the body of the code

# I save the unique values of (CMTE_ID, ZIP_CODE) in ids:

ids = []

# saving the first line of the code in the txt file:

text = str(df2.iloc[0,0]) + '|'+ str(df2.iloc[0,1])+'|' + str(int(round(df2.iloc[0,3],0)))+'|' + "1"+'|' + str(int(round(df2.iloc[0,3],0)))
savefile = open('./output/medianvals_by_zip.txt', 'a')
savefile.write(text +'\n')

# append the first tuple of (CMTE_ID, ZIP_CODE) in ads list:
    
ids.append(tuple((df2.iloc[0,0], df2.iloc[0,1])))




# what I add to index? index is a one dimention array, with multiple lists in it.
#each list contains, 1- index of the unique tuple, 2- number of transaction 3- all amt of transactions
# that i need them to calculate the median.

index = []

# I add first row information here:
    
index.append([0,1,int(round(df2.iloc[0,3],0))]) 

for i in range(1,df2.shape[0]):
        #print i
        a = df2.iloc[i,0]
        b = df2.iloc[i,1]
        if (a,b) not in ids:
          ids.append((a,b))
          total_amount_trans = int(round(df2.iloc[i,3],0))
          number_of_trans = 1
          median_trans = int(round(df2.iloc[i,3],0))
          
          #Temporary list to help appending information to the main inxel list:
              
          m = []
          m.append(ids.index(tuple((a,b))))
          m.append(1)
          m.append(total_amount_trans)
          index.append(m)
          
          
          text = str(a)+'|'+ str(b)+'|' + str(total_amount_trans)+'|' + str(number_of_trans)+'|'+ str(median_trans)
          savefile.write(text+ '\n')
        
        # if there is repetition in tuple(CMTE_ID, ZIP_CODE),
        # I add previous amounts to the current amount and then 
        # calculate the median.
        else:

          total_amount_trans = int(round(df2.iloc[i,3],0)) 
          in2 = ids.index(tuple((a,b)))
          index[in2].append(total_amount_trans)
          index[in2][1] = index[in2][1] + 1
          number_of_trans = index[in2][1] 
          cc = index[in2][2:]
          median_trans = int(round(statistics.median(cc),0))
          
          # saving to the txt file
          text= str(a) +'|'+ str(b)+'|'+ str(total_amount_trans)+'|'+ str(number_of_trans)+'|'+ str(median_trans)
          savefile.write(text + '\n')
  
savefile.close()

time= clock()-start
print time
