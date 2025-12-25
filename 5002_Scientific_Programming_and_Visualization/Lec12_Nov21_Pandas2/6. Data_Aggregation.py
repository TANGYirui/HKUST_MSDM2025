import pandas as pd
import numpy as np


df = pd.DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'],
                   'key2' : ['one', 'two', 'one', 'two', 'one'],
                   'data1' : np.arange(5)+10,
                   'data2' : np.arange(5)+100})

#the data1 column using the labels from key1.
#This grouped variable is now a GroupBy object. It has not actually computed 
#anything yet except for some intermediate data about the group key df['key1'].
grouped = df['data1'].groupby(df['key1'])
grouped.sum()
grouped.mean()

#You can also use two different keys at the same time
means = df['data1'].groupby([df['key1'], df['key2']]).mean()
means.unstack()

# you can also do it for all the columns
df.groupby('key1')[['data1','data2']].mean()


#The GroupBy object supports iteration
for name, group in df.groupby('key1'):
    print(name)
    print(group)
    
#In the case of multiple keys, the first element in the tuple 
#will be a tuple of key values
for (k1, k2), group in df.groupby(['key1', 'key2']):
    print((k1, k2))
    print(group)
    
    
#By default groupby groups on axis=0, but you can group on any of the other axes.
#For example, we could group the columns of our example df here by dtype like so
grouped = df.groupby(df.dtypes, axis=1)
print('\n'*2)
for dtype, group in grouped:
    print(dtype)
    print(group)

















