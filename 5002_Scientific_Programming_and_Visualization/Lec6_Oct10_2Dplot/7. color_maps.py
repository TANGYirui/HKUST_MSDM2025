import numpy as np
#import matplotlib.pylab as pl
import matplotlib.pyplot as plt

plt.figure()
x = np.linspace(0, 2*np.pi, 64)
y = np.cos(x) 

#plt.figure()
#plt.plot(x,y)


    
# colors[1,3]=1
# colors[n-1,3]=1

XX=[0,1,2,3,4,5]
XX=[-5,-4,-3,-2,-1,0,1,2,3,4,5]

n = len(XX)

colors = plt.cm.flag(np.linspace(0,1,n))
colors = plt.cm.jet(np.linspace(0,1,n))
# colors = plt.cm.Greys(np.linspace(0,1,n))
# colors = plt.cm.Purples(np.linspace(0,1,n))
# colors = plt.cm.Reds(np.linspace(0,1,n))
# colors = plt.cm.Reds(np.linspace(0.5,1,n))
# colors = plt.cm.bwr(np.linspace(0,1,n))
# colors = plt.cm.seismic(np.linspace(0,1,n))

# for i in range(n):
#     colors[i,3]=1-i/n

for i in range(n):
    plt.plot(x, XX[i]*y, color=colors[i])
    
# for i in range(n):
#     plt.plot(x, XX[i]*y)

plt.title('using colormap to plot many lines with different colors')