from scipy.spatial import Delaunay
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv(r'C:\Users\Student240914\Desktop\inzynierka\__Napisane\Programy i dane\Magiczne Bloczki\Dane_wyjatki.csv',sep=";")

print(data)
points = np.array(data[data.columns[1:3]])
print(points)
tri = Delaunay(points,incremental=False)
plt.triplot(points[:,0], points[:,1], tri.simplices)
#plt.plot(points[:,0], points[:,1])
plt.show()