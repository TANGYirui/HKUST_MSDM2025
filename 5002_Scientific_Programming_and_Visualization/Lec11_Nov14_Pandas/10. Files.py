import pandas as pd
import numpy as np
import sys

# Example 1
filename='file_examples/ex1.csv'
df11 = pd.read_csv(filename)
df12 = pd.read_table(filename, sep=',')

# Example 2
filename='file_examples/ex2.csv'
# 2.1 there could no header in csv
df21 = pd.read_csv(filename,header=None)
# 2.2 add colums by hands
df22 = pd.read_csv(filename, names=['a', 'b', 'c', 'd', 'message'])

# 2.3 you can also set the index
names = ['a', 'b', 'c', 'd', 'message']
df23 = pd.read_csv(filename, names=names, index_col='message')
# You can use df22.set_index('message') to relize df2_3

# Example 3
filename='file_examples/csv_mindex.csv'
parsed = pd.read_csv(filename,index_col=['key1', 'key2'])

# ### In some cases, a table might not have a fixed delimiter, using whitespace or some
# ##other pattern to separate fields.
# ### Because there was one fewer column name than the number of data rows,
# #read_table infers that the first column should be the DataFrame’s index in this spe‐
# #cial case.
# #the fields here are separated by a variable amount of whitespace. 
# #In these cases, you can pass a regular expression as a delimiter for read_table. 
# df3 = pd.read_table('file_examples/ex3.txt', sep='\s+')
# ##dealing with comments or skipping some rows
# df4 = pd.read_csv('file_examples/ex4.csv', skiprows=[0, 2, 3])
# ##dealing with the missing value
# df5 = pd.read_csv('file_examples/ex5.csv')
# #The na_values option can take either a list or set of strings to consider missing values
# df51 = pd.read_csv('file_examples/ex5.csv', na_values=['NULL'])
# sentinels = {'message': ['foo', 'NA'], 'something': ['two']}
# df52 = pd.read_csv('file_examples/ex5.csv', na_values=sentinels)
# pd.options.display.max_rows = 10
# df6 = pd.read_csv('file_examples/ex6.csv')
# df61 = pd.read_csv('file_examples/ex6.csv', nrows=5)
# #The TextParser object returned by read_csv allows you to iterate over the parts of
# #the file according to the chunksize.
# df62 = pd.read_csv('file_examples/ex6.csv', chunksize=1000)
# tot = pd.Series([],dtype='float64')
# for piece in df62:
#     tot = tot.add(piece['key'].value_counts(), fill_value=0)
# tot = tot.sort_values(ascending=False)


# ###write the data into file
# df5.to_csv('file_examples/out.csv')

# ###Other delimiters can be used, of course (writing to sys.stdout so it prints the text
# ###result to the console):
# df5.to_csv(sys.stdout, sep='|')
# #Missing values appear as empty strings in the output. You might want to denote them
# #by some other sentinel value

# df5.to_csv(sys.stdout, na_rep='Spe_Char_For_Empty')

# #With no other options specified, both the row and column labels are written. Both of
# #these can be disabled
# df5.to_csv(sys.stdout, index=False, header=False)

# #You can also write only a subset of the columns, and in an order of your choosing:
# df5.to_csv(sys.stdout, index=False, columns=['a', 'b', 'c'])

# #Series also has a to_csv method
# dates = pd.date_range('1/1/2000', periods=7)
# ts = pd.Series(np.arange(7), index=dates)
# ts.to_csv('file_examples/tseries.csv')


# import csv
# f = open('file_examples/ex7.csv')
# reader = csv.reader(f)
# for line in reader:
#     print(line)
# with open('file_examples/ex7.csv') as f:
#     lines = list(csv.reader(f))

# header, values = lines[0], lines[1:]
# data_dict = {h: v for h, v in zip(header, zip(*values))}

# class my_dialect(csv.Dialect):
#     lineterminator = '\n'
#     delimiter = ';'
#     quotechar = '"'
#     quoting = csv.QUOTE_MINIMAL
# f = open('file_examples/ex7.csv')
# reader = csv.reader(f, dialect=my_dialect)

# #We can also give individual CSV dialect parameters as keywords to csv.reader
# #without having to define a subclass
# f = open('file_examples/ex7.csv')
# reader = csv.reader(f, delimiter='|')

# #To write delimited files manually, you can use csv.writer. It accepts an open, writa‐
# #ble file object and the same dialect and format options as csv.reader
# with open('file_examples/mydata.csv', 'w') as f:
#     writer = csv.writer(f, dialect=my_dialect)
#     writer.writerow(('one', 'two', 'three'))
#     writer.writerow(('1', '2', '3'))
#     writer.writerow(('4', '5', '6'))
#     writer.writerow(('7', '8', '9'))
    
# obj = """
# {"name": "Wes",
# "places_lived": ["United States", "Spain", "Germany"],
# "pet": null,
# "siblings": [{"name": "Scott", "age": 30, "pets": ["Zeus", "Zuko"]},
# {"name": "Katie", "age": 38,
# "pets": ["Sixes", "Stache", "Cisco"]}]
# }
# """

# import json
# #To convert a JSON string to Python form, use json.loads
# result = json.loads(obj)
# #json.dumps, on the other hand, converts a Python object back to JSON
# asjson = json.dumps(result)
# #Conveniently, you can pass a list of dicts (which were previously JSON objects) to the DataFrame constructor and select a sub‐
# #set of the data fields
# siblings = pd.DataFrame(result['siblings'], columns=['name', 'age'])
# #The pandas.read_json can automatically convert JSON datasets in specific arrange‐
# #ments into a Series or DataFrame.

# data = pd.read_json('file_examples/example.json')
# #If you need to export data from pandas to JSON, one way is to use the to_json meth‐
# #ods on Series and DataFrame
# print(data.to_json())
# print(data.to_json(orient='records'))


# ##The pandas.read_html function has a number of options, but by default it searches
# ##for and attempts to parse all tabular data contained within <table> tags. The result is
# ##a list of DataFrame objects
# tables = pd.read_html('file_examples/fdic_failed_bank_list.html')
# failures = tables[0]
# print(failures.head())
# close_timestamps = pd.to_datetime(failures['Closing Date'])
# close_timestamps.dt.year.value_counts()


# #One of the easiest ways to store data (also known as serialization) efficiently in binary
# #format is using Python’s built-in pickle serialization. pandas objects all have a
# #to_pickle method that writes the data to disk in pickle format
# frame = pd.read_csv('file_examples/ex1.csv')
# frame.to_pickle('file_examples/frame_pickle')
# #You can read any “pickled” object stored in a file by using the built-in pickle directly,
# #or even more conveniently using pandas.read_pickle
# pd.read_pickle('file_examples/frame_pickle')




















