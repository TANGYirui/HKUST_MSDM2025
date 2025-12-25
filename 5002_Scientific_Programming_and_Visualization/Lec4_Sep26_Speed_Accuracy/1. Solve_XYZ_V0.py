# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
How do you improve the codes? 
It is clearly inefficient since you have already checked smaller range
"""
import time

start_time=time.time()

The_number=42

Num_Try=100
limit=1

get_result=0
while Num_Try>0 and get_result==0:
    start_time=time.time()
    Num_Try = Num_Try -1
    limit = limit+10
    print("Searching results in range [",-limit,",",limit,")")
    for x in range(-limit,limit):
        for y in range(-limit,limit):
            for z in range(-limit,limit):
                if x**3+y**3+z**3 == The_number:
                    get_result=1
                    break
            if get_result==1:
                break
        if get_result==1:
            break
        
    print("--- %s seconds ---"%(time.time()-start_time)) 
        
if x**3+y**3+z**3 == The_number:
    print(str(x)+'^3 + '+str(y)+'^3 + '+str(z)+'^3 = '+str(The_number))     
else:
    print("We cannot get the results in range [",-limit,",",limit,")")
    
print("--- %s seconds ---"%(time.time()-start_time)) 
    
