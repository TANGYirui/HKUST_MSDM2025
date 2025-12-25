import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename='file_examples\DOSCAR2'

# # for test
# f = open(filename)
# num_line=10
# nline=0
# while nline<num_line:
#     line = f.readline()
#     print(nline, line)
#     nline += 1
# f.close()

f = open(filename)


# skipping first 4 lines
# l0=f.readline(); l1=f.readline(); 
# l2=f.readline(); l3=f.readline()
nline=0
while nline<4:
    f.readline()
    nline += 1

l4=f.readline(); name=l4.split()

l5  =f.readline(); tmp =l5.split();
Emax = float(tmp[0]);Emin = float(tmp[1])
NEDOS= int(tmp[2]);  EF   = float(tmp[3])

#shorter way
[Emax,Emin,NEDOS,EF,Occu]=map(float,l5.split())
NEDOS=int(NEDOS)

# use list to get the data
DOS = []
for ni in range(NEDOS):
    DOS.append(list(map(float,f.readline().split())))
f.close()

# # use array to get the data
# DOS = np.zeros([NEDOS,5])
# for ni in range(NEDOS):
#     DOS[ni,:]=list(map(float,f.readline().split()))
# f.close()

DOS=np.array(DOS)
DOS[:,0]=DOS[:,0]-EF
# plt.plot(DOS[:,0],DOS[:,1],'r')
# plt.plot(DOS[:,0],-DOS[:,2],'b')

DMax=np.max(DOS[:,1:3]); DMin=np.min(DOS[:,1:3])

# use pandas to do the analysis


# use pandas to do the analysis
DOS=pd.DataFrame(DOS,columns=['En','up','dw','sup','sdw'])
DOS['En']=DOS['En']-EF
DOS=DOS.set_index('En')

plt.plot(DOS['up'],'r')
plt.plot(-DOS['dw'],'b')

DMax=DOS.loc[:,'up':'dw'].max().max()
DMin=DOS.loc[:,'up':'dw'].min().min()


# make the plot look better
EnMax=2; EnMin=-2
plt.xlim([EnMin,EnMax])
plt.ylim([-DMax,DMax])
plt.plot([0,0],[-DMax,DMax],'k')
plt.plot([EnMin,EnMax],[0,0],'k')

