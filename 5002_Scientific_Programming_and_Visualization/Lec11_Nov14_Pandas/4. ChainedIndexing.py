import pandas as pd
import numpy as np

### chained indexing, operation odering matters
df = pd.DataFrame({'a': ['one', 'one', 'two',
                          'three', 'two', 'one', 'six'],
                    'c': np.arange(7)})

labels = pd.Index(['ind0','ind1','ind2','ind3','ind4','ind5','ind6'])
df.index = labels

## Q1. check the following statement, which works?
dfa = df.copy()
dfa['c'][0]=0.1
dfa.iloc[0]['c']=1
dfa.loc['ind0']['c']=11
dfa.loc['ind0','c']=111
dfa.iloc[1,1]=1111

## Q2. check the operation orders
dfb = df.copy()

mask = dfb['a'].str.startswith('o')
###When get the values, the following two seems to be the same
print('case 1:', dfb['c'][mask])
print('case 2:', dfb[mask]['c'])

# # ###while, they are different when you try to assign values,
# # ###the case 1 works, while the case 2 does not
# dfb['c'][mask] = 42
# dfb[mask]['c'] = 24

# # print(type(dfb['c']))
# # print(type(dfb[mask]))

# ## Q3. Better to use loc()
# dfc = df.copy()
# mask = dfc['a'].str.startswith('o')
# dfc.loc[mask,'c'] = 42


