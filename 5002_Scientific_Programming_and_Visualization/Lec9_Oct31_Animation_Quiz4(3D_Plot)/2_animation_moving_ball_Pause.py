import numpy as np
import matplotlib.pyplot as plt

h0=180
v0=10

t = np.linspace(0, 6, 20, endpoint=True)
s = 10*t**2/2
v = v0*t
h = h0-s


t_slice=len(t)

plt.figure(1)
# plt.axis('square')
plt.xlabel('horizontal position')
plt.ylabel('vertical position')
plt.xlim([min(v)-1, max(v)+10])
plt.ylim([-10, max(h)+10])

plt.title('Movement of a ball',color='blue',fontsize=20)
text_step=plt.text(5, 100, 'we begin to plot',color='black',fontsize=20)
plt.text(5, 10, 'horizontal position',color='blue',fontsize=20)
plt.text(40, 160, 'vertical\nposition',color='red',fontsize=20)
plt.pause(1)
# plt.savefig('first.png')

for ni in range(t_slice):
   
    text_step.set_text('time='+str(ni)+'s')
    # plt.text(5, 100, 'time='+str(ni)+'s',color='black',fontsize=20)
    plt.plot(v[ni],h[ni],'ko',markersize=5)
    plt.plot(v[ni],0,'bo',markersize=10,markerfacecolor='none')
    plt.plot(60,h[ni],'ro',markersize=7,markerfacecolor='none')

    
    # plt.savefig(str(ni)+'.png')
    plt.pause(0.4)
    
plt.text(62, 0, 'Hit',color='black',fontsize=20)

# plt.savefig('last.png')


