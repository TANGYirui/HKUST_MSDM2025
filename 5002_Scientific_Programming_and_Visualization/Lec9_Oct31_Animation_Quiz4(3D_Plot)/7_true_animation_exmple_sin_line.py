import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig_example, ax = plt.subplots()
# xdata, ydata = [], []

#prepare something you want to update
ln, = plt.plot([], [], 'r.-')
text_step=plt.text(0, 0.5, 't',color='black',fontsize=20)
ax.set_xlim(0, 4*np.pi);     ax.set_ylim(-1, 1)

#the initializaion function
def init():
    return ln,text_step

#The function to update what you want to plot
def replot(t):
    print(t)
    x = np.linspace(0, np.pi*4, 100)
    y = np.sin(x + 0.01 * t*np.pi)
    ln.set_data(x, y)
    text_step.set_text('t='+str(t))
    return ln,text_step

ani = FuncAnimation(fig=fig_example, 
                    init_func=init, 
                    func=replot, 
                    frames=100,  #Source of data to pass func and each frame of the animation
                    interval=100, #delay between frames in milliseconds.
                    blit=True)
plt.show()

# ani.save('animation_sin_line.mp4', 
#           dpi=720,fps=10, 
#           extra_args=['-vcodec', 'libx264'])


# ani.save('animation_sin_line.mp4', 
#           dpi=360,fps=5, 
#           extra_args=['-vcodec', 'libx264'])