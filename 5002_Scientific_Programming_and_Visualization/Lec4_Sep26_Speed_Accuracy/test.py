import numpy as np
import time

# a=2**100
# b=2
# c=1
# d=3.0

# e=a+b-c-a
# f=a-a+b-c
# g=a+b-d-a 
# # gives 0.0 because of numerical instability
# # a+b 约等于 a (因为 a 远大于 b)
# h=a-a+b-d

# print(type(a))
# print(type(b))
# print(type(c))
# print(type(d))
# print(e)
# print(f)
# print(g)
# print(h)


A = np.ones([3, 4], float)  
print(A) 

A = np.empty([2, 2])  
print(A)

A = np.diag([1, 2, 3])  
print(A) 

A = np.arange(0, 5, 1)  
print(A) 

A = np.linspace(0, 1, 5)  
print(A) 

import time
B=np.zeros(100000000) 
B[100]=2; B[-100]=3; A=list(B); 

tst=3; #how about tst=2 or 1??
st=time.time(); tst in A; print(time.time()-st)
st=time.time(); tst in B; print(time.time()-st)
st=time.time(); (B==tst).any(); 
print(time.time()-st)
