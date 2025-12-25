# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 15:39:00 2022

@author: test2
"""
import copy


##### test copy and deep copy
origin=['10','20',[30,40]]

copy0=origin                  ### purely a new assigment
copy1=copy.copy(origin)       ### Shallow copy
copy2=copy.deepcopy(origin)   ### deep copy


print("----------test0-----------")
copy0[0]='copy0'
print("origin =",origin)
print("copy0  =",copy0)
print("copy1  =",copy1)
print("copy2  =",copy2)

print("\n\n----------test1-----------")
copy1[0]='copy1'
print("origin =",origin)
print("copy0  =",copy0)
print("copy1  =",copy1)
print("copy2  =",copy2)

print("\n\n----------test2-----------")
copy1[2][0]='Changed'
print("origin =",origin)
print("copy0  =",copy0)
print("copy1  =",copy1)
print("copy2  =",copy2)


print('id(origin) =',id(origin))
print('id(copy0)  =',id(copy0))
print('id(copy1)  =',id(copy1))
print('id(copy2)  =',id(copy2))

print('id(origin[0]) =',id(origin[0]))
print('id(copy1[0])  =',id(copy1[0]))
print('id(origin[1]) =',id(origin[1]))
print('id(copy1[1])  =',id(copy1[1]))
print('id(origin[2]) =',id(origin[2]))
print('id(copy1[2])  =',id(copy1[2]))

print("\n\n----------test3-----------")
copy1[2]=[4,5]
print("origin =",origin)
print("copy0  =",copy0)
print("copy1  =",copy1)
print("copy2  =",copy2)

print("copy0 is origin,", copy0 is origin)
print("copy1 is origin,", copy1 is origin)
print("copy2 is origin,", copy2 is origin)



import copy
a = [1, 2, [1, 2]]
b = copy.copy(a)
b[2][0] = 11

print("list a:", a)
print("list b:", b)



