import matplotlib.pyplot as plt
import numpy as np
x = [1,1.5,2,2.5,3,3.5,3.6]
y = [7.5,8,8.5,9,9.5,10,10.5]
 
x1=[8,8.5,9,9.5,10,10.5,11]
y1=[3,3.5,3.7,4,5,7,8]
 
# plt.scatter(x,y, label='high income low saving',color='r')
plt.figure()
plt.subplot(121)
S1=plt.scatter(x, y, c=y, cmap='Spectral',label='A')
S2=plt.scatter(x1,y1,s=np.array(y1)*30,label='B',color='b')
plt.xlabel('saving')
plt.ylabel('income')
plt.title('Scatter()')
plt.legend()
plt.show()

plt.subplot(122)
plt.plot(x,y, 'r.', markersize=12,label='A')
plt.plot(x1,y1,'b.',label='B')

plt.xlabel('saving')
plt.ylabel('income')
plt.title('Plot()')
plt.legend()
plt.show()