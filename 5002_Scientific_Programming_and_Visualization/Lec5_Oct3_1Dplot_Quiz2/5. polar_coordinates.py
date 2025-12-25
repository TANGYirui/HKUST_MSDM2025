import numpy as np
import matplotlib.pyplot as plt

#x = []
#y = []
#for theta in np.linspace(0,4*np.pi,1000):
#    r = np.exp(theta/np.pi/2)
#    x.append(r*np.cos(theta))
#    y.append(r*np.sin(theta))
#
#plt.figure()



#plt.subplot(121,projection='polar')
plt.subplot(121,polar=True)

theta = np.arange(-np.pi, 4*np.pi, 0.01)
r = np.exp(theta/np.pi/2)
#r = theta

plt.plot(theta,r)


plt.subplot(122)

x=r*np.cos(theta)
y=r*np.sin(theta)
plt.plot(x,y)

plt.axis('square')
plt.xlim(-5,8)
plt.ylim(-6,4)

plt.show()

