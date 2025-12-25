from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

# ax = plt.axes(projection='3d')#,proj_type='ortho')
ax = plt.axes(projection='3d',proj_type='ortho')
# #ensure the aspect is correct, while it does not work as expected
# ax.set_box_aspect([1,1,1])
#you need to fine-tune the aspect ratio
ax.set_box_aspect([1,1,2]) ## why is it 2 for z direction?

Num_points=41
#parameters of the cube
len_edge=10
center_cube=[10,20,30]
#paramethers of the sphere
center_sphere=[10,20,40]
radius=5



#plot the interface between sphere and cubic
Plane_XX, Plane_YY= np.meshgrid(np.linspace(0, 1, Num_points),np.linspace(0, 1, Num_points))
ax.plot_surface(Plane_XX*len_edge+center_cube[0]-len_edge/2, 
                Plane_YY*len_edge+center_cube[1]-len_edge/2, 
                Plane_YY*0+center_cube[2]+len_edge/2, color='y',edgecolor='none',shade=False)

#plot the cube with center at center_sub

linear_points=np.linspace(0, 1, Num_points)
const1=linear_points*0+len_edge/2
const2=linear_points*0-len_edge/2
line=linear_points*len_edge-len_edge/2
height1=-len_edge/2
height2=len_edge/2

ax.scatter(center_cube[0],center_cube[1],center_cube[2],c='r',marker='*')

ax.plot(const1+center_cube[0], line+center_cube[1], height1+center_cube[2], zdir='z',c='b')
ax.plot(const2+center_cube[0], line+center_cube[1], height1+center_cube[2], zdir='z',c='b')
ax.plot(line+center_cube[0], const1+center_cube[1], height1+center_cube[2], zdir='z',c='b')
ax.plot(line+center_cube[0], const2+center_cube[1], height1+center_cube[2], zdir='z',c='b')

ax.plot(const1+center_cube[0], line+center_cube[1], height2+center_cube[2], zdir='z',c='b')
ax.plot(const2+center_cube[0], line+center_cube[1], height2+center_cube[2], zdir='z',c='b')
ax.plot(line+center_cube[0], const1+center_cube[1], height2+center_cube[2], zdir='z',c='b')
ax.plot(line+center_cube[0], const2+center_cube[1], height2+center_cube[2], zdir='z',c='b')

ax.plot(const1+center_cube[1], line+center_cube[2], height2+center_cube[0], zdir='x',c='b')
ax.plot(const2+center_cube[1], line+center_cube[2], height2+center_cube[0], zdir='x',c='b')
ax.plot(const1+center_cube[1], line+center_cube[2], height1+center_cube[0], zdir='x',c='b')
ax.plot(const2+center_cube[1], line+center_cube[2], height1+center_cube[0], zdir='x',c='b')


#plot the sphere with center at center_sphere
u = np.linspace(0, 2 * np.pi, Num_points)
v = np.linspace(0, np.pi, Num_points)

XX=np.zeros([Num_points,Num_points],float)
YY=np.zeros([Num_points,Num_points],float)
ZZ=np.zeros([Num_points,Num_points],float)

nnu=-1
for nu in u:
    nnu=nnu+1
    nnv=-1
    for nv in v:
        nnv=nnv+1
        XX[nnu,nnv]=np.sin(nv)*np.sin(nu)*radius+center_sphere[0]
        YY[nnu,nnv]=np.sin(nv)*np.cos(nu)*radius+center_sphere[1]
        ZZ[nnu,nnv]=np.cos(nv)*radius+center_sphere[2]

ax.plot_surface(XX, YY, ZZ, color='r',edgecolor='k',shade=True)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

theta=20
alpha=30
ax.view_init(theta, alpha)


plt.axis('off')
plt.draw()


