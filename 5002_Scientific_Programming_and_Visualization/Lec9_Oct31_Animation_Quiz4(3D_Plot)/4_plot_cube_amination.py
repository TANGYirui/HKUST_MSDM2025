from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes(projection='3d',proj_type='ortho')

phi=20
theta=20
ax.view_init(phi, theta)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_box_aspect([1,1,1])



Num_points=10

linear_points = np.linspace(0, 1, Num_points)

Vortex=np.array([[0,0,0],[0,1,0],[1,0,0],[1,1,0],[0,0,1],[0,1,1],[1,0,1],[1,1,1]],float)

for ni in range(8):
    ax.scatter3D(Vortex[ni][0],Vortex[ni][1],Vortex[ni][2],c='r')

num_image=-1

num_image +=1
# plt.savefig(str(num_image)+'.png')

xdata=[]
ydata=[]
zdata=[]
for p1 in (0,3,5,6):
    for p2 in (1,2,4,7):
        line=Vortex[p2]-Vortex[p1]
        if line[0]**2+line[1]**2+line[2]**2 < 1.5:
            for ni in range(1,Num_points-1):
                x,y,z=linear_points[ni]*line+Vortex[p1]
                xdata.append(x)
                ydata.append(y)
                zdata.append(z)

for ni in range(len(xdata)):
    ax.scatter3D(xdata[ni],ydata[ni],zdata[ni],c='b')
    plt.pause(0.001)
    num_image +=1
    # plt.savefig(str(num_image)+'.png')


phi=0
theta=0

for add_phi in np.linspace(0,90,5):
    for add_theta in np.linspace(0,90,5):  
        ax.view_init(phi+add_phi, theta+add_theta)        
        plt.draw()
        plt.pause(0.01)
        num_image +=1
        # plt.savefig(str(num_image)+'.png')

print(num_image)

plt.draw()
