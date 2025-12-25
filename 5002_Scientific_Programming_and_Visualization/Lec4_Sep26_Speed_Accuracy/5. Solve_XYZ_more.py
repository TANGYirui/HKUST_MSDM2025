# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
We change the block search ordering. Can you improve it?
There are still some redundancy in the codes since x, y 
and z can interchange with each other.

For loop are extremely slow in python. 
Can you use matrix to replace the for loop?
"""
import time
import numpy as np

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


#put the operations in the outer loop
def func_check1(xx,yy,zz):
    get_result=0
    for x in xx:
        x3=x**3
        for y in yy:
            y3=y**3
            for z in zz:
                if x3+y3+z**3 == The_number:
                    return x,y,z,get_result
    return x,y,z,get_result


#do the power calculations in advance since it will talke some time
def func_check2(xx,yy,zz):
    get_result=0
    xx3=[x**3 for x in xx]
    yy3=[y**3 for y in yy]
    zz3=[z**3 for z in zz]
    for x in xx3:
        for y in yy3:
            for z in zz3:
                if x+y+z == The_number:
                    get_result=1
                    return xx[xx3.index(x)],yy[yy3.index(y)],zz[zz3.index(z)],get_result
    return xx[xx3.index(x)],yy[yy3.index(y)],zz[zz3.index(z)],get_result

#replace the for loop by matrix operations
def func_check3(xx,yy,zz):

    xx3=[x**3 for x in xx]
    yy3=[y**3 for y in yy]
    zz3=[z**3 for z in zz]
    
    MX=np.array(xx3)
    MY=np.array(yy3)
    MZ=np.array(zz3)

    XY=np.zeros([len(xx),len(yy)])
    for n in range(len(yy)):
        XY[n,:]=MX+MY[n]
    
#    XY=np.zeros([len(xx),len(yy)])
#    for n in range(len(yy)):
#        for m in range(len(xx)):
#            XY[n,m]=MX[m]+MY[n]
    
    
    XYZ=np.zeros([len(xx),len(yy),len(zz)])
    for n in range(len(zz)):  
        XYZ[n,:,:]=XY+MZ[n]
        
    T1,T2,T3=np.where(XYZ==The_number)
    
    if len(T1)>0:
        return xx[T1[0]],yy[T2[0]],zz[T3[0]],1
    else:
        return max(xx),max(yy),max(zz),0

#only keep the array which is necessary
def func_check4(xx,yy,zz):

    xx3=[x**3 for x in xx];     MX=np.array(xx3)

    XY=np.zeros([len(xx),len(yy)]) 
    for n in range(len(yy)):
        XY[n,:]=MX+yy[n]**3
        
    XYZ=np.zeros([len(xx),len(yy),len(zz)])
    for n in range(len(zz)):  
        XYZ[n,:,:]=XY+zz[n]**3
        
    T1,T2,T3=np.where(XYZ==The_number)
    
    if len(T1)>0:
        return xx[T1[0]],yy[T2[0]],zz[T3[0]],1
    else:
        return max(xx),max(yy),max(zz),0

#do the power calculations in advance
def func_check5(xx,yy,zz):

    xx3=[x**3 for x in xx];    MX=np.array(xx3)
    yy3=[y**3 for y in yy];    zz3=[z**3 for z in zz]
        
    XY=np.zeros([len(xx),len(yy)])
    for n in range(len(yy3)):
        XY[n,:]=MX+yy3[n]
        
    XYZ=np.zeros([len(xx),len(yy),len(zz)])
    for n in range(len(zz)):  
        XYZ[n,:,:]=XY+zz3[n]
        
    T1,T2,T3=np.where(XYZ==The_number)
    
    if len(T1)>0:
        return xx[T1[0]],yy[T2[0]],zz[T3[0]],1
    else:
        return max(xx),max(yy),max(zz),0

#use integer to replace float
def func_check6(xx,yy,zz):

    xx3=[x**3 for x in xx];    MX=np.array(xx3)
    yy3=[y**3 for y in yy];    zz3=[z**3 for z in zz]

    XY=np.zeros([len(xx3),len(yy3)],int)   
    for n in range(len(yy3)):
        XY[n,:]=MX+yy3[n]

    XYZ=np.zeros([len(xx3),len(yy3),len(zz3)],int)
    for n in range(len(zz3)):  
        XYZ[n,:,:]=XY+zz3[n]
        
    T1,T2,T3=np.where(XYZ==The_number)
    
    if len(T1)>0:
        return xx[T1[0]],yy[T2[0]],zz[T3[0]],1
    else:
        return max(xx),max(yy),max(zz),0

#change all the for loops to be array operations
def func_check7(xx,yy,zz):
    
    MX=np.array(xx)**3
    MY=np.array(yy)**3
    MZ=np.array(zz)**3
    
    XY=np.zeros([len(xx),len(yy)],int) 
    TT1=XY.copy()+MX # copy will take some time
    TT2=XY.copy()+MY
    XY=TT1+TT2.transpose()

    XYZ=np.zeros([len(xx),len(yy),len(zz)],int)
    TT4=XYZ.copy()+XY
    TT5=XYZ.copy()+MZ
    XYZ=TT4+TT5.transpose()

    T1,T2,T3=np.where(XYZ==The_number)
    
    if len(T1)>0:
        return xx[T1[0]],yy[T2[0]],zz[T3[0]],1
    else:
        return max(xx),max(yy),max(zz),0

#remove some redundent statements
def func_check8(xx,yy,zz):
    
    MX=np.array(xx)**3
    MY=np.array(yy)**3
    MZ=np.array(zz)**3

    TT1=np.zeros([len(xx),len(yy)],int)+MX
    TT2=np.zeros([len(xx),len(yy)],int)+MY
    XY=TT1+TT2.transpose()

    TT4=np.zeros([len(xx),len(yy),len(zz)],int)+XY
    TT5=np.zeros([len(xx),len(yy),len(zz)],int)+MZ
    XYZ=TT4+TT5.transpose()

    T1,T2,T3=np.where(XYZ==The_number)
    
    if len(T1)>0:
        return xx[T1[0]],yy[T2[0]],zz[T3[0]],1
    else:
        return max(xx),max(yy),max(zz),0

#even fewer statements
def func_check9(xx,yy,zz):
    
    MX=np.array(xx)**3
    MY=np.array(yy)**3
    MZ=np.array(zz)**3
    
    XY=np.zeros([len(xx),len(yy)],int)+MX
    XY=XY.transpose()+MY
    
    XYZ=np.zeros([len(xx),len(yy),len(zz)],int)+XY
    XYZ=XYZ.transpose()+MZ

    T1,T2,T3=np.where(XYZ==The_number)
      
    if len(T1)>0:
        return xx[T1[0]],yy[T2[0]],zz[T3[0]],1
    else:
        return max(xx),max(yy),max(zz),0


Limit_Block=5
The_number=42
limit=11

get_result=0
xx0=[i for i in range(-limit,limit)];
yy0=[i for i in range(-limit,limit)];
zz0=[i for i in range(-limit,limit)];

Num_z=0
Num_y=0
Num_x=0

block_shift=[0]
for n in range(1,Limit_Block):
    block_shift.append(n)
    block_shift.append(-n)

for Num_x in block_shift:
    for Num_y in block_shift:
        for Num_z in block_shift:
            #time1=time.time()
            xx=[x+2*limit*Num_x for x in xx0 ]
            yy=[y+2*limit*Num_y for y in yy0 ]
            zz=[z+2*limit*Num_z for z in zz0 ]
            
            # to get the nonzero results. Does this always work?
            # xx=[a for a in xx if a != 0]
            # yy=[a for a in yy if a != 0]
            # zz=[a for a in zz if a != 0]
            
#            print('searching the block: x in [',min(xx),',',max(xx),'),', \
#                 'y in [',min(yy),',',max(yy),'),', \
#                 'z in [',min(zz),',',max(zz),')')

            x,y,z,get_result=func_check9(xx,yy,zz)
            #print("time for one block: %s seconds "%(time.time()-time1)) 
            
            if get_result==1:
                break
        if get_result==1:
            break
    if get_result==1:
        break

    
        
if x**3+y**3+z**3 == The_number:
    print(str(x)+'^3 + '+str(y)+'^3 + '+str(z)+'^3 = ',str(The_number))     
else:
    print("We cannot get the results in range [",-2*limit*Limit_Block,",",2*limit*Limit_Block,")")                
                
print("Time for the whole program --- %s seconds ---"%(time.time()-start_time)) 
