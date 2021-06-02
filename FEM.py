import numpy as np 
import matplotlib.pyplot as plt 

L = 0.02
number = 4
points = int(number**0.5)
x = np.linspace(0, L, points)
y = np.linspace(0, L, points)
mesh = np.meshgrid(x, y)
print(mesh)