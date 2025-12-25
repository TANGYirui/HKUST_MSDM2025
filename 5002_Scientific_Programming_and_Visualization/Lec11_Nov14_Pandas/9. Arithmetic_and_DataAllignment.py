import pandas as pd
import numpy as np

#alignment for series
s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1],index=['a', 'c', 'e', 'f', 'g'])

s3=s1+s2

#alignment for DataFrame
df1 = pd.DataFrame(np.arange(9.).reshape((3, 3)), columns=list('bcd'),
                   index=['Ohio', 'Texas', 'Colorado'])
df2 = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns=list('bde'),
                   index=['Utah', 'Ohio', 'Texas', 'Oregon'])

#Adding these together returns a DataFrame whose index and columns are the unions
#of the ones in each DataFrame
df3 = df1 + df2

#In arithmetic operations between differently indexed objects, you might 
#want to fill with a special value, like 0, when an axis label is found

df4 = pd.DataFrame(np.arange(12.).reshape((3, 4)), columns=list('abcd'))
df5 = pd.DataFrame(np.arange(20.).reshape((4, 5)), columns=list('abcde'))
df5.loc[1, 'b'] = np.nan

print(df4 + df5)
print(df4.add(df5,fill_value=0))

frame = pd.DataFrame(np.arange(12.).reshape((4, 3)),
                     columns=list('bde'),
                     index=['Utah', 'Ohio', 'Texas', 'Oregon'])

series = frame.iloc[0]
series2 = pd.Series(range(3), index=['b', 'e', 'f'])
series3 = frame['d']

frame - series
frame - series2
frame.sub(series3, axis='index')


#NumPy ufuncs (element-wise array methods) also work with pandas objects
###apply function
#f = lambda x: x.max() - x.min()
def f(x):
    return x.max()-x.min()
def f2(x):
    return pd.Series([x.min(), x.max()], index=['min', 'max'])

frame = pd.DataFrame(np.random.randn(4, 3), columns=list('bde'),
                  index=['Utah', 'Ohio', 'Texas', 'Oregon'])
print(frame.apply(f))
print(frame.max()-frame.min())

print(frame.apply(f2))

format = lambda x: '%.2f' % x
print(frame.applymap(format))

###Series has a function map
print(frame['b'].map(format))


df = pd.DataFrame([[1, np.nan,2], [3, 4, 5],
                [np.nan, np.nan, 6], [7,8, 9]],
    index=['a', 'b', 'c', 'd'],
    columns=['one', 'two','three'])

df.cumsum() ##cumulative sum over the index for each column
df.cumsum(axis=1)

df.sum()
df.sum(axis=1)













