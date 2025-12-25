import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

Fig1, ax = plt.subplots()

#prepare something you want to update
#the comma after ln is very important, please check the 
#type of return values with and without comma
#plt.plot() return a tuple with only one element
#https://stackoverflow.com/questions/16037494/x-is-this-trailing-comma-the-comma-operator
ln,= plt.plot([], [], 'ro')
#You can also use the following method
# ln= plt.plot([], [], 'ro')[0]
text_step=plt.text(0, 0, 't',color='black',fontsize=20)


#the initializaion function
#A function used to draw a clear frame. 
#If not given, the results of drawing from the first item 
#in the frames sequence will be used. 
#This function will be called once before the first frame.
def init():
    ax.set_xlim(0, 2*np.pi);     ax.set_ylim(-1, 1)
    # return 0
    return ln,text_step
ax.set_xlim(0, 2*np.pi);     ax.set_ylim(-1, 1)

#The function to update what you want to plot
#The function to call at each frame.
#The first argument will be the next value in frames. 
#Any additional positional arguments can be supplied via the fargs parameter.
def replot(t):
    # print(t)
    ln.set_data([t*0.02], [np.sin(t*0.02)]) 
    text_step.set_text('t='+str(t))
    # print(t)
    return ln,text_step

ani = FuncAnimation(fig=Fig1, #which figure you want to update
                    init_func=init,  #the inition function
                    func=replot, #the update function
                    frames=range(100,200),  #Source of data to pass func and each frame of the animation
                    interval=100, #delay between frames in milliseconds, 1000 means 1 second
                    blit=True #only update the plot that changed
                    )
plt.show()
# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
## your system: for more information, see
## http://matplotlib.sourceforge.net/api/animation_api.html
# ani.save('animation_example.mp4', dpi=720, fps=5, extra_args=['-vcodec', 'libx264'])
#
## Set up formatting for the movie files
##Writer = matplotlib.animation.writers['ffmpeg']
##writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
##ani.save('im.mp4', writer=writer)

