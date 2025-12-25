#coding and decoding

from numpy import mod
from random import random,seed,randrange

def char_table(str,shift):
    all_characters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=[]\;,./~!@#$%^&*()_+{}|:<>? '
    num_char=len(all_characters)
    pos=all_characters.find(str)
    return all_characters[mod(pos+shift,num_char)]       

def coding_decoding(str,codes,coding=1):
    str2=[]    
    full_codes=codes
    if len(str)>len(codes):
        N_codes=len(codes)
        for ni in range(N_codes,len(str)):
            full_codes.append(codes[mod(ni,N_codes)])
    for ni in range(len(str)):
        str2.append(char_table(str[ni],coding*full_codes[ni]))
    return str2

#str1='I love hkust when i was a 7-year old child!'
str1='aaaaaaaaaaaa'
key=123
seed(key)
codes=[]; 
codes_len=len(str1);
codes_range=1000;
for ni in range(codes_len):
    codes.append(randrange(codes_range))

#codes=[1]
str2=coding_decoding(str1, codes,1)
str3=coding_decoding(str2, codes,-1)

print("The original message is    --->\n","".join(str1))
print("After coding, message is   --->\n","".join(str2))
print("After decoding, message is --->\n", "".join(str3))
