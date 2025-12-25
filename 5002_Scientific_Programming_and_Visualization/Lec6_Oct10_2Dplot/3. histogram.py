import matplotlib.pyplot as plt
population_age = [0,10,10,22,55,62,45,21,22,34,
42,42,4,2,102,95,85,55,110,120,70,65,55,111,115,80,75,65,54,44,43,42,48]
bins = [0,10,20,30,40,50,60,70,80,90,100]

plt.figure(figsize=(10,6),dpi=100)
plt.subplot(131)
bins = [0,18,60,100]
plt.hist(population_age, bins, histtype='bar', rwidth=0.5)
plt.xlabel('age groups'); plt.ylabel('Number of people')
plt.title('Histogram(bins)'); plt.show()

plt.subplot(132)
Nbin=5
A=plt.hist(population_age, Nbin, histtype='bar', rwidth=0.5)

plt.xlabel('age groups'); plt.ylabel('Number of people')
plt.title('Histogram(Nbins)'); plt.show()

##check the return of plt.hist()
print(type(A)); print(A); print(A[0]); print(A[1])

plt.subplot(133)
plt.bar((A[1][0:-1]+A[1][1:])/2,A[0],width=15)

plt.xlabel('age groups'); plt.ylabel('Number of people')
plt.title('Bar()'); plt.show()

