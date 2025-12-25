import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from numpy import nan as NA


# Example 1: Handling missing data
# 1.1 filtering out missing data in series 
S11 = pd.Series(['aardvark', 'artichoke', np.nan, 'avocado'])
# check the output of the following commands in the console windows 
# to understand the results
S11
S11.isnull()

S12 = pd.Series([1, pd.NA, 3.5, np.nan, 7])
S12.dropna()
S12[S12.notnull()]

# 1.2 filtering out missing data in DataFrame 
DF1 = pd.DataFrame([[1., 6.5, 3., 4], [NA, NA, NA, NA],
                     [NA, NA, NA, 3], [NA, NA, 6.5, 3.], [NA, 0, 6, 3.]])
DF1.dropna()
DF1.dropna(how='all')
DF1.dropna(axis=1,how='all')
#thresh: minimum amount of na values to drop (not include)
DF1.dropna(thresh=2)

# 1.3 fill in some values for missing data
DF1.fillna(0)
DF1.fillna({1:100,2:300})  # filling different values for different columns
DF1.fillna(method='ffill') # forward filling for the same column
DF1.fillna(method='bfill') # backward filling for the same column


# Example 2: removing the duplicate data
DF2 = pd.DataFrame({'k1': ['one', 'two'] * 3 + ['two']*2, 'k2': [1, 1, 2, 3, 3, 4, 4, 4], 'k3': [1.1, 1.09, 2, 3, 3, 4.001, 4.001,4.003]})
DF2.loc[8]=['one',3,3]
###check whether the values of k1 and k2 are the same
DF2.duplicated(['k1', 'k2'])
DF2.duplicated(['k1', 'k2', 'k3'])
DF2.drop_duplicates(['k1', 'k2'], keep='last')
DF2.round({'k3':2}).drop_duplicates(['k3'], keep='last')

# Example 3: do the element-wise transformation
DF3 = pd.DataFrame({'food': ['bacon', 'pulled pork', 'bacon','Pastrami', 'corned beef', 'Bacon', 'pastrami', 'honey ham', 'nova lox'], 'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})

meat_to_animal = {
'bacon': 'pig',
'pulled pork': 'pig',
'pastrami': 'cow',
'corned beef': 'cow',
'honey ham': 'pig',
'nova lox': 'salmon'
} 

DF3['animal'] = DF3['food'].str.lower().map(meat_to_animal)
DF3['animal'] = DF3['food'].map(lambda x: meat_to_animal[x.lower()])

# Example 4: Replacing values
S4 = pd.Series([1., -999., 2., -999., -1000., 3.]) 
S4.replace(-999, np.nan) 
S4.replace([-999, -1000], np.nan) 
S4.replace([-999, -1000], [np.nan, 0]) 
S4.replace({-999: np.nan, -1000: 0}) 

# Example 5: Renaming Axis Indexes
DF5 = pd.DataFrame(np.arange(12).reshape((3, 4)),
index=['Ohio', 'Colorado', 'New York'],
columns=['one', 'two', 'three', 'four'])

DF5.index=DF5.index.map(lambda x: x[:3].upper())
# DF5.rename(index=str.title, columns=str.upper)
# DF5.rename(index=str.title, columns=str.upper,inplace=True)

# Example 6: Discretization and Binning
ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32] 
bins = [18, 25, 35, 60, 100] 
Categories61 = pd.cut(ages, bins)
group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior'] 
Categories62 = pd.cut(ages, bins, labels=group_names) 


Categories61.codes
Categories61.categories
pd.value_counts(Categories61)

Categories62.codes
Categories62.categories
pd.value_counts(Categories62)

# 6.2: difference between cut() and qcut()
data = np.random.randn(40)
cut61=pd.cut(data, 4, precision=2)
# qcut: Discretize variable into equal-sized buckets based on rank or 
# based on sample quantiles.
qcut62=pd.qcut(data, 4)
qcut63=pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.])

pd.value_counts(cut61)
pd.value_counts(qcut62)
pd.value_counts(qcut63)

# Example 7: Detecting and Filtering Outliers
DF7 = pd.DataFrame(np.random.randn(10, 4)) 
DF7.describe()
#check the outliers
DF7[2][np.abs(DF7[2]) > 1]
DF7[(np.abs(DF7) > 2).any(axis='columns')] 
# DF7[(np.abs(DF7) > 1).any(axis=1)]
#Return whether any element is True, potentially over an axis.
#Return the row as long as there is any outlier in the row

#do something for the outliers
DF71 = DF7.copy()
DF71[np.abs(DF7) > 1] = np.sign(DF7) * 1
DF71.describe() 

# Example 8: Permutation and Random Sampling
# take samples of different rows
DF8 = pd.DataFrame(np.arange(5 * 4).reshape((5, 4)))
sampler = np.random.permutation(5)
sampler
DF8.take(sampler)
DF8.sample(n=3) ##It will be different everytime
#replace keyword can allow repeated choices
DF8.sample(n=6,replace=True)

# Example 9: Computing Indicator/Dummy Variables
DF9=pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'], 'data1': range(20,26)})
pd.get_dummies(DF9['key'])
dummies=pd.get_dummies(DF9['key'],prefix='key')
DF9[['data1']].join(dummies)

# 9.2
np.random.seed(12345)
values = np.random.rand(5)
values
bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
DF92=pd.get_dummies(pd.cut(values, bins))

# Example 10: string manipulation, regular expression
import re

# 10.1 many different ways to use it
text = "foo    bar\t baz  \tqux"
re.split(r'\s+', text)  #the 1st way

regex = re.compile(r'\s+')
re.split(regex,text)   #the 2nd way
regex.split(text)      #the 3rd way

regex.findall(text)
re.findall(regex,text)

# 10.2 a more complicated example
text = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@ust.hk
Ming liu@connect.ust.hk
Ryan ryan@yahoo.com
"""
# there are three parts of patterns
# [A-Z0-9._%+-]+
# @[A-Z0-9.-]+
# \.[A-Z]{2,4}
pattern1 = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
regex1 = re.compile(pattern1, flags=re.IGNORECASE) 
# re.IGNORECASE makes the regex case-insensitive

regex1.findall(text)
regex1.search(text)
regex1.sub('______', text)
print(regex1.sub('REDACTED', text))

### () capture and group
pattern2 = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
regex2 = re.compile(pattern2, flags=re.IGNORECASE)
regex2.findall(text)
print(regex2.sub(r'Username: \1, Domain: \2, Suffix: \3', text))


# 10.3 vectorized string function, how to use re in pandas
data = {'Dave': 'dave@google.com', 'Ming': 'liu@connect.ust.hk', 'Steve': 'steve@gmail.com', 'Rob': 'rob@gmail.com', 'Wes': np.nan}
S10 = pd.Series(data)

S10.str[:]
S10.str.len()

a = S10.str.findall(pattern1, flags=re.IGNORECASE)
b = S10.str.findall(pattern2, flags=re.IGNORECASE)

#check the following examples for comparison
re.findall(pattern2,S10['Dave'],flags=re.IGNORECASE)

c=S10.copy()
c[0:4]=list(map(lambda x: regex2.findall(x), S10[0:4]))


# ## sometimes it might give unexpected results?
# d=S10.copy()
# d[S10.notnull()]=list(map(lambda x: regex2.findall(x), S10[0:4]))
# d[S10.notnull()]=list(map(lambda x: regex2.findall(x), S10[S10.notnull()]))





















