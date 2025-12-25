import numpy as np
import matplotlib.pyplot as plt

# Some example data to display
x = np.linspace(0, 2 * np.pi, 400); y = np.sin(x ** 2)

fig = plt.figure(figsize=(8,6),dpi=100)
axs = fig.add_gridspec(2, 2, hspace=0, wspace=0.1)

ax1=plt.subplot(axs[0,0])
ax1.plot(x, y)

ax2=plt.subplot(axs[0,1],sharey=ax1)
ax2.plot(x*2,  y**2, 'tab:orange')    #Tableau Colors 
plt.tick_params(axis='y', which='both',left=False,right=False, labelleft=False)

ax3=plt.subplot(axs[1,0],sharex=ax1)
ax3.plot(x+1,  -y, 'tab:green')

ax4=plt.subplot(axs[1,1],sharex=ax2,sharey=ax3)
ax4.plot(x + 2, -y**2, 'tab:red')
plt.tick_params(axis='y', which='both',left=False,right=False, labelleft=False)

ax5=fig.add_axes([0.6,0.4,0.25,0.2])

#the comma after ln is very important, please check the 
#type of return values with and without comma
#https://stackoverflow.com/questions/16037494/x-is-this-trailing-comma-the-comma-operator
#ax.plot() returns a list with one element. By adding the comma to 
#the assignment target list, you ask Python to unpack the return value
#and assign it to each variable named to the left in turn.
ln5_no_comma=ax5.plot(x*2, y*0+0.5, 'k')
ln5,=ax5.plot(x*2, y*0+0.5, 'k')
ln5.set_linewidth(5)
ln5.set_dashes([5,4,3,2])

ln6=ax5.plot(x*2, y*0+0.4, 'r',lw=3)[0]  ## taking the first element of return of plot()
ln6.set_alpha(0.9) # set the transparency
for nshift in [-0.3, -0.2, -0.1, 0, 0.1,0.2,0.3, 0.4]:
    ax5.plot(x*2, y*0-nshift, 'r',lw=3,alpha=abs(nshift*2)+0.1)

#Add a centered suptitle to the figure.
fig.suptitle('Sharing x per column, y per row',x=0.5,y=0.92)

fig.savefig('test.png')
plt.savefig('test2.pdf')



