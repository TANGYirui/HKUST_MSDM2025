# -*- coding: utf-8 -*-
"""
@author: Junwei Liu
"""

from numpy import mod
from random import random,seed,randrange

def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def find_gcd(a,b):
    gcd = 0
    while b != 0:
        gcd=b
        b=a%b
        a=gcd
    return gcd

def generate_key(p,q):
    n=p*q    
    phi=(p-1)*(q-1)
    e=randrange(2,phi-1)
    while find_gcd(e,phi) > 1:
        e=randrange(2,phi-1) 
#    #you can improve this part for large p and q, now it is very inefficient
#    for m in range(n):
#        if (phi*m+1)%e==0:
#            d=(phi*m+1)/e
#            print("get the private key")
#            break
#   #you can use extended Euclidean algorithm to get the private key
    r,d1,y=xgcd(e,phi)
    d1=d1%phi
    
    return n,e,int(d1)

# p=106697219132480173106064317148705638676529121742557567770857687729397446898790451577487723991083173010242416863238099716044775658681981821407922722052778958942891831033512463262741053961681512908218003840408526915629689432111480588966800949428079015682624591636010678691927285321708935076221951173426894836169;
# q=144819424465842307806353672547344125290716753535239658417883828941232509622838692761917211806963011168822281666033695157426515864265527046213326145174398018859056439431422867957079149967592078894410082695714160599647180947207504108618794637872261572262805565517756922288320779308895819726074229154002310375209;

#p=977
#q=571

p=13
q=23


n,e,d=generate_key(p,q)

private_key=(n,d)
public_key=(n,e)

def en_de_cription(key,mess):
    #the calculation is very slow for large key
    #you can replace this one by Montgomery reduction algorithm for a*b% mod n
    return mess**key[1]%key[0]

mes=235
mes2=en_de_cription(public_key,mes)
mes3=en_de_cription(private_key,mes2)

print(mes,mes2,mes3)


#
#            
#    
#    