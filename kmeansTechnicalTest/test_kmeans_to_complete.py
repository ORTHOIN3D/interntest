import numpy as np
import random
from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import pyplot
from sklearn.cluster import KMeans  # pip install scikit-learn     
import math


#######################################################
#                   MAIN CODE                         #
#######################################################

# Loading the stl mesh file
#your_mesh = mesh.Mesh.from_file('canine.stl')
#your_mesh = mesh.Mesh.from_file('premolar.stl')
#your_mesh = mesh.Mesh.from_file('molar.stl')
your_mesh = mesh.Mesh.from_file('sphere.stl')
#your_mesh = mesh.Mesh.from_file('torus.stl')


# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
# Plot the original mesh
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors, edgecolors=(0.45,0.45,0.45,0.7) ,facecolors=(0.75,0.75,0.75,0.7))) #edgecolors='k', alpha=1
# Auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
# Show the plot to the screen
pyplot.show()

# 1. Obtain information like the mesh vertices (coordinates), normals, curvature, other types of relevant information

# 2. Make a matrix ready for the KMeans algorithm

# 3. You can try with minimum 2 centroids

# 4. Plot the results on a 3D plot like the one provided above with colors

