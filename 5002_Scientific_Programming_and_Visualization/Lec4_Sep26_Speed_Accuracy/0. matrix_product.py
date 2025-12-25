import numpy as np
import time
import matplotlib.pyplot as plt

def matrix_product(N):
    C=np.zeros([N,N],float)
    A=np.random.rand(N,N)
    B=np.random.rand(N,N)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i,j] += A[i,k]*B[k,j]

len_matrix=list(range(10,210,10))
time_prod=[]
num_test=5
for N in len_matrix:
    start_time=time.time()
    for nn in range(num_test):
        matrix_product(N)
    time_tmp=time.time()-start_time
    time_prod.append(time_tmp)
    
    print(time_tmp)

ratio=[]
for N,t in zip(len_matrix,time_prod):
    ratio.append(t/N/N/N)

aver_num = 5
if aver_num > len(len_matrix): aver_num = len(len_matrix)
aver_ratio = sum(ratio[-aver_num-1:-1])/aver_num

time_fit=[]
for N in len_matrix:
    time_fit.append(aver_ratio*N*N*N)
    
plt.plot(len_matrix,time_prod,'-*',markersize=10,label='calculated')
plt.plot(len_matrix,time_fit,'-o',markersize=10,label='fitted')

plt.xscale('log'); plt.yscale('log'); plt.legend()