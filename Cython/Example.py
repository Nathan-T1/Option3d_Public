import numpy as np
from Option3d import  *
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors
from matplotlib import cm

def plot(df):

	X,Y = np.meshgrid(df.columns.astype(float), df.index)
	Z = df.values

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	surf = ax.plot_surface(X, Y, Z,cmap=cm.coolwarm,label = "Graph", antialiased=True)
	
	plt.show()

'''
Each row in array represents a seperate leg
Each row must have 9 elements each

Element 1: Long or short (1 for long, -1 for short)
Element 2: Call or put (0 for call, 1 for put)
Element 3: Spot price (Enter the same value for all)
Element 4: Stirke 
Element 5: DTE (Enter integer)
Element 6: IV (Enter as decimal, 20% ~ .20)
Element 7: Spot Width (.20 means calculate for spot value +-20% from the current underlying price)
Element 8: Spot Step (.005 means within the range, calculate at .5% intervals)
Element 9: Time Step (1 would mean calculate once a day, .25 means calculate every 1/4 of a day ~ 4 times a day)

Below would represent a Iron Condor
'''

array = np.array(
[[-1, 0, 100, 100, 20, .20, .20, .0025, .25],
[1, 0, 100, 101, 20, .20, .20, .0025, .25],
[-1, 1, 100, 100, 20, .20, .20, .0025, .25],
[1, 1, 100, 99, 20, .20, .20, .0025, .25]], 
np.float64
	)

'''
Function is called main_array
Takes two parameters

1: A two demensional array. If you only want to use one leg make sure you 
use a 2d array ~ [[a,b,c]]

2: Z. Represents what you want to calculate and display on the z axis of the surface plot.
Must be a string like: Delta, Gamma, Theta, Vega, P/L, Exercise Probability
'''

start = time.time()
df = main_array(array, "Theta")
end = time.time()

print(df)
print(end-start)

plot(df)


