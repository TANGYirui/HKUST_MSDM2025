#A Mobius strip is similar to a strip of paper glued into a loop with a half-twist. 
#Topologically, it's quite interesting because despite appearances it has only a single side!
#Here we will visualize such an object using Matplotlib's three-dimensional tools. 
#The key to creating the Mobius strip is to think about it's parametrization: 
#it's a two-dimensional strip, so we need two intrinsic dimensions. 

from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt


theta = np.linspace(0, 2 * np.pi, 30)
w = np.linspace(-0.25, 0.25, 8)
w, theta = np.meshgrid(w, theta)



#Now from this parametrization, we must determine the (x, y, z) positions of the embedded strip.

#Thinking about it, we might realize that there are two rotations happening: one is the position 
#of the loop about its center (what we've called θ), 
#while the other is the twisting of the strip about its axis (we'll call this ϕ). 
#For a Mobius strip, we must have the strip makes half a twist during a full loop, or Δϕ=Δθ/2.

phi = 0.5 * theta

#Now we use our recollection of trigonometry to derive the three-dimensional embedding. 
#We'll define r, the distance of each point from the center, and use this to find the embedded (x,y,z) coordinates:

# radius in x-y plane
r = 1 + w * np.cos(phi)

x = np.ravel(r * np.cos(theta))
y = np.ravel(r * np.sin(theta))
z = np.ravel(w * np.sin(phi))


#Finally, to plot the object, we must make sure the triangulation is correct. 
#The best way to do this is to define the triangulation within the underlying parametrization, 
#and then let Matplotlib project this triangulation into the three-dimensional space of the Möbius strip. 
#This can be accomplished as follows:

# triangulate in the underlying parametrization
from matplotlib.tri import Triangulation
tri = Triangulation(np.ravel(w), np.ravel(theta))

ax = plt.axes(projection='3d')
ax.plot_trisurf(x, y, z, triangles=tri.triangles,
                cmap='viridis', linewidths=0.2);

ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1);

