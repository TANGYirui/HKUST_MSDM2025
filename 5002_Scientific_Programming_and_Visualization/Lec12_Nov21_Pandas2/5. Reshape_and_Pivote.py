import pandas as pd
import numpy as np


########## stack and unstack
data = pd.DataFrame(np.arange(6).reshape((2, 3)),
                    index=pd.Index(['Ohio', 'Colorado'], name='state'),
                    columns=pd.Index(['one', 'two', 'three'], name='number'))

result = data.stack()
result.unstack()

#By default the innermost level is unstacked (same with stack). 
#You can unstack a different level by passing a level number or name
result.unstack(0)
result.unstack('state')
#Unstacking might introduce missing data if all of the values in the level 
#aren’t found in each of the subgroups

s1 = pd.Series([0, 1, 2, 3], index=['a', 'b', 'c', 'd'])
s2 = pd.Series([4, 5, 6], index=['c', 'd', 'e'])
data2 = pd.concat([s1, s2], keys=['one', 'two'])

data2.unstack()

#Stacking filters out missing data by default,
#so the operation is more easily invertible

data2.unstack().stack()
data2.unstack().stack(dropna=False)

#When you unstack in a DataFrame, the level unstacked becomes 
#the lowest level in the result
df = pd.DataFrame({'left': result, 'right': result + 5},
                  columns=pd.Index(['left', 'right'], name='side'))

df.unstack('state')

#When calling stack, we can indicate the name of the axis to stack
df.unstack('state').stack('side')


################ pivoting and melting
wdata = pd.read_csv(r'file_examples\wide_format.csv')
ldata = pd.read_csv(r'file_examples\long_format.csv')

# DataFrame.pivot(*, columns, index=<no_default>, values=<no_default>)[source]
# Return reshaped DataFrame organized by given index / column values.

# Reshape data (produce a “pivot” table) based on column values. Uses unique values from specified index / columns to form axes of the resulting DataFrame. This function does not support data aggregation, multiple values will result in a MultiIndex in the columns. See the User Guide for more on reshaping.

wdata_pivot = ldata.pivot_table('year','variable','value')
# ldata_melt = pd.melt(wdata, ['year'])



# The first two values passed are the columns to be used respectively as 
# the row and column index, then finally an optional value column to fill 
# the DataFrame.
# Suppose you had two value columns that you wanted to reshape simultaneously

ldata['value2'] = np.random.randn(len(ldata))

#By omitting the last argument, you obtain a DataFrame with hierarchical columns
# pivoted = ldata.pivot('year', 'variable')


#An inverse operation to pivot for DataFrames is pandas.melt. Rather than 
#transforming one column into many in a new DataFrame, it merges multiple
#columns into one, producing a DataFrame that is longer than the input

df = pd.DataFrame({'key': ['foo', 'bar', 'baz'],
                    'A': [1, 2, 3],
                    'B': [4, 5, 6],
                    'C': [7, 8, 9]})

melted = pd.melt(df, ['key'])

#Using pivot, we can reshape back to the original layout
reshaped = melted.pivot('key', 'variable', 'value')
reshaped2= melted.pivot_table('value',index='key',columns='variable')

#Since the result of pivot creates an index from the column used as the row 
#labels, we may want to use reset_index to move the data back into a column
reshaped.reset_index()

#You can also specify a subset of columns to use as value columns
pd.melt(df, id_vars=['key'], value_vars=['A', 'B'])

#pandas.melt can be used without any group identifiers
pd.melt(df, value_vars=['A', 'B', 'C'])
pd.melt(df, value_vars=['key', 'A', 'B'])


