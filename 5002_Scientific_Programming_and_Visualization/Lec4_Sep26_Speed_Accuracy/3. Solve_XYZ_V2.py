# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
In the structuralized codes, it is easy to find whether 
there are some repeated calculations. If so, change your 
codes or algorithms to remove it.
Note: Can you improve it?
"""

import time
start_time=time.time()
def func_check(xx,yy,zz):
    get_result=0
    for x in xx:
        for y in yy:
            for z in zz:
                if x**3+y**3+z**3 == The_number:
                    get_result=1
                    return x,y,z,get_result
    return x,y,z,get_result

The_number=2

Limit_Block=5; 

limit=10; 
xx0=list(range(-limit,limit)); 
yy0=list(range(-limit,limit)); 
zz0=list(range(-limit,limit))

get_result=0; range_min=0; range_max=0
for Num_x in range(-Limit_Block,Limit_Block+1):
    for Num_y in range(-Limit_Block,Limit_Block+1):
        for Num_z in range(-Limit_Block,Limit_Block+1):
            time1=time.time()
            xx=[x+2*limit*Num_x for x in xx0 ]
            yy=[y+2*limit*Num_y for y in yy0 ]
            zz=[z+2*limit*Num_z for z in zz0 ]
            range_min=min(range_min,min(xx))
            range_max=max(range_max,max(xx))
            x,y,z,get_result=func_check(xx,yy,zz)
            # print("time for one block: %s seconds "%(time.time()-time1)) 
            if get_result==1:
                break
        if get_result==1:
            break
    if get_result==1:
        break

if x**3+y**3+z**3 == The_number:
    print(str(x),'^3 + ',str(y),'^3 + ',str(z),'^3 = ',str(The_number))     
else:
    print("We cannot get the results in range [",range_min,",",range_max,"]")                
                
print("Time for the whole program --- %s seconds ---"%(time.time()-start_time)) 