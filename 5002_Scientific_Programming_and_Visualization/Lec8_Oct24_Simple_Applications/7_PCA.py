from scipy import misc
import matplotlib.pyplot as plt
#from mpl_toolkits import mplot3d
from numpy import linalg
import numpy as np

num_samples=1000
data=np.zeros([3,num_samples])
for n in range(num_samples):
    data[0,n]=n+np.random.rand()*100
    data[1,n]=n+np.random.rand()*10
    data[2,n]=n+np.random.rand()


data=data/data.max()


data[0,:]=data[0,:]-sum(data[0,:])/num_samples
data[1,:]=data[1,:]-sum(data[1,:])/num_samples
data[2,:]=data[2,:]-sum(data[2,:])/num_samples

x=data[0,:]
y=data[1,:]
z=data[2,:]

plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(x,y,z,'.')


Cov_Mat=data@np.transpose(data)/num_samples

L,PCs=linalg.eigh(Cov_Mat)

PC0=PCs[:,0]
PC1=PCs[:,1]
PC2=PCs[:,2]



# To check the calculations of eigenvalues
# Cov_Mat@PCs[:,0]-L[0]*PCs[:,0]
# Cov_Mat@PCs-PCs@np.diag(L)

def get_line(A,B):
    npoints=100
    x=np.zeros([3,npoints])
    for n in range(npoints):
        x[0,n]=A[0]+(B[0]-A[0])/npoints*n
        x[1,n]=A[1]+(B[1]-A[1])/npoints*n
        x[2,n]=A[2]+(B[2]-A[2])/npoints*n
    return x[0,:],x[1,:],x[2,:]

x1,y1,z1=get_line([0,0,0], PC0*(L[0]**0.2))
x2,y2,z2=get_line([0,0,0], PC1*(L[1]**0.2))
x3,y3,z3=get_line([0,0,0], PC2*(L[2]**0.2))

# x1,y1,z1=get_line([0,0,0],[0,0,1])
# x2,y2,z2=get_line([0,0,0],[1,-1,0])
# x3,y3,z3=get_line([0,0,0],[1,1,0])

ax.plot3D(x1,y1,z1,'r',label='PC0',linewidth=10)
ax.plot3D(x2,y2,z2,'b',label='PC1',linewidth=10)
ax.plot3D(x3,y3,z3,'g',label='PC2',linewidth=10)

# plt.axis('equal')
ax.set_box_aspect([1,1,1])
plt.legend()

phi=45
theta=50
ax.view_init(phi, theta)
#plt.axis('square')
#ax.set_title('phi=30,theta=60')
plt.draw()
