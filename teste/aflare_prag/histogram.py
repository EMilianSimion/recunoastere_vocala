import numpy as np
import matplotlib.pyplot as plt

corect = []
gresit = []
with open('ccomb.txt', 'r') as f:
    for line in f:
        corect.append(float(line.split(',')[0].split(' ')[-1]))

with open('gcomb.txt', 'r') as f:
    for line in f:
        gresit.append(float(line.split(',')[0].split(' ')[-1]))
# corect = np.sort(corect)
# gresit = np.sort(gresit)
#
# print(np.average(corect))
#
# # plt.scatter(x, y)
# xplot = [i*(len(corect)/len(gresit)) for i in range(len(gresit))]
#
# print((xplot))
# print(len(gresit))
# yplot = range(len(corect))
#
# plt.scatter(xplot, gresit, color='red')
# plt.scatter(yplot, corect, color='blue')
# plt.grid()
# plt.xlabel('x values')
# plt.ylabel('y values')
# plt.show()
#
# # print(corect[1750])

print(len(corect))
print(len(gresit))
correct_200 = [a for a in corect if a < -210]
print(len(correct_200))
gresit_200 = [a for a in gresit if a < -210]
print(len(gresit_200))

#
# # histogram plot
# from numpy.random import seed
# from numpy.random import randn
# from matplotlib import pyplot
#
# # seed the random number generator
# seed(1)
# # generate univariate observations
# data1 = corect
# data2 = gresit
# # histogram plot
# pyplot.hist(data1)
# pyplot.hist(data2, color='red')
# pyplot.show()
