# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
It is still very slow and the search order is bad since it starts with 
the big number. In this version, we changed the search order.

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

The_number=42

Limit_Block=5; limit=10; xx0=list(range(-limit,limit)); 
yy0=list(range(-limit,limit)); zz0=list(range(-limit,limit))

block_shift=[0]
for n in range(1,Limit_Block+1):
    block_shift.append(n);  block_shift.append(-n)

get_result=0; range_min=0; range_max=0
for Num_x in block_shift:
    for Num_y in block_shift:
        for Num_z in block_shift:
            xx=[x+2*limit*Num_x for x in xx0 ]
            yy=[y+2*limit*Num_y for y in yy0 ]
            zz=[z+2*limit*Num_z for z in zz0 ]
            range_min=min(range_min,min(xx))
            range_max=max(range_max,max(xx))
            x,y,z,get_result=func_check(xx,yy,zz)
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