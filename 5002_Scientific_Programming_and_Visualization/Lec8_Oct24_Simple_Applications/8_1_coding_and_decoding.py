# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
"""

#coding and decoding

from numpy import mod

shift=1
all_characters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=[]\;,./~!@#$%^&*()_+{}|:<>? '
num_char=len(all_characters)
codes={}; decodes={}
for ni in range(num_char):
    codes[all_characters[ni]]=all_characters[(ni+shift)%num_char]
    decodes[all_characters[mod(ni+shift,num_char)]]=all_characters[ni]

str1='we are learning encryption now. Do you understand it? Easy!!!'

# str1='aaaaa'
str2=[];str3=[]
for ni in range(len(str1)):
    str2.append(codes[str1[ni]])

for ni in range(len(str2)):
    str3.append(decodes[str2[ni]])

print("The original message is    --->\n","".join(str1))
print("After coding, message is   --->\n","".join(str2))
print("After decoding, message is --->\n", "".join(str3))

