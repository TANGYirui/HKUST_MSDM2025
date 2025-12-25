# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
Check the complexity in practice
"""
import time
import numpy as np
import matplotlib.pyplot as plt

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
    TT1=XY.copy()+MX
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

#list might be faster. Do the test
def func_check10(xx,yy,zz):
    
    xx3=[x**3 for x in xx]
    yy3=[y**3 for y in yy]
    zz3=[z**3 for z in zz]
    
    XY=np.zeros([len(xx),len(yy)],int)+xx3
    XY=XY.transpose()+yy3
    
    XYZ=np.zeros([len(xx),len(yy),len(zz)],int)
    for n in range(len(zz)):  
        XYZ[n,:,:]=XY+zz3[n]

    T1,T2,T3=np.where(XYZ==The_number)
    
    if len(T1)>0:
        return xx[T1[0]],yy[T2[0]],zz[T3[0]],1
    else:
        return max(xx),max(yy),max(zz),0

The_number=13

num_test=1

NN=list(range(20,220,20))
Num_limit=len(NN)

TT=np.zeros([11,Num_limit,num_test])

N_limit=-1
for limit in NN:
    
    print('limit=',limit)

    xx=list(range(-limit,limit))
    yy=list(range(-limit,limit))
    zz=list(range(-limit,limit))
    
    N_limit=N_limit+1
    for n in range(num_test):    
        # start_time=time.time()
        # func_check2(xx,yy,zz)
        # TT[2,N_limit,n]=time.time()-start_time     
        
        # start_time=time.time()
        # func_check6(xx,yy,zz)
        # TT[6,N_limit,n]=time.time()-start_time        
      
        # start_time=time.time()
        # func_check9(xx,yy,zz)
        # TT[9,N_limit,n]=time.time()-start_time
        
        # start_time=time.time()
        # func_check10(xx,yy,zz)
        # TT[10,N_limit,n]=time.time()-start_time
        for nf in [2,6,9,10]:
            start_time=time.time()
            run_str='func_check'+str(nf)+'(xx,yy,zz)'
            eval(run_str) ## example of using eval()
            TT[nf,N_limit,n]=time.time()-start_time     
            


# plt.figure()

TTT=np.zeros([11,Num_limit])
for n_f in range(11):
    for n_l in range(Num_limit):
        TTT[n_f,n_l]=sum(TT[n_f,n_l,:])/num_test

#############      
#plt.figure()
#plt.plot(NN,TTT[6,:],'-*',label='Func_check6')
#plt.plot(NN,TTT[7,:],'-^',label='Func_check7')
#plt.plot(NN,TTT[8,:],'-s',label='Func_check8')
#plt.plot(NN,TTT[9,:],'-o',label='Func_check9')
#plt.xlabel('N')
#plt.ylabel('Time')
#plt.legend()

############
plt.figure()
plt.plot(np.log(NN),np.log(TTT[2,:]),'-o',label='Func_check2')
plt.plot(np.log(NN),np.log(TTT[6,:]),'-*',label='Func_check6')
plt.xlabel('log(N)')
plt.ylabel('log(Time)')
plt.legend()


############
plt.figure()
plt.plot(NN,TTT[2,:],'-o',label='Func_check2')
plt.plot(NN,TTT[6,:],'-*',label='Func_check6')
plt.xlabel('N')
plt.ylabel('Time')
plt.legend()

############
plt.figure()
plt.plot(NN,TTT[2,:],'-o',label='Func_check2')
plt.plot(NN,TTT[6,:],'-*',label='Func_check6')
plt.xlabel('N')
plt.ylabel('Time')
plt.xscale('log')
plt.yscale('log')


T2_poly=np.polyfit(NN,TTT[2,:],4)
T6_poly=np.polyfit(NN,TTT[6,:],4)

T2_linear=np.polyfit(np.log(NN),np.log(TTT[2,:]),1)
T6_linear=np.polyfit(np.log(NN),np.log(TTT[6,:]),1)



T2_fit=T2_linear[1]+np.log(NN)*T2_linear[0]
T6_fit=T6_linear[1]+np.log(NN)*T6_linear[0]

plt.plot(NN,np.exp(T2_fit),'-r',label='slope'+str(round(T2_linear[0],3)))
plt.plot(NN,np.exp(T6_fit),'-b',label='slope'+str(round(T6_linear[0],3)))
plt.legend()

plt.show()
