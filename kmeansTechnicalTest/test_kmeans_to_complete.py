##################################
# Description and library import #
##################################

# The aim of this test is to check whether you understand 
# the mesh processing aspects involved in R&D for our company
# In this task, the aim is to prepare data for incoming deep 
# learning purposes. One way to do that is to extract features 
# from the mesh of interest, e.g. incisives, canines, premolars, 
# and molars obtained from the original mesh. Typical features 
# are the normals, the mean and gaussian curvatures, or the discretized 
# Laplacian, to name a few. 
# 
# As we are also at the position where we don't have enough data
# for deep learning, we are also investigating the generation of 
# fake data based on real data. As in image processing, we can 
# generate fake data simply by adding random noise to each vertex 
# of the mesh and/or simply deform in an intelligent manner the shape 
# of mesh with some constraints. Rotation of the tooth is also a good 
# feature to look at. Getting data clusters from the KMeans algorithms 
# can for instance be used to only select a certain part of the tooth 
# and apply some noise or deform it locally.
# 
# Therefore, the aim of this exercise is to obtain the centroids found 
# by the KMeans algorithm using for instance the coordinates, the normals 
# and eventually the curvatures (convex and concave aspects of the mesh)

# In this exercise, we provide a way to load the data, and beyond that, you 
# have the choice to either get the matrix data that will be used in the 
# KMeans algorithm and the choice on using a pre-existing algorihm for the KMeans 
# (scikit-learn has a version available) or implement your own version 
# and to finally display the cluster on the original data similar to the original 
# data provided in the code below. 

# While most libraries should be installed by default, it might 
# be that you need to install sklearn via 
#
# pip install -U scikit-learn
#
# The documentation for using the KMeans algorithm from scikit-learn is available at:
#
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
#
# Also, for loading the stl-mesh(es) available in the same directory, we use 
# the library called numpy-stl accessible via:
#
# pip install numpy-stl
# 
# For this second library, you can load the data as provided using the following command:
#
# mesh.Mesh.from_file('sphere.stl')
#
# The documentation for using this mlibrary is available at:
#
# https://pypi.org/project/numpy-stl/



# Typical libraries:
import numpy as np
import random
import math

# For plotting:
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import pyplot

# stl related library
from stl import mesh
# KMeans related library
from sklearn.cluster import KMeans  



#######################################################
#                   MAIN CODE                         #
#######################################################

# Loading the stl mesh file
#your_mesh = mesh.Mesh.from_file('canine.stl')
your_mesh = mesh.Mesh.from_file('premolar.stl')
#your_mesh = mesh.Mesh.from_file('molar.stl')
#your_mesh = mesh.Mesh.from_file('sphere.stl')
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

# # Hint on creating noise on the mesh surface
# amount_of_noise = 3./100.
# noise = np.random.randn(numberOfPointsOnMesh, 3) * amount_of_noise

# 1. Obtain information like the mesh vertices (coordinates), normals, curvature, other types of relevant information

# 2. Make a matrix ready for the KMeans algorithm

# 3. You can try with minimum 2 centroids

# 4. Plot the results on a 3D plot like the one provided above with colors

