from matplotlib import pyplot as plt
import numpy as np

plt.figure()
x1=np.linspace(0,4,5)-0.1
x2=np.linspace(0,4,5)+0.1
x3=np.linspace(0,4,5)
 

plt.bar(x1,[50,40,70,80,20],label="A", color='b',width=.1)
plt.bar(x2,[80,20,20,50,60],label="B", color='r',width=.1)
plt.bar(x3,[70,10,20,30,40],label="C", color='g',width=.1)


plt.plot(x3,[50,40,70,80,20],label="A", color='b')
plt.plot(x3,[80,20,20,50,60],label="B", color='r')
plt.plot(x3,[70,10,20,30,40],label="C", color='g')


plt.legend()

plt.xlabel('Days')
plt.ylabel('Distance (kms)')
plt.title('Information')
plt.show()
