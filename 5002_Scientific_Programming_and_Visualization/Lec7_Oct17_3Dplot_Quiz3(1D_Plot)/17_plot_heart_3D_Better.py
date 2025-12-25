from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np
from skimage import measure


# Set up mesh
n = 100

x = np.linspace(-3,3,n)
y = np.linspace(-3,3,n)
z = np.linspace(-3,3,n)
X, Y, Z =  np.meshgrid(x, y, z)

# Create cardioid function 
def f_heart(x,y,z):
    F =  ((-x**2 * z**3 -9*y**2 * z**3/80) +
               (x**2 + 9*y**2/4 + z**2-1)**3)
    return F

# Obtain value to at every point in mesh
vol = f_heart(X,Y,Z) 

# Extract a 2D surface mesh from a 3D volume (F=0)
verts, faces, _,_ = measure.marching_cubes(vol, 0, spacing=(0.1, 0.1, 0.1))



# Create a 3D figure
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
ax.plot_trisurf(verts[:, 0]-5, verts[:,1]-5, faces, verts[:, 2]-5,
                cmap='Spectral', lw=1)

# Change the angle of view and title
ax.view_init(15, -15)

ax.set_title(u"Made with ❤ (XXX and Python)", fontsize=15) # if you have Python 3
# ax.set_title("Love From XXX", fontsize=15)
ax.set_xlim(-3,3)
ax.set_ylim(-3,3)
ax.set_zlim(-3,3)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')


# Show me some love ^^
#plt.show()
X, Z = np.meshgrid(x, z)
Y=np.zeros(X.shape)
F=f_heart(X, Y, Z )
CS = ax.contour(X, F, Z, levels=[0], zdir='y', offset=3)
# plt.axis('off')

# plt.savefig('x.pdf')
# plt.show()
