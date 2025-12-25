import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import style



plt.figure(figsize=(8,6), dpi=100) #dpi: dot per inch

ax1=plt.subplot(2,2,1)

theta=np.linspace(0, 2*np.pi, 100)
rho=1-np.sin(theta)
x=rho*np.cos(theta)
y=rho*np.sin(theta)

ax1.plot(x, y,color='blue',linewidth=4)
ax1.set_aspect('equal', adjustable='box')
plt.title('fat heart',fontsize=20)




ax2=plt.subplot(2,2,2)
ax2.set_aspect('equal', adjustable='box')
x1=np.linspace(0,2,100)
y1=np.sqrt(1-(abs(x1)-1)**2)
x2=np.linspace(-2,0,100)
y2=np.sqrt(1-(abs(x1)-1)**2)

y11=np.arccos(1-abs(x1))-math.pi
y22=np.arccos(1-abs(x2))-math.pi

ax2.plot(x1, y1,color='red',linewidth=4)
ax2.plot(x2, y2,color='red',linewidth=4)
ax2.plot(x1, y11,color='red',linewidth=4)
ax2.plot(x2, y22,color='red',linewidth=4)

plt.title('better heart',fontsize=20)



ax3=plt.subplot(2,2,3)
ax3.set_aspect('equal', adjustable='box')
x1=np.linspace(0,2,100)
y1=np.sqrt(1-(abs(x1)-1)**2)
x2=np.linspace(-2,0,100)
y2=np.sqrt(1-(abs(x1)-1)**2)

y11=np.arccos(1-abs(x1))-math.pi
y22=np.arccos(1-abs(x2))-math.pi

ax3.plot(x1, y1,color='red',linewidth=4)
ax3.plot(x2, y2,color='red',linewidth=4)
ax3.plot(x1, y11,color='red',linewidth=4)
ax3.plot(x2, y22,color='red',linewidth=4)

plt.title('better heart',fontsize=20,x=0.5, y=0.5,color="b",size=14)
plt.axis("off")




ax4=plt.subplot(2,2,4, projection='polar')
ax4.set_aspect('equal', adjustable='box')

theta=np.linspace(0, 2*np.pi, 100)
rho=1-np.sin(theta)

ax4.plot(theta, rho,color='blue',linewidth=4)
plt.title('fat heart',x=0.5, y=0.6,color="b",size=14)
plt.show()