import numpy as np
import matplotlib.pyplot as plt

h0=20

v0=10

t = np.linspace(0, 2, 20, endpoint=True)
s = 9.81*t**2/2
v = 9.81*t
h = h0-s

l=v0*t


# Create a new figure
# plt.figure()
fig=plt.figure(figsize=(16,8), dpi=100) #dpi: dot per inch

# the first subplot
ax1=plt.subplot(221)
# ax1=plt.subplot(4,3,12)

ax1.plot(l, h, color="blue", linewidth=2.0, linestyle="-.",marker='o')
# plt.plot(l, h, color="blue", linewidth=2.0, linestyle="-.",marker='o')

plt.title('trajectory of a falling ball',fontsize=20)

#set the x axis
plt.xlim(0,max(l))
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off

#set the y axis
plt.ylabel('height (m)',fontsize=20)
plt.ylim(0,20)
plt.yticks(np.linspace(0,20,11,endpoint=True),fontsize=20)



# the second subplot
ax2=plt.subplot(222, sharey=ax1)
# ax2=plt.subplot(222)

plt.plot(t, h, color="blue", linewidth=2.0, linestyle="-",marker='s')

#set x axis
plt.xlabel('time (s)',fontsize=20)
plt.xlim(0,2)
plt.xticks(np.linspace(0,2,11,endpoint=True),fontsize=20)

#set y axis
plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left=False,      # ticks along the bottom edge are off
    right=False,         # ticks along the top edge are off
    labelleft=False) # labels along the bottom edge are off


# the third subplot
ax3=plt.subplot(223,sharex=ax1)

plt.plot(l, t, color="blue", linewidth=2.0, linestyle="-",marker='s')

# Set x axis
plt.xlabel('distance (m)',fontsize=20)
plt.xticks(np.linspace(0,max(l),11,endpoint=True),fontsize=20)

# Set y axis
plt.ylim(0,2)
plt.yticks(np.linspace(0,2,11,endpoint=True),fontsize=20)
plt.ylabel('time (s)',fontsize=20)


# the fourth subplot

ax4=fig.add_axes([0.17,0.34,0.1,0.1])
ax4.plot(s,t,color='green')
plt.xlabel('vertical \n distance (m)',fontsize=10)
plt.ylabel('time (s)',fontsize=10)
plt.show()
