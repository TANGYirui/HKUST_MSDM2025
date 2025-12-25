import matplotlib.pylab as plt
import numpy as np
import numpy
from scipy.linalg import svd

x = np.linspace(-np.pi, np.pi, 400)
mu, sigma = 0, 0.1
noise = np.random.normal(mu, sigma, 400)
#noise = np.random.rand(400)
signal=np.sin(x)

signal_with_noise=signal+noise

signal_mat = signal_with_noise.reshape(20, 20)


plt.subplot(121)
plt.plot(x, signal)
plt.title("sin")

plt.subplot(122)
plt.plot(x, signal_with_noise,label='original')
plt.title("sin with noise")


U,s,Vh = svd(signal_mat)
print(s)

num=5
for nn in range(num):
    K=nn+1
    A = U[:,0:K]@ numpy.diag(s[0:K]) @ Vh[0:K,:]
    signal_K = A.reshape((400,))

    plt.plot(x, signal_K-K*1,label='K='+str(K))  

plt.legend()

plt.show()