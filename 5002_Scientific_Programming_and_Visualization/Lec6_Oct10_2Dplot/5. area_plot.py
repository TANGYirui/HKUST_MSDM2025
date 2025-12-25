import matplotlib.pyplot as plt
days = [1,2,3,4,5]
  
sleeping =[7,8,6,11,7]
eating = [2,3,4,3,2]
working =[7,8,7,2,2]
playing = [8,5,7,8,13]

# playing = [10,5,7,8,13]


# ### old methods
# plt.plot([],[],color='m', label='Sleeping', linewidth=5)
# plt.plot([],[],color='c', label='Eating', linewidth=5)
# plt.plot([],[],color='r', label='Working', linewidth=5)
# plt.plot([],[],color='k', label='Playing', linewidth=5)
# plt.stackplot(days, sleeping,eating,working,playing, colors=['m','c','r','k'])


### better and new method
activities = ['sleeping','eating','working','playing']  
plt.stackplot(days,sleeping,eating,working,playing, colors=['m','c','r','k'],labels=activities)
  
plt.xlabel('days')
plt.xticks(days)
plt.ylabel('hours')
plt.title('Stack Plot')
plt.legend()
plt.show()