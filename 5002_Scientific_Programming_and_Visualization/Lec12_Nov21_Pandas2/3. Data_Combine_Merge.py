import pandas as pd
import numpy as np
#example 1: Many-to-one join
#the data in df1 has multiple rows labeled a and b, 
#whereas df2 has only one row for each value in the key column
df11 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],'data1': range(7)})
df12 = pd.DataFrame({'key': ['a', 'b', 'd'],'data2': range(3)})
print('\ndf11=\n',df11)
print('\ndf12=\n',df12)
print('\nmerge\n',pd.merge(df11,df12))

#If that information is not specified, merge uses the overlapping column names 
#as the keys. It’s a good practice to specify explicitly
print('\nmerge\n',pd.merge(df11,df12,on='key'))

#If the column names are different in each object, you can specify them separately
df13 = pd.DataFrame({'lkey': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],'data1': range(7)})
df14 = pd.DataFrame({'rkey': ['a', 'b', 'd'],'data2': range(3)})
print('\ndf13=\n',df13)
print('\ndf14=\n',df14)
print('\nmerge\n',pd.merge(df13, df14, left_on='lkey', right_on='rkey'))


# By default merge does an 'inner' join; the keys in the result are the 
# intersection, or the common set found in both tables. Other possible options 
# are 'left', 'right', and 'outer'. The outer join takes the union of the keys, 
# combining the effect of applying both left and right joins
print('\nmerge\n',pd.merge(df11,df12,how='outer'))


#example 2: Many-to-Many join
#Many-to-many joins form the Cartesian product of the rows
#The join method only affects the distinct key values appearing in the result
df21 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],'data1': range(6)})
df22 = pd.DataFrame({'key': ['a', 'b', 'a', 'b', 'd'],'data2': range(5)})
print('\ndf21=\n',df21)
print('\ndf22=\n',df22)
print('\nmerge\n',pd.merge(df21,df22,how='inner'))


#example 3: To merge with multiple keys, pass a list of column names

left3 = pd.DataFrame({'key1': ['foo', 'foo', 'bar'],
                      'key2': ['one', 'two', 'one'],
                      'lval': [1, 2, 3]})
right3 = pd.DataFrame({'key1': ['foo', 'foo', 'bar', 'bar'],
                      'key2': ['one', 'one', 'one', 'two'],
                      'rval':[4, 5, 6, 7]})

print('\nleft=\n',left3)
print('\nright=\n',right3)
print('\nmerge\n',pd.merge(left3, right3, on=['key1', 'key2'], how='outer'))

pd.merge(left3, right3, on='key1')
pd.merge(left3, right3, on='key1', suffixes=('_left', '_right'))


#example 4: merging on index
# In some cases, the merge key(s) in a DataFrame will be found in its index. 
# In this case, you can pass left_index=True or right_index=True (or both) 
# to indicate that the index should be used as the merge key

left4 = pd.DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'],'value': range(6)})
right4 = pd.DataFrame({'group_val': [3.5, 7]}, index=['a', 'b'])

print('\nleft1=\n',left4)
print('\nright1=\n',right4)
print('\nmerge\n',pd.merge(left4, right4, left_on='key', right_index=True))

#example 5:
#With hierarchically indexed data, things are more complicated, as joining on 
#index is implicitly a multiple-key merge
left5 = pd.DataFrame({'key1': ['Ohio', 'Ohio', 'Ohio','Nevada', 'Nevada'],
                      'key2': [2000, 2001, 2002, 2001, 2002],
                      'data': np.arange(5.)})

right5 = pd.DataFrame(np.arange(12).reshape((6, 2)),
                      index=[['Nevada', 'Nevada', 'Ohio', 'Ohio','Ohio', 'Ohio'],
                             [2001, 2000, 2000, 2000, 2001, 2002]],
                      columns=['event1', 'event2'])

print('\nlefth=\n',left5)
print('\nrighth=\n',right5)
print('\nmerge\n',pd.merge(left5, right5, left_on=['key1', 'key2'], right_index=True))

#example 6: Using the indexes of both sides of the merge is also possible
left6 = pd.DataFrame([[1., 2.], [3., 4.], [5., 6.]],
                     index=['a', 'c', 'e'], columns=['Ohio', 'Nevada'])

right6 = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [13, 14]],
                      index=['b', 'c', 'd', 'e'], columns=['Missouri', 'Alabama'])

print('\nleft2=\n',left6)
print('\nright2=\n',right6)
print('\nmerge\n',pd.merge(left6, right6, how='outer', left_index=True, right_index=True))

# DataFrame has a convenient join instance for merging by index. It can also be used
# to combine together many DataFrame objects having the same or similar indexes but
# non-overlapping columns. 
print('\njoin\n:',left6.join(right6, how='outer'))









