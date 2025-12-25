import matplotlib.pyplot as plt
# axes=plt.subplot(111)
# plt.plot([1,5],[2,3])
# plt.xlabel("X-axis")
# plt.ylabel("Y-axis")

# # axes.set_aspect(1)
# # plt.show()

fig=plt.figure()
# plt.subplot(111)
plt.plot([1,5],[2,2])
plt.plot([1,5],[6,6])
plt.plot([1,1],[2,6])
plt.plot([5,5],[2,6])

plt.plot([1,5],[2,6])
plt.plot([1,5],[6,2])
plt.plot([0,6],[4,4])
plt.xlabel("X-axis")
plt.ylabel("Y-axis")



axes=plt.gca() ###Get the current Axes

# set_aspect: {'auto', 'equal'} or num. 
# axes.set_aspect(1)
# axes.set_aspect(7,adjustable='datalim')
# axes.set_aspect('equal')

# In constrain the aspect ratio, we can use plt.axis() method. There are six major types of parameters: Scaled, Equal, tight, auto, image, square.
# Scaled: This parameter Scales both the axis equally. This means you can draw a perfect circle in your plot box. All the outlier data points will be scaled accordingly to show them.
# Equal: This parameter changes axis limits to equalize both the scaling. Instead of the scale, we need to use it equally in our code to get this all.
# Tight: This parameter Disables auto-scaling and sets the limit so that you can view all the points in your graphs. It also includes outliers. 
# AUTO: This parameter auto-scales both the axes.
# IMAGE: This parameter Scales so that your data limits equal to axis limits.
# SQUARE: This parameter forces the plot to become square. This means that both the x and y axes have the same length.


# ### try others:"Scaled, equal, tight, auto, image, square". 
# plt.axis('Image')
# plt.axis('Equal')
# plt.axis('tight')
# plt.axis('square')
# plt.show()