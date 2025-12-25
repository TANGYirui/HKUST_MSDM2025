import pandas as pd
import numpy as np

obj = pd.Series(range(3), index=['a', 'b', 'c'])
index = obj.index


# #Q1:Index objects are immutable and thus can't be modified by the user
index[1]='d'

labels = pd.Index(np.arange(3))
obj2 = pd.Series([1.5, -2.5, 0], index=labels)
print(id(obj2.index))
print(id(labels))
print(obj2.index is labels)

#In addition to being array-like, an Index also behaves like a fixed-size set
print('a' in index)

#Unlike Python sets, a pandas Index can contain duplicate labels
#Selections with duplicate labels will select all occurrences of that label
dup_labels = pd.Index(['foo', 'foo', 'bar', 'bar'])
obj3 = pd.Series([1.5, -2.5, 0, 5], index=dup_labels)
print(obj3['foo'])





