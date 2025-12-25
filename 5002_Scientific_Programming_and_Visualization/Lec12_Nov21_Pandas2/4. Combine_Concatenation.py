import pandas as pd
import numpy as np

#example 1
s11 = pd.Series([0, 1], index=['a', 'b'])
s12 = pd.Series([2, 3, 4], index=['c', 'd', 'e'])
s13 = pd.Series([5, 6], index=['f', 'g'])

pd.concat([s11, s12, s13])
#By default concat works along axis=0, producing another Series. If you pass axis=1,
#the result will instead be a DataFrame (axis=1 is the columns)
pd.concat([s11, s12, s13],axis=1)


#example 2: You can instead intersect them by passing join='inner'
pd.concat([s11, s12, s13],axis=1,join='inner')
s2=pd.concat([s11,s13])
pd.concat([s11, s2],axis=1,join='inner')

#example 3: concatation with keys. 
#It will create a hierarchical index on the concatenation axis
s3 = pd.concat([s11, s11, s13], keys=['one', 'two', 'three'])

s3.unstack()
#In the case of combining Series along axis=1, the keys become 
#the DataFrame column headers
pd.concat([s11, s12, s13], axis=1, keys=['one', 'two', 'three'])

#example 4: concatation for dataframe objects
df41 = pd.DataFrame(np.arange(6).reshape(3, 2), 
                   index=['a', 'b', 'c'],columns=['one', 'two'])

df42 = pd.DataFrame(5 + np.arange(4).reshape(2, 2),
                   index=['a', 'c'],columns=['three', 'four'])

pd.concat([df41, df42], keys=['level1', 'level2'])
pd.concat([df41, df42], axis=1, keys=['level1', 'level2'])
#If you pass a dict of objects instead of a list, 
#the dict’s keys will be used for the keys option
pd.concat({'level1': df41, 'level2': df42}, axis=1)

#example 5: There are additional arguments governing how the hierarchical 
#index is created 
pd.concat([df41, df42], axis=1, keys=['level1', 'level2'], 
          names=['upper', 'lower'])

#example 6: ignore index
df61 = pd.DataFrame(np.random.randn(3, 4), columns=['a', 'b', 'c', 'd'])
df62 = pd.DataFrame(np.random.randn(2, 3), columns=['b', 'd', 'a'])

pd.concat([df61, df62], ignore_index=True)

#example7: combine_first can update null elements with value in the same location in other

s71 = pd.Series([np.nan, 2.5, np.nan, 3.5, 4.5, np.nan],
              index=['f', 'e', 'd', 'c', 'b', 'a'])

s72 = pd.Series(np.arange(len(s71), dtype=np.float64),
              index=['f', 'e', 'd', 'c', 'b', 'a'])

#combine_first can update null elements with value in the same location in other
s71.combine_first(s72)

#np.where(condition, x, y) 
#if condition is satisfied, output x, otherwise output y
np.where(pd.isnull(s71), s72, s71)

#With DataFrames, combine_first does the same thing column by column, so you
#can think of it as “patching” missing data in the calling object with data 
#from the #object you pass
df71 = pd.DataFrame({'a': [1., np.nan, 5., np.nan],
                    'b': [np.nan, 2., np.nan, 6.],
                    'c': range(2, 18, 4)})

df72 = pd.DataFrame({'a': [5., 4., np.nan, 3., 7.],
                    'b': [np.nan, 3., 4., 6., 8.]})

df71.combine_first(df72)










