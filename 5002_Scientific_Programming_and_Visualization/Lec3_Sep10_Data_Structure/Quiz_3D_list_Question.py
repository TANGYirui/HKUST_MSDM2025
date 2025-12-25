#. Generate a 3D list with random integer
from random import randint,seed
import numpy as np
n=20;m=30;p=40;
seed(20932948)
A =[[[randint(-1,1) for x in range(n)] for y in range(m)] for z in range(p)]