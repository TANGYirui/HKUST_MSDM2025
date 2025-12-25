import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(6,4),dpi=200)
plt.subplot(111,projection='polar')
plt.axis('off')

r = np.arange(50,200,10)
theta = np.linspace(0,2*np.pi,len(r),endpoint=False)

angle_scaler=theta[1]*0.8
plt.bar(theta,r,
        width=angle_scaler, ## width of bars
        # width=r/max(r)*theta[1], ## width of bars
        color=plt.cm.jet(np.linspace(0,1,len(r))),
        bottom=50)

plt.text(3.3,60,'Center',fontsize=14)

for ni in range(len(r)):
    plt.text(theta[ni],r[ni]+65,str(r[ni]),fontsize=10)