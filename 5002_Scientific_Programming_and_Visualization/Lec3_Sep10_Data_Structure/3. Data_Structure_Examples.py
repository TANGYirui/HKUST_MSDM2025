# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
"""

# a list of strings
animals = ['name', 'class', 'age', 'country']

# a list of integers
numbers = [1, 7, 4, 10, 162]

# an empty list
my_list = []

# a list of variables we defined somewhere else
#things = [var1, var2, var3]


numbers = [1, 2, 3, 4, 5, 5, 5]

# add an element to the end
numbers.append(5)
print(numbers)
# append several values at once to the end, differnent from append
#numbers.extend([56, 2, 12])
numbers.append([56, 2, 12])
print(numbers)

# count how many times a value appears in the list
numbers.count(5)

# find the index of a value
numbers.index(3)
# if the value appears more than once, we will get the index of the first one
numbers.index(2)
## if the value is not in the list, we will get a ValueError!
#numbers.index(42)

# insert a value at a particular index
numbers.insert(0, 45) # insert 45 at the beginning of the list

# remove an element by its index and assign it to a variable
my_number = numbers.pop(0)

# remove an element by its value
numbers.remove(2)
# if the value appears more than once, only the first one will be removed
numbers.remove(5)


#exmaple of Tuple
WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')


#exmaple of set
even_numbers = {2, 4, 6, 8, 10}
big_numbers = {6, 7, 8, 9, 10}

# subtraction: big numbers which are not even
print(big_numbers - even_numbers)

# union: numbers which are big or even
print(big_numbers | even_numbers)

# intersection: numbers which are big and even
print(big_numbers & even_numbers)

# numbers which are big or even but not both
print(big_numbers ^ even_numbers)

#examples of range
# print the integers from 0 to 9
print(list(range(10)))

# print the integers from 1 to 10
print(list(range(1, 11)))

# print the odd integers from 1 to 10
print(list(range(1, 11, 2)))

#examples of dictionary
marbles = {"red": 34, "green": 30, "brown": 31, "yellow": 29 }

# Get a value by its key, or None if it doesn't exist
marbles.get("orange")
marbles["red"]
# We can specify a different default
marbles.get("orange", 0)

# Add several items to the dictionary at once
marbles.update({"orange": 34, "blue": 23, "purple": 36})

# All the keys in the dictionary
marbles.keys()
# All the values in the dictionary
marbles.values()
# All the items in the dictionary
marbles.items()



