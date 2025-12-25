import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename='file_examples\DOSCAR'
df = pd.read_csv(filename, sep=r'\s+')

# df = pd.read_csv(filename,delimiter=r"\s+")
# delimiter:str, default None;  Alias for sep.

# df = pd.read_csv(filename,delim_whitespace=True)
# delim_whitespace:bool, default False
#     Specifies whether or not whitespace (e.g. ' ' or '    ')
#     will be used as the sep. Equivalent to setting sep='\s+'. 
#     If this option is set to True, nothing should be passed 
#     in for the delimiter parameter.

EF = -2.35

plt.plot([EF-EF,EF-EF],[250,-250],'k')
plt.plot(df['En']-EF,df['up'],'r')
plt.plot(df['En']-EF,-df['dw'],'b')
