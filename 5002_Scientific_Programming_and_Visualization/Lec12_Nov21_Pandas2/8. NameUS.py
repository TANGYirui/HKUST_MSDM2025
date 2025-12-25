import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ### do few tests before you use it
names1880 = pd.read_csv('names/yob1880.txt',
                        names=['name', 'sex', 'births'])
names1880
names1880.groupby('sex').births.sum()
names1880.groupby('name').births.sum()
### do simple check
names1880.groupby('sex').births.sum().sum() - names1880.groupby('name').births.sum().sum()

################### Task 0: get all the data
years = range(1880, 2019)

pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = 'names/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)

    frame['year'] = year #add new column to save year
    pieces.append(frame)

## Concatenate everything into a single DataFrame
## names = pd.concat(pieces)
## # check the index
## print(names.index)
## print(names.loc[[1,100]])
names0 = pd.concat(pieces, ignore_index=True)
names = names0.copy()
## # check the index
## print(names.index)
## print(names.loc[[1,100]])
#
#

################### Task 1: births of males and females
total_births_sex = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)
# total_births_sex_default = names.pivot_table('births', index='year', columns='sex')
# total_births_sex_mean = names.pivot_table('births', index='year', columns='sex', aggfunc='mean')
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html

# ##doubel check
# n1880=names[names['year']==1880]
# sum(n1880[n1880['sex']=='F']['births'])
# n1880[n1880['sex']=='F']['births'].sum()
# sum(n1880[n1880['sex']=='M']['births'])

total_births_sex.plot(title='Total births by sex and year')

################### Task 2: find the the top 1,000 names for each sex/year combination
def add_prop(group):
    group['prop'] = group['births'] / group['births'].sum()
    return group
#get the propobility of each name for given year and sex
names = names.groupby(['year', 'sex'],group_keys=False).apply(add_prop)

# to do a sanity check.
# verifying that the prop column sums to 1 within all the groups:
print(names.groupby(['year', 'sex'])['prop'].sum())


# now we extract a subset of the data to facilitate further analysis: 
# the top 1,000 names for each sex/year combination

# # you can do it by hand
# pieces = [] 
# for year, group in names.groupby(['year', 'sex']): 
#     pieces.append(group.sort_values(by='births', ascending=False)[:1000]) 
# top1000 = pd.concat(pieces, ignore_index=True)

# you can also do it using apply function
def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]

grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
#check the data
print(top1000.loc[1880,'F'])

# check the index
print(top1000.index)
# Drop the group index, not needed
top1000.reset_index(inplace=True, drop=True)


################### Task 3: analyze Naming Trends
boys = top1000[top1000['sex'] == 'M']
girls = top1000[top1000['sex'] == 'F']
# check the index
print(boys.index)

total_births_top1000 = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)

# check the basic information
print(total_births_top1000.info())

#check the data
print(top1000[(top1000.name=='Mary')&(top1000.year==1880)])
print(total_births_top1000.loc[1880,'Mary'])

#get a subset and plot to check the results
subset = total_births_top1000[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots=True, figsize=(12, 10), grid=False,
            title="Number of births per year")

################### 4 Measuring the increase in naming diversity
# plt.figure()
table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex\nProportion of births represented in top 1000 names by sex',
            yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))
#the decrease means that there are more and more other new names. Why??

#you can get how many of the most popular names it takes to reach 50%
boys2010 = boys[boys.year == 2010]
prop_cumsum_2010 = boys2010.sort_values(by='prop', ascending=False).prop.cumsum()
print(prop_cumsum_2010[:10])
num_tmp=prop_cumsum_2010.values.searchsorted(0.5)
# to double check it
print(boys2010[:num_tmp].prop.sum())
print(boys2010[:num_tmp+1].prop.sum())

#compare the results for 1900
boys1900 = boys[boys.year == 1900]
prop_cumsum_1900 = boys1900.sort_values(by='prop', ascending=False).prop.cumsum()
prop_cumsum_1900.values.searchsorted(0.5) # it is much smaller

#do the same thing for all the years
def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')


# fig = plt.figure()
diversity.head()
diversity.plot(title="Number of popular names in top 50%")

################### Task 5: To check the “last letter” revolution
# extract last letter from name column
get_last_letter = lambda x: x[-1]
last_letters = names['name'].map(get_last_letter)
last_letters.name = 'last_letter'

table = names.pivot_table('births', index=last_letters,
                          columns=['sex', 'year'], aggfunc=sum)

##check the results of three different years by hand
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
subtable.head()

#get the quantitative changes
subtable.sum()
letter_prop = subtable / subtable.sum()
letter_prop

#visualize the data
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)
plt.subplots_adjust(hspace=0.25)


### check three different letter
letter_prop = table / table.sum()
dny_ts = letter_prop.loc[['d', 'n', 'y'], 'M'].T
dny_ts.head()

dny_ts.plot()
#
## analyze the similar name
all_names = pd.Series(top1000['name'].unique())
lesley_like = all_names[all_names.str.lower().str.contains('lesl')]
print(lesley_like)

#find the number of these similar names
filtered = top1000[top1000['name'].isin(lesley_like)]
filtered.groupby('name').births.sum()


#Boy names that became girl names (and vice versa)
table = filtered.pivot_table('births', index='year',
                              columns='sex', aggfunc='sum')

#plot the results
# fig = plt.figure()
table.plot(style={'M': 'k-', 'F': 'k--'})
#
#normalize the results and plot it again
table = table.div(table.sum(1), axis=0)
table.tail()

fig = plt.figure()
table.plot(style={'M': 'k-', 'F': 'k--'})
