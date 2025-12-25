# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
"""

#coding and decoding

from numpy import mod
import numpy as np

def char_table(str,shift):
    all_characters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=[]\;,./~!@#$%^&*()_+{}|:<>? '
    num_char=len(all_characters)
    pos=all_characters.find(str)
    return all_characters[mod(pos+shift,num_char)]       

def coding_decoding(str,codes,coding=1):
    str2=[]
    for ni in range(len(str)):
        str2.append(char_table(str[ni],coding*codes[ni]))
    return str2

# np.random.seed(10)

str1='much better methods'
str1='aaaa'
codes=[]; 
for ni in range(len(str1)):
#    codes.append(len(str1)-ni)
    codes.append(np.random.randint(len(str1)))
#    codes.append(1)

shift=10

str2=coding_decoding(str1,codes,shift)
str3=coding_decoding(str2,codes,-shift)

print("The original message is    --->\n","".join(str1))
print("After coding, message is   --->\n","".join(str2))
print("After decoding, message is --->\n", "".join(str3))

