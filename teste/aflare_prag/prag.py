import numpy as np
import matplotlib.pyplot as plt

corect = []
gresit = []
with open('cmfcc.txt', 'r') as f:
    for line in f:
        corect.append(float(line.split(',')[0].split(' ')[-1]))

with open('gmfcc.txt', 'r') as f:
    for line in f:
        gresit.append(float(line.split(',')[0].split(' ')[-1]))
# corect = np.sort(corect)
# gresit = np.sort(gresit)

print(np.average(corect))

# plt.scatter(x, y)
xplot = [i*(len(corect)/len(gresit)) for i in range(len(gresit))]

print((xplot))
print(len(gresit))
yplot = range(len(corect))

plt.scatter(xplot, gresit, color='red')
plt.scatter(yplot, corect, color='blue')
plt.grid()
plt.xlabel('x values')
plt.ylabel('y values')
plt.show()

# print(corect[1750])
