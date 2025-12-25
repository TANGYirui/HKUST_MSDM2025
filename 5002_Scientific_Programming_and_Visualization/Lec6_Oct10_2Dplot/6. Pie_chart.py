import matplotlib.pyplot as plt

plt.figure()
slices = [8,2,8,6]
activities = ['sleeping','eating','working','playing']
cols = ['c','m','y','k']
 
plt.pie(slices[::-1], labels=activities[::-1],
   colors=cols,
  startangle=90,
    shadow= True,
   explode=(0.1,0.,0.,0.),
  autopct='%1.2f%%')
 
plt.title('Pie Plot')
plt.show()