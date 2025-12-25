import pandas as pd

#directly build a series object
obj = pd.Series([4, 7, -5, 3])

#build a series object with explict index
obj2 = pd.Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])

#alter the index
obj.index = ['Bob', 'Steve', 'Jeff', 'Ryan']

#convert a dict to a series object
sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
obj3 = pd.Series(sdata)

#convert a dict to a series object with index
states = ['California', 'Ohio', 'Oregon', 'Texas']
obj4 = pd.Series(sdata, index=states)

#alter the index
obj.index = ['Bob', 'Steve', 'Jeff', 'Ryan']

#alignment of the data
obj5=obj3+obj4

# #questions
# #Q1. Can you use the duplicate index?
# obj2 = pd.Series([4, 7, -5, 3], index=['d', 'd', 'a', 'c'])
# # If it works, can we convert it to a dict?
# dict2=dict(obj2)
# #Q2. Can the number of index be different from the number of value?
# obj2 = pd.Series([4, 7, -5], index=['d', 'b', 'a', 'c'])
# # #Q3. Can the value be different type?
# obj2 = pd.Series([4, 7, -5, '3'], index=['d', 'b', 'a', 'c'])
# # #Q4. Can the index be different type?
# obj2 = pd.Series([4, 7, -5, '3'], index=['d', 'b', 'a', 10])
# # #Q5. How about empty value?
# obj2 = pd.Series([4, 7, pd.NA, '3'], index=['d', 'b', 'a', 10])
# # #Q6. How about empty index?
# obj2 = pd.Series([4, 7, pd.NA, 3], index=['d', 'b', 'a', pd.NA])