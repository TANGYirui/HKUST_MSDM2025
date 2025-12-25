# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
Organize the code using functions or other structures

Easy to read
Easy to find the redundancy or inefficient parts

Note: It is still very slow and the search order is bad since it starts with 
the big number.

"""
import time

start_time=time.time()
#def func_check(xx,yy,zz):
#    get_result=0
#    for x in xx:
#        for y in yy:
#            for z in zz:
#                if x**3+y**3+z**3 == The_number:
#                    get_result=1
##                    return x,y,z,get_result
#                    break
#            if get_result==1:
#                break
#        if get_result==1:
#            break
#    return x,y,z,get_result


def func_check(xx,yy,zz):
    get_result=0
    for x in xx:
        for y in yy:
            for z in zz:
                if x**3+y**3+z**3 == The_number:
                    get_result=1
                    return x,y,z,get_result
    return x,y,z,get_result

The_number=42

Num_Try=11
limit=1

get_result=0
while Num_Try>0 and get_result==0:
    Num_Try = Num_Try -1
    limit = limit+10
    print("Searching the results in range [",-limit,",",limit,")")
    xx=list(range(-limit,limit))
    yy=list(range(-limit,limit))
    zz=list(range(-limit,limit))
    x,y,z,get_result=func_check(xx,yy,zz)

if x**3+y**3+z**3 == The_number:
    print(str(x),'^3 + ',str(y),'^3 + ',str(z),'^3 = ',str(The_number))     
else:
    print("We cannot get the results in range [",-limit,",",limit,")")               
                
print("Time for the whole program --- %s seconds ---"%(time.time()-start_time)) 