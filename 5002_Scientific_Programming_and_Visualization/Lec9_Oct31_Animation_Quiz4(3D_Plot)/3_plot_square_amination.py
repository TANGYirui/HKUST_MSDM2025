
import numpy as np
import matplotlib.pyplot as plt

plt.figure()
plt.axis('square')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim([-0.2, 1.2])
plt.ylim([-0.1, 1.3])

Num_points=20
linear_points = np.linspace(0, 1, Num_points)

shift_x=-0.1
shift_y=0.2

Vortex=np.array([[0,0],[0,1],[1,0],[1,1],
                 [shift_x,shift_y],[shift_x,1+shift_y],
                 [1+shift_x,shift_y],[1+shift_x,1+shift_y]])

for ni in (0,1,2,3):
    plt.plot(Vortex[ni][0],Vortex[ni][1],'r*')

num_image=-1

num_image+=1
# plt.savefig(str(num_image)+'.png')

#Example, plot a simple square
num_lines=0
for p1 in (0,3):
    for p2 in (1,2):
        line=Vortex[p2]-Vortex[p1]
        num_lines+=1
        for ni in range(1,Num_points-1):
            x,y=linear_points[ni]*line+Vortex[p1]
            plt.plot(x,y,'b.')
            plt.pause(0.01)
            
            num_image += 1
            # plt.savefig(str(num_image)+'.png')
            

#plot other 2D shapes
for ni in (4,5,6,7):
    plt.plot(Vortex[ni][0],Vortex[ni][1],'r*')
    
for p1 in (4,7):
    for p2 in (5,6):
        line=Vortex[p2]-Vortex[p1]
        num_lines+=1
        for ni in range(1,Num_points-1):
            x,y=linear_points[ni]*line+Vortex[p1]
            plt.plot(x,y,'b.')
            plt.pause(0.01)


for p1 in (0,1,2,3):
    p2=p1+4
    line=Vortex[p2]-Vortex[p1]
    num_lines+=1
    for ni in range(1,Num_points-1):
        x,y=linear_points[ni]*line+Vortex[p1]
        plt.plot(x,y,'b.')
        plt.pause(0.01)

