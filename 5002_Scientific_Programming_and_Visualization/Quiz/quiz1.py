

from random import randint,seed
import numpy as np
n=20;m=30;p=40;
seed(21227857)
A =[[[randint(-1,1) for x in range(n)] for y in range(m)] for z in range(p)]

# convert to numpy array
A_np = np.array(A)
count_0 = np.sum(A_np == 0)
count_1 = np.sum(A_np == 1)
count_n1 = np.sum(A_np == -1)

# print 
print(f"\nNumber of 0  : {count_0}")
print(f"Number of 1  : {count_1}")
print(f"Number of -1 : {count_n1}")

""" Output:
Number of 0  : 7924
Number of 1  : 7984
Number of -1 : 8092"""

