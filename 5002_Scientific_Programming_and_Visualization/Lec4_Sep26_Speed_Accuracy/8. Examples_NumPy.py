# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
Examples of NumPy
"""

import numpy as np
import time
import matplotlib.pyplot as plt

# ###############################################
# #Example 1: test the speed for summation
# ###############################################
# num_A=list(range(1000,3200,200))
# num_test=10

# TT=np.zeros([3,len(num_A)]); NN=0
# for len_A in num_A:
#     A=np.zeros([len_A,len_A],float)
#     A_list=list(A.copy());    
#     C=A.copy()
#     D=np.random.rand(len_A,len_A)
#     D_list=list(D)

#     T=np.zeros([3,num_test])
#     for n in range(num_test):
#         start_time=time.time()  
#         for i in range(len_A):
#             for j in range(len_A):
#                 A[i,j]=A[i,j]+D[i,j]
#         T[0,n]=time.time()-start_time
        
#         start_time=time.time()  
#         for i in range(len_A):
#             for j in range(len_A):
#                 A_list[i][j]=A_list[i][j]+D_list[i][j]
#         T[1,n]=time.time()-start_time
        
#         start_time=time.time()  
#         C=C+D
#         T[2,n]=time.time()-start_time
        
#     TT[:,NN]=T.sum(axis=1)/num_test
#     NN=NN+1

# plt.figure()
# plt.subplot(121)
# plt.plot(num_A[4:],TT[0,4:],'-o',label='A[i,j]=A[i,j]+D[i,j]')
# plt.plot(num_A[4:],TT[1,4:],'-*',label='A_list[i][j]=A_list[i][j]+D_list[i,j]')
# plt.plot(num_A[4:],TT[2,4:],'-^',label='C=C+D')
# plt.xlabel('N'); plt.ylabel('Time'); plt.legend()


# plt.subplot(122)
# plt.plot(num_A[4:],TT[0,4:],'-o',label='A[i,j]=A[i,j]+D[i,j]')
# plt.plot(num_A[4:],TT[1,4:],'-*',label='A_list[i][j]=A_list[i][j]+D_list[i,j]')
# plt.plot(num_A[4:],TT[2,4:],'-^',label='C=C+D')
# plt.xscale('log');plt.yscale('log');

# Fit0=np.polyfit(np.log(num_A[4:]),np.log(TT[0,4:]),1)
# Fit1=np.polyfit(np.log(num_A[4:]),np.log(TT[1,4:]),1)
# Fit2=np.polyfit(np.log(num_A[4:]),np.log(TT[2,4:]),1)

# TT0=Fit0[0]*np.log(num_A[4:])+Fit0[1]
# TT1=Fit1[0]*np.log(num_A[4:])+Fit1[1]
# TT2=Fit2[0]*np.log(num_A[4:])+Fit2[1]

# plt.plot(num_A[4:],np.exp(TT0),'-r',label='slope'+str(round(Fit0[0],3)))
# plt.plot(num_A[4:],np.exp(TT1),'-b',label='slope'+str(round(Fit1[0],3)))
# plt.plot(num_A[4:],np.exp(TT2),'-k',label='slope'+str(round(Fit2[0],3)))

# plt.xlabel('N'); plt.ylabel('Time'); plt.legend()


# # plt.subplot(122)
# # plt.plot(np.log(num_A),np.log(TT[0,:]),'-o',label='A[i,j]=A[i,j]+D[i,j]')
# # plt.plot(np.log(num_A),np.log(TT[1,:]),'-*',label='A_list[i][j]=A_list[i][j]+D_list[i,j]')
# # plt.plot(np.log(num_A),np.log(TT[2,:]),'-^',label='C=C+D')
# # plt.xlabel('log(N)'); plt.ylabel('log(Time)'); plt.legend()


#######################################################
## Example 2: Array Iterating: access all the elements in an array
#######################################################
n1=2;n2=3;n3=4

A1 =np.array([x for x in range(n1)])
A2 =np.array([[x+y*10 for x in range(n1)] for y in range(n2)])
A3 =np.array([[[x+y*10+z*100 for x in range(n1)] 
                for y in range(n2)] 
              for z in range(n2)])

for x in A1:
    print(x)

print()
for x in A2:
    print(x)

print()
for x in A2:
    print(x)
    for y in x:
        print(y)

print()
for x in A3:
    print(x)
    
print()  
   
##https://numpy.org/doc/stable/reference/generated/numpy.nditer.html
for x in np.nditer(A3):
    print(x)
    if x==210:
        print("found it")

for x in np.nditer(A3[:, ::2]):
    print(x)  
# order:{'C', 'F', 'A', 'K'}, optional; Default is ‘K’. 
# Controls the iteration order. ‘C’ means C order, 
# ‘F’ means Fortran order, ‘A’ means ‘F’ order if all the
# arrays are Fortran contiguous, ‘C’ order otherwise, 
# and ‘K’ means as close to the order the array elements 
# appear in memory as possible. This also affects the element memory order 
#of allocate operands, as they are allocated to be compatible with 
# iteration order.    
for x in np.nditer(A3, order='F'):
    print(x)

for idx, x in np.ndenumerate(A3):
    print(idx, x)
    if x==210:
        A3[idx]=200000
    
# #######################################################
# ## Example 3: Joining Array
# #######################################################

arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])
arr_j0 = np.concatenate((arr1, arr2), axis=0)
arr_j1 = np.concatenate((arr1, arr2), axis=1)

print(arr_j0)
print(arr_j1)


arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr_s0 = np.stack((arr1, arr2), axis=0)
arr_s1 = np.stack((arr1, arr2), axis=1)
arr_hs = np.hstack((arr1, arr2))
arr_vs = np.vstack((arr1, arr2))
arr_ds = np.dstack((arr1, arr2))
print(arr_s0)
print(arr_s1)
print(arr_hs)
print(arr_vs)
print(arr_ds)


# #######################################################
# ## Example 4: Splitting Array
# #######################################################

arr = np.array([1, 2, 3, 4, 5, 6])
newarr = np.array_split(arr, 4)

arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18]])
newarr2d_a0 = np.array_split(arr2d, 3)
newarr2d_a1 = np.array_split(arr2d, 3, axis=1)

print(newarr2d_a0) 
print(newarr2d_a1) 


# ########################################################
# ## Example 5: Searching Arrays
# ########################################################

arr = np.array([1, 2, 3, 4, 2, 6])
x = np.where(arr%2 == 0)

# print(x)

# # #The method starts the search from the left and returns the first index
# # # where the number 2.5 is no longer larger than the next value.
# x_s = np.searchsorted(arr, 2.5)
# x_ms = np.searchsorted(arr, [2.5,4.5,6.5])

# ########################################################
# ## Example 6: Sorting Arrays
# ########################################################

arr = np.array([[3,2,4], [5,0,1],[7,9,3]])
print(np.sort(arr,axis=0)) 
print(np.sort(arr,axis=1))

# ind=np.argsort(arr,axis=1)
# print(np.take_along_axis(arr,ind,axis=1))

# #sort based on the first row
# print(arr[:, arr[0].argsort()])

# ########################################################
# ## Example 7: Filter Array
# ########################################################

arr = np.array([41,42,43,44])
x = [True,False,True,False]
newarr = arr[x]
print(newarr) 

filter_arr = arr > 42
print(arr[filter_arr])

filter_arr = arr%2==0
print(arr[filter_arr])


# Create an empty list
filter_arr = []

# go through each element in arr
for element in arr:
  # if the element is completely divisble by 2, set the value to True, otherwise False
  if element % 2 == 0:
    filter_arr.append(True)
  else:
    filter_arr.append(False)

print(arr[filter_arr])









