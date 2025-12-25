import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
#
# style.use('ggplot')
# style.use('classic')
# style.use('dark_background')

#print(style.available)

# style.use('Solarize_Light2')

h0=20

t = np.linspace(0, 2, 2001, endpoint=True)
s = 9.81*t**2/2
v = 9.81*t
h = h0-s

##plt.figure()
##plt.show()
##plt.figure(4)
plt.figure(figsize=(8,6), dpi=100) #dpi: dot per inch
###
# the simplest plot
plt.plot(t,h)
plt.plot(t,s)
plt.show()

# # # the simplest plot with legend
# # plt.plot(t,h,label='height')
# # plt.plot(t,s,label='distance')

# # ##set the color, linewidth, linestyle
# # plt.plot(t,h,color=(0,0,1),linewidth=1.5,linestyle='-',marker='o', markersize=20,label='height')
# # # plt.plot(t,h,'bo-',label='height')
# # plt.plot(t,s,'rs:',label='distance')
# # # ##
# # ###show the legend
# # plt.legend()
# # # #plt.legend(loc='center left', frameon=True,fontsize=20)
# # # ## loc could be 
# # # ##        best
# # # ##        upper right
# # # ##        upper left
# # # ##        lower left
# # # ##        lower right
# # # ##        right
# # # ##        center left
# # # ##        center right
# # # ##        lower center
# # # ##        upper center
# # # ##        center
# # # ###
# # #
# #add title for the whole figure
# # plt.title('movement of a falling ball',fontsize=20)

# # #add the description for x axis
# # plt.xlabel('time (s)',fontsize=20)
# # #add the description for y axis
# # plt.ylabel('distance (m)',fontsize=20)

# # # Set x and y limits
# # plt.xlim(0,2)
# # plt.ylim(0,20)
# # # ##
# # # Set x and y ticks
# # plt.xticks(np.linspace(0,2,11,endpoint=True),fontsize=20)
# # plt.yticks(np.linspace(0,20,6,endpoint=True),fontsize=20)
# # plt.yticks([],[])

# # ##turn on the grid
# # plt.grid(which='major',axis='both',color='k',linestyle=':',linewidth=1)
# # #plt.grid(which='major',axis='x',color='k',linestyle=':',linewidth=1)
# # #plt.grid(which='major',axis='y',color='g',linestyle='-',linewidth=2)
# # #
# # #add some text decription in the figure
# # plt.text(0.25, 13, '$h_0=20 m $', fontsize=20, color='red')
# # #
# # #add some text decription in the figure with an arrow
# # plt.annotate('starting point', xy=(0, 20), xytext=(0.24, 16),
# #             arrowprops=dict(facecolor='black', shrink=0,linewidth=0.5),
# #             fontsize=20)
# # #
# plt.show()
# #
