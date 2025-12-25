import pandas as pd
import numpy as np

# Example 1: series
S1 = pd.Series(np.linspace(11,19,9), index=[['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'd'],[1, 2, 3, 1, 3, 1, 2, 2, 3]])


S1.index
S1.index.shape
S1.index.levels[0]
S1.index.levels[1]

#different to access the multiple level index
S1['a']
S1.loc['a']
S1.loc['a',:]
S1.loc[['a','d'],1]
S1.loc[:,1]
S1.iloc[0:5]
S1[:,1]

A=S1.unstack()
B=A.stack()


# Example 2: dataframe
DF2 = pd.DataFrame(np.arange(12).reshape((4, 3)), index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]], columns=[['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])

# give names to index
DF2.index.names=['key1','key2']
DF2.columns.names=['state','color']

C=DF2.unstack()
C.index
C.columns

C2=C.unstack()
C2.index
C2.columns

C3=C.stack()
C3.index
C3.columns

# creat index
MI=pd.MultiIndex.from_arrays([['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']], names=['state', 'color'])

# Reordering and Sorting Levels
DF2.swaplevel('key1', 'key2')
DF2.sort_index(level=1)
DF2.swaplevel(0, 1).sort_index(level=0)

# set_index() and reset_index()
D=DF2.reset_index('key1')
D2=D.reset_index('key2')
E=D2.set_index(['key1','key2'])
E.index
E.columns

E2=D2.set_index(['key2','key1'])
E2.index
E2.columns

################# for multi-level index
#you can use set_index and reset_index to 
#realize multilevel idnex
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
'year': [2000, 2001, 2002, 2001, 2002, 2003],
'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame0 = pd.DataFrame(data)

frame5=frame0.set_index(['state','year'])
frame0_back=frame5.reset_index(level=[1])
frame0_back0=frame5.reset_index(level=[0,1])
frame0_back1=frame5.reset_index('state')
frame0_back2=frame0_back1.reset_index('year')

#different to access the multiple level index
print(frame5.loc['Ohio'].loc[2001])
print(frame5.loc['Ohio',2001])
print(frame5.iloc[2])

