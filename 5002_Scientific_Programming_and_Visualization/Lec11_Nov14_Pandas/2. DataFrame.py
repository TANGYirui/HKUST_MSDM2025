import pandas as pd
import numpy as np

#convert a dict of equal-length lists or numpy array to a DataFrame object
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
'year': [2000, 2001, 2002, 2001, 2002, 2003],
'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame0 = pd.DataFrame(data)
frame1 = pd.DataFrame(np.random.randn(4, 3))

##convert a nested dict of dicts. Pandas will interpret the outer dict keys
##as the columns and the inner keys as the row indices
pop = {'Nevada': {2001: 2.4, 2002: 2.9},
       'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
frame2 = pd.DataFrame(pop)

#specify a sequence of columns
frame3 = pd.DataFrame(data, columns=['year', 'state', 'pop'])

#Pass a column that isn’t contained in data
frame3 = pd.DataFrame(data, columns=['year', 'state', 'pop', 'debt'],
                  index=['one', 'two', 'three', 'four', 'five','six'])

# ##quesitons
# Q1. Can the number of index and rows of data be different
frame3 = pd.DataFrame(data, columns=['year', 'state', 'pop', 'debt'],
                  index=['one', 'two', 'three', 'four', 'five'])

#use a list to change the value
frame3['debt'] = np.arange(0,6,1)
#Q2. Can the length of list and index different?
# frame3['debt'] = np.arange(1,6,1)
# frame3['debt'] = 6.5

# #use a Series to change the value
val = pd.Series([-1.2, -1.5, -1.7], index=['two', 'four', 'five'])
frame3['debt'] = val

# Q3. How about the index does not exist in DataFrame
val = pd.Series([-1.2, -1.5, -1.7], index=['two', 'four', 'seven'])
frame3['debt'] = val

# # # #add a non-existing column
frame3['eastern'] = frame3.state == 'Ohio'
# #delete a column
del frame3['eastern']





