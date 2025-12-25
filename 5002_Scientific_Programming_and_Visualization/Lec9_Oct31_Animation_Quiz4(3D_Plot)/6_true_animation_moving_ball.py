import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation

fig, ax = plt.subplots()


plt.title('Movement of a ball',color='blue',fontsize=20)
plt.text(5, 10, 'horizontal position',color='blue',fontsize=20)
plt.text(40, 160, 'vertical\nposition',color='red',fontsize=20)

#the comma after ln is very important
ln1, = plt.plot([], [], 'ko', animated=True)
ln2, = plt.plot([], [], 'bo', mfc='none', animated=True)
ln3, = plt.plot([], [], 'ro', mfc='none', animated=True)
text_step=plt.text(5, 100, '',color='black',fontsize=20)


ax.set_xlim(-5, 70)
ax.set_ylim(-10, 200)

def init():
    
    return ln1,ln2,ln3,text_step

# update function.  This is called sequentially
h0=180
v0=10
def update(t):
    print(t)
    text_step.set_text('t='+str(int(t*10)/10))
    s = 10*t**2/2
    h = h0-s
    l=v0*t
    ln1.set_data([l],[h])
    ln2.set_data([l],[0])
    ln3.set_data([60],[h])
    return ln1,ln2,ln3,text_step

# call the animator.  blit=True means only re-draw the parts that have changed.
ani = FuncAnimation(fig=fig, func=update, frames=np.linspace(0, 6, 100, endpoint=True),
                    interval=10,
                    init_func=init, blit=True)

plt.show()

#ani.save('animation_moving_ball.mp4', dpi=720, fps=10, extra_args=['-vcodec', 'libx264'])
