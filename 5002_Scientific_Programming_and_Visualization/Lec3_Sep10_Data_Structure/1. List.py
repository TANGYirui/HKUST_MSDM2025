####1. Be careful when you use a list to be the element, there might unexpected errors

##test the 1D list
T=[0,-1,2,-3,4]

## map function
Map_T=map(abs,T)
Map_T=list(map(abs,T))

def square(x):
    return x**2
Map_T=list(map(square,T))

# Using lambda function
Lambda_T=list(map(lambda x: x ** 2, T))

### example of lambda function
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))



T=[0,-1,2,-3,4]

B=T ###test 1
C=T.copy() ##test 2
D=T[:] ##test 3

print('\ncommand: B=T; C=T.copy(); D=T[:]')


print('id(T)=',id(T),', id(T[0])=',id(T[0]),', id(T[1])=',id(T[1]),', id(T[2])=',id(T[2]))
print('id(B)=',id(B),', id(B[0])=',id(B[0]),', id(B[1])=',id(B[1]),', id(B[2])=',id(B[2]))
print('id(C)=',id(C),', id(C[0])=',id(C[0]),', id(C[1])=',id(C[1]),', id(C[2])=',id(C[2]))
print('id(D)=',id(D),', id(D[0])=',id(D[0]),', id(D[1])=',id(D[1]),', id(D[2])=',id(D[2]))

print()
print('T=',T)
print('B=',B)
print('C=',C)
print('D=',D)

T[0:5]=[1,1,1,1,1]
print('\nafter T[0:5]=[1,1,1,1,1]')
print('T=',T)
print('B=',B)
print('C=',C)
print('D=',D)

T=[2,2,2,2,2]
print('\nafter T=[2,2,2,2,2]')
print('id(T)=',id(T),', id(T[0])=',id(T[0]),', id(T[1])=',id(T[1]),', id(T[2])=',id(T[2]))
print('T=',T)
print('B=',B)
print('C=',C)
print('D=',D)

##test the 2D list
import copy
print()
T2=[0,1,2,3,4]

B2=[None,None]
B2[0]=T2
B2[1]=T2.copy()
B2.append(T2)

C2=B2.copy()
D2=B2[:]
E2=B2
F2=copy.copy(B2)
G2=copy.deepcopy(B2)

print('B2=[None,None]; B2[0]=T2.copy(); B2[1]=T2; B2.append(T2)')
print('C2=B2.copy(); D2=B2[:]; E2=B2')
print('\nid(T2)=',id(T2))
print('id(B2)=',id(B2),', id(B2[0])=',id(B2[0]),', id(B2[1])=',id(B2[1]),', id(B2[2])=',id(B2[2]))
print('id(C2)=',id(C2),', id(C2[0])=',id(C2[0]),', id(C2[1])=',id(C2[1]),', id(C2[2])=',id(C2[2]))
print('id(D2)=',id(D2),', id(D2[0])=',id(D2[0]),', id(D2[1])=',id(D2[1]),', id(D2[2])=',id(D2[2]))
print('id(E2)=',id(E2),', id(E2[0])=',id(E2[0]),', id(E2[1])=',id(E2[1]),', id(E2[2])=',id(E2[2]))
print('id(F2)=',id(F2),', id(F2[0])=',id(F2[0]),', id(F2[1])=',id(F2[1]),', id(F2[2])=',id(F2[2]))
print('id(G2)=',id(G2),', id(G2[0])=',id(G2[0]),', id(G2[1])=',id(G2[1]),', id(G2[2])=',id(G2[2]))

print()
print('T2=',T2)
print('B2=',B2)
print('C2=',C2)
print('D2=',D2)
print('E2=',E2)
print('F2=',F2)
print('G2=',G2)

print()
T2[0:5]=[1,1,1,1,1]
D2[0][2]="*";C2[1][0]="#";
#T2=[1,1,1,1,1]
print('after T2[0:5]=[1,1,1,1,1];D2[0][2]="*";C2[1][0]="#";')
print('T2=',T2)
print('B2=',B2)
print('C2=',C2)
print('D2=',D2)
print('E2=',E2)
print('F2=',F2)
print('G2=',G2)


#####################################################
###### test list size
#####################################################

import sys
import matplotlib.pyplot as plt

a=1
print(a.__sizeof__())
print(sys.getsizeof(1))

a=[1]
print(a.__sizeof__())
print(sys.getsizeof(a))

b=['sjdfosajfsaodfsaojdfsjaodfjasdfjso']
print(sys.getsizeof(b)-sys.getsizeof(a))
# sys.getsizeof only takes account of the list itself, not items it contains.

test_list=[]
size_l=[]
mem_l=[]
size_l.append(len(test_list))
mem_l.append(sys.getsizeof(test_list))
print(sys.getsizeof(test_list))
for n in range(100):
    test_list.append(n)
    # print(list_size)
    # print(id(list_size),sys.getsizeof(list_size))
    size_l.append(len(test_list))
    mem_l.append(sys.getsizeof(test_list))
    
plt.plot(size_l,mem_l,'*-')
plt.xlabel('size of list'); plt.ylabel('Memory used')




