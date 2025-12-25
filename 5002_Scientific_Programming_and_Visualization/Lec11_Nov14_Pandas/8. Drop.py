import pandas as pd
import numpy as np

S0 = pd.Series(np.arange(5.), index=['a', 'c', 'c', 'd', 'e'])

#For series, it is pretty simple and straight forward
S1 = S0.drop('c')
S2 = S0.drop(['d', 'c'])
##Q1: how about the orginal obj???
#Many functions, like drop, which modify the size or shape of a Series or 
#DataFrame, can manipulate an object in-place without returning a new object
print(S0)
S0.drop('c', inplace=True)
print(S0)

#With DataFrame, index values can be deleted from either axis. 
DF = pd.DataFrame(np.arange(16).reshape((4, 4)),
                    index=['Ohio', 'Colorado', 'Utah', 'New York'],
                    columns=['one', 'two', 'three', 'four'])

DF1 = DF.drop(['Colorado', 'Ohio'])

#You can drop values from the columns by passing axis=1 or axis='columns'
# data2 = data.drop('two', axis=1)
DF2 = DF.drop('two', axis='columns')

DF3 = DF2.copy()
### add new column
DF3['five']=pd.NA
### add one row by loc
DF3.loc['Hong Kong']=[16,17,18,pd.NA]



