import numpy as np
import matplotlib.pyplot as plt

num_points=40
radius=10
alpha=np.linspace(0,np.pi*2,num_points,endpoint=True)
x=np.zeros(num_points,float)
y=np.zeros(num_points,float)
for ni in range(num_points):
    x[ni]=radius*np.cos(alpha[ni])
    y[ni]=radius*np.sin(alpha[ni])

plt.figure()
plt.axis('square')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim([int(min(x)-1.1), int(max(x)+1.1)])
plt.ylim([int(min(y)-1.1), int(max(y)+1.1)])

# plt.plot(x,y,'r.')

x_num=len(x)
for ni in range(x_num):
    plt.title(['step=', ni],color='blue',fontsize=20)    
    plt.plot(x[ni],y[ni],'-ro',markersize=5)
    plt.savefig(str(ni)+'.png')
    plt.pause(0.5)

plt.title('we begin to plot',color='blue',fontsize=20)
text_step=plt.text(1, -0.1, 'we begin to plot',color='blue',fontsize=20)

plt.savefig('first.png')

text_step.set_text('Done')
plt.title('Done',color='blue',fontsize=20)

plt.savefig('last.png')

#
