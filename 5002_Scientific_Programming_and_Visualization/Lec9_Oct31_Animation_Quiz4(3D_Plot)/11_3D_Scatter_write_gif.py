import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter 

# Define Data


data = np.random.random(size=(10,3))
df = pd.DataFrame(data, columns=["x","y","z"])

# Create Figure


fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

# Plot Graph


scatter_plot = ax.scatter3D([],[],[], color='m')

# Define Update function


def update(i):
    # scatter_plot._offsets3d = (i,i,i)
    scatter_plot._offsets3d = (df.x.values[:i], df.y.values[:i], df.z.values[:i])

# Set annimation


ani = FuncAnimation(fig, update, frames=len(df), interval=50)


# Show


plt.tight_layout()
plt.show()

# Save


# ani.save('3D Scatter Animation.gif', writer='pillow', fps=30)