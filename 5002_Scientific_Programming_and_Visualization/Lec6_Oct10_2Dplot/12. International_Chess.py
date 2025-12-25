# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:34:12 2019

@author: Junwei Liu
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

plt.figure()
# startcolor=(1,1,1);
# midcolor=(1,1,1);
# endcolor=(247/255, 220/255, 111/255);
# my_cmap = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap',[startcolor,midcolor,endcolor],5)

# startcolor=(0,1,0);
# startcolor=(1,1,1);
startcolor=(0,0,0);
midcolor=(1,1,1);
endcolor=(247/255, 220/255, 111/255);
# endcolor=(1, 0, 0);
# endcolor=(211/255, 84/255, 0/255);
my_cmap = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap',[startcolor,midcolor,endcolor],4)



num_x=8; num_y=8
pannel=np.zeros([num_x,num_y],float); 
for nx in range(num_x):
    for ny in range(num_y):
        if (nx+ny)%2==1:
            # pannel[nx,ny]=nx+ny
            pannel[nx,ny]=1

# plt.imshow(pannel)
# plt.imshow(pannel,cmap=my_cmap,interpolation='bicubic')
plt.imshow(pannel,cmap=my_cmap)

plt.xticks(np.linspace(0,9,8,endpoint=False),
            ('a','b','c','d','e','f','g','h'),fontsize=20)
plt.xlim([-0.5,7.5])
#plt.xlim([0,8])
plt.yticks(np.linspace(0,9,8,endpoint=False),
            ('1','2','3','4','5','6','7','8'),fontsize=20)
plt.ylim([-0.5,7.5])
#plt.xlabel(['a','b'])
plt.tick_params(bottom=False, left=False,labeltop=True,labelright=True,
               labelbottom=False,labelleft=False)

