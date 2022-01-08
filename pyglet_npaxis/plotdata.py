from matplotlib import pyplot as plt
x=range(10)
y = [i*i for i in x]

x = 1,1.3,2,3,4,5,7,10
y = 246,181,118,73,56,44,33,22
plt.axis( [0,10,0,250] )
plt.plot(x,y)
plt.show()