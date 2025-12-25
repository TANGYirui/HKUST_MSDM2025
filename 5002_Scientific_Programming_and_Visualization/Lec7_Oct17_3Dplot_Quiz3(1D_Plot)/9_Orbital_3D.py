import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits import mplot3d

epsilon=10E-10
Z=1
N=3

def func_dxy(x,y,z):    
    r=np.sqrt(x**2+y**2+z**2)
    if r<epsilon:
        return 0
    rho=2*Z*r/N
    
    R3d=1/9/np.sqrt(30)*rho**2*Z**3/2*np.exp(-rho/2)
    Y3dxy=np.sqrt(60/4)*x*y/r**2*np.sqrt(1/4/np.pi)
    return Y3dxy*R3d
    
def func_px(x,y,z):
    r=np.sqrt(x**2+y**2+z**2)
    if r<epsilon:
        return 0

    rho=2*Z*r/N
    R2p=(1/2/np.sqrt(6))*rho*Z**3/2*np.exp(-rho/2)
    Y2px=np.sqrt(3)*x/r/np.sqrt(4*np.pi)

    return R2p*Y2px
    

x_min=-20; x_max=20; z=0
y_min=-20; y_max=20

num_x=50; num_y=50
dxy=np.zeros([num_x,num_y],float); 
xx=np.zeros([num_x,num_y],float); yy=np.zeros([num_x,num_y],float)
px=np.zeros([num_x,num_y],float); 
colors=np.zeros([num_x,num_y],dtype=str); 
colortuple=('r','b','y','g')
for nx in range(num_x):
    for ny in range(num_y):
        xx[nx,ny]=nx/(num_x-1)*(x_max-x_min)+x_min
        yy[nx,ny]=ny/(num_y-1)*(y_max-y_min)+y_min
        dxy[nx,ny]=func_dxy(nx/(num_x-1)*(x_max-x_min)+x_min,ny/(num_y-1)*(y_max-y_min)+y_min,z)
        px[nx,ny]=func_px(nx/(num_x-1)*(x_max-x_min)+x_min,ny/(num_y-1)*(y_max-y_min)+y_min,z)
        colors[nx,ny] = colortuple[(nx + ny)%len(colortuple)]

fig = plt.figure()
ax=plt.axes(projection='3d',proj_type='ortho')
#ensure the aspect is correct
ax.set_box_aspect([1,1,1])

# # Example0
# ax.plot_surface(xx, yy, px, rstride=1, cstride=1, cmap='jet', edgecolor='none')
# # ax.plot_surface(xx.T, yy.T, px, rstride=1, cstride=1, cmap='jet', edgecolor='none')


# # Example1.1
# ax.contour3D(xx,yy,px,50)
# # ax.contour3D(xx,yy,px,50,cmap=cm.coolwarm)
# ax.set_title('3D contour plot for px orbital')

# # Example1.2
# ax.contour3D(xx,yy,px,50,zdir='z',offset=0.04,cmap=cm.coolwarm)
# ax.set_title('2D contour plot in xy(z=0.04) plane in 3D')

# # Example1.3
# ax.contour3D(xx,yy,px,50,zdir='x',offset=20,cmap=cm.coolwarm)
# ax.set_title('2D contour plot in yz(x=10) plane in 3D')

# ax.contour3D(xx,yy,px,50,zdir='y',offset=-20,cmap=cm.coolwarm)
# ax.set_title('2D contour plot in yz(x=10) plane in 3D')

# Example2.1
# ax.plot_wireframe(xx, yy, px, color='grey')
# ax.set_title('wireframe of px orbital')
# #
# # Example2.2
# ax.plot_surface(xx, yy, px, cmap='jet', edgecolor='k')
# ax.set_title('plot_surface of px orbital')

# # # Example2.3
# ax.plot_surface(xx, yy, px, rstride=5, cstride=1, cmap='jet', edgecolor='k')
# ax.set_title('rstride=5')
# #
# ## Example2.4
# ax.plot_surface(xx, yy, px, rstride=4, cstride=4, cmap='jet', edgecolor='none')
# ax.set_title('rstride=4, cstride=4')

# # Example2.5
# ax.plot_surface(xx, yy, px, facecolors=colors, linewidth=0,shade=False)
# ax.set_title('change facecolors')

# #practice1
# # ax.plot_wireframe(xx, yy, px, color='grey')
# ax.plot_surface(xx, yy, px,  cmap='jet', linewidth=0,shade=False)
# ax.contour3D(xx,yy,px,50,zdir='z',offset=0.045,cmap=cm.coolwarm)
# ax.contour3D(xx,yy,px,50,zdir='x',offset=22,cmap=cm.coolwarm)
# ax.contour3D(xx,yy,px,50,zdir='y',offset=22,cmap=cm.coolwarm)
# ax.set_title('combination of different plots')

#practice2
ax.contour3D(xx,yy,dxy,20,zdir='z',offset=-0.01,cmap=cm.coolwarm)
ax.contour3D(xx,yy,dxy,20,zdir='z',offset=-0.01)
ax.contour3D(xx,yy,dxy,100)


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

phi=40
theta=80
ax.view_init(phi, theta)
plt.draw()
