import pandas as pd
import numpy as np

obj = pd.Series([4.5, 7.2, -5.3, 3.6], index=['d', 'b', 'a', 'c'])
obj2 = obj.reindex(['a', 'a', 'b', 'c', 'd', 'e'])

obj3 = pd.Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
obj4 = obj3.reindex(range(6), method='ffill')

#With DataFrame, reindex can alter either the (row) index, columns, or both.
frame1 = pd.DataFrame(np.arange(9).reshape((3, 3)),
                     index=['a', 'c', 'd'], columns=['Ohio', 'Utah', 'Texas'])
frame2 = frame1.reindex(['a', 'b', 'c', 'd'])

#The columns can be reindexed with the columns keyword
states = ['Utah', 'Texas']
frame3 = frame1.reindex(columns=states)

#you can reindex more succinctly by label-indexing with loc
frame4 = frame1.loc[['a', 'c', 'd'], states]

##Q1. Can use reindex the non-exsiting column
states = ['Texas', 'Utah', 'California']
frame3 = frame1.reindex(columns=states)

##Q2. Can we use loc to reindex the non-existing rows?
states = ['Utah', 'Texas']
frame4 = frame1.loc[['a', 'b', 'c', 'd'], states]





