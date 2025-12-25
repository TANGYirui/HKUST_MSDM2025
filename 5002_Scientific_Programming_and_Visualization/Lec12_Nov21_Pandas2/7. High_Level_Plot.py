import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(np.random.randn(10, 4).cumsum(0),
                  columns=['A', 'B', 'C', 'D'],index=np.arange(0, 100, 10))
df.plot()

fig, axes = plt.subplots(2, 1)
data = pd.Series(np.random.rand(16), index=list('abcdefghijklmnop'))
data.plot.bar(ax=axes[0], color='k', alpha=0.7)
data.plot.barh(ax=axes[1], color='k', alpha=0.7)

df = pd.DataFrame(np.random.rand(6, 4),
                  index=['one', 'two', 'three', 'four', 'five', 'six'],
                  columns=pd.Index(['A', 'B', 'C', 'D'], name='Genus'))

df.plot.bar()
df.plot.barh(stacked=True, alpha=0.5)

### get data from CSV file

# tips = pd.read_csv('file_examples\tips.csv') #does not work, why?
tips = pd.read_csv(r'file_examples\tips.csv')
#use seaborn to plot the data with error bar
plt.figure()
tips['tip_pct'] = tips['tip'] / (tips['total_bill'] - tips['tip'])
sns.barplot(x='tip_pct', y='day', data=tips, orient='h')


#Compute a simple cross tabulation of two (or more) factors.
#By default, computes a frequency table of the factors unless an array of values and an aggregation function are passed.
party_counts = pd.crosstab(tips['day'], tips['size'])
party_counts = party_counts.loc[:, 2:5]
party_pcts = party_counts.div(party_counts.sum(1), axis=0)

party_pcts.plot.bar()






