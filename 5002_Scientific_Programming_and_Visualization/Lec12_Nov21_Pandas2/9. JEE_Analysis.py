# -*- coding: utf-8 -*-
"""
https://towardsdatascience.com/accessing-data-in-a-multiindex-dataframe-in-pandas-569e8767201d
https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

@author: Junwei Liu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

all_font=sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])

plt.style.use('ggplot')
# plt.rcParams['font.sans-serif']=['SimHei'] # to show Chinese characters
plt.rcParams['font.family'] = 'Microsoft YaHei'
colors= plt.cm.jet(np.linspace(1,0,17))

Pro_choose='Beijing'

filename='file_examples\JEE_simple.xlsx'

Mainland_ori = pd.read_excel(filename,sheet_name='Mainland')
Mainland=Mainland_ori.sort_values('Intake Year').set_index(['Intake Year','JEE Province'])

###Other ways to set index
# Mainland=pd.pivot_table(Mainland,index=['Intake Year','JEE Province'])
# Mainland=Mainland.set_index(['Intake Year','JEE Province'])


## how to get values of index of different levels
Years=Mainland.index.get_level_values('Intake Year').unique()
Name_Pro=Mainland.index.get_level_values('JEE Province').unique()
Name_Un=Mainland.columns

# Num_Un,=Name_Un.shape
Num_Un=Name_Un.shape[0]
colorset={}
for ni in range(Num_Un):
    colorset[Name_Un[ni]]=colors[ni]

# ## select the data based first level index
# Mainland.loc[2017,:]
# ## select the data based other level index
# Mainland.loc[pd.IndexSlice[:,Pro_choose],:]


plt.figure(figsize=[8,8])

def plot_bar_color(x,y,color='r',name=[],shift=0):
    plt.plot([x-0.1,x+0.1],[y,y],color=color)
    if len(name)>0:
        plt.text(x+0.15,y-0.6+shift,name)

for tmp_year in Years:
    cutoffs=Mainland.loc[(tmp_year,Pro_choose)]
    for tmp_un in Name_Un:
        plot_bar_color(tmp_year,cutoffs[tmp_un],colorset[tmp_un])


plt.xticks(list(Years))
plt.xlabel('Intake year')
plt.ylabel('JEE Score')
plt.title(Pro_choose)

for ni in range(Num_Un):
    plot_bar_color(2016,690-ni*3,colorset[Name_Un[ni]],Name_Un[ni])

# plt.savefig(Pro_choose,dpi=800)