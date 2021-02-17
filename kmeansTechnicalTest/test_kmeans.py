import numpy as np
import random
from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import pyplot
from sklearn.cluster import KMeans  # pip install scikit-learn     
import math

# find the max dimensions, so we can know the bounding box, getting the height,
# width, length (because these are the step size)...
def find_mins_maxs(obj):
    minx = obj.x.min()
    maxx = obj.x.max()
    miny = obj.y.min()
    maxy = obj.y.max()
    minz = obj.z.min()
    maxz = obj.z.max()
    return minx, maxx, miny, maxy, minz, maxz

def random_color():
    #colors = []

    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)

    colors = (r,g,b)

    return colors

def angle_between_vectors(pt1,pt2):
    x1 = pt1[0]
    y1 = pt1[1]

    x2 = pt2[0]
    y2 = pt2[1]

    angle = math.atan2(y1, x1) - math.atan2(y2, x2)
    angle = (angle * 360.) / (2*math.pi)
    print(f"original angle: {angle}")
    if (angle < 0):
        angle += 360
    print(f"transformed angle: {angle}")
    print(" ")
    return angle

def compass_to_rgb(h, s=1, v=1):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return (r, g, b)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


#######################################################
#                   MAIN CODE                         #
#######################################################

# Loading the stl mesh file
#your_mesh = mesh.Mesh.from_file('canine.stl')
#your_mesh = mesh.Mesh.from_file('premolar.stl')
#your_mesh = mesh.Mesh.from_file('molar.stl')
your_mesh = mesh.Mesh.from_file('sphere.stl')
#your_mesh = mesh.Mesh.from_file('torus.stl')

# Get the mins and maxs in all dimensions
# 
# What do the min and the max represent for each dimension?
#
(minx, maxx, miny, maxy, minz, maxz) = find_mins_maxs(your_mesh)
print(f"minx: {minx}, maxx : {maxx}")
print(f"miny: {miny}, maxy : {maxy}")
print(f"minz: {minz}, maxz : {maxz}")

# Because the mesh is not centered to (0,0,0), we ensure it does
your_mesh.translate([-(maxx+minx)/2., -(maxy+miny)/2., -(maxz+minz)/2.])

#Get some info about the mesh
_, cog, inertia = your_mesh.get_mass_properties()

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

# One dirty way to split the X, Y, and Z coordinates from the stl mesh
# We also need the normals for our test
#
# Qs: What are the vertices? What are the normals? How many type of normals exist in computer graphics?
#

all_xs = []
all_normals_xs = []
all_ys = []
all_normals_ys = []
all_zs = []
all_normals_zs = []
for indtria in range(len(your_mesh.points)):
    all_xs.append(your_mesh.points[indtria][0])
    all_xs.append(your_mesh.points[indtria][3])
    all_xs.append(your_mesh.points[indtria][6])
    
    all_normals_xs.append(your_mesh.normals[indtria][0])
    
    all_ys.append(your_mesh.points[indtria][1])
    all_ys.append(your_mesh.points[indtria][4])
    all_ys.append(your_mesh.points[indtria][7])
    
    all_normals_ys.append(your_mesh.normals[indtria][1])
    
    
    all_zs.append(your_mesh.points[indtria][2])
    all_zs.append(your_mesh.points[indtria][5])
    all_zs.append(your_mesh.points[indtria][8])
    
    all_normals_zs.append(your_mesh.normals[indtria][2])
    
#Convert the x's, y's, and z's as numpy array
all_xs = np.array(all_xs)
all_ys = np.array(all_ys)
all_zs = np.array(all_zs)

# Because the previous list contains three points per triangle face, 
# there will be many occurrence of the same point, and we only need 
# one version of the each mesh point to be stored in the list:
#
# Q: What does the function numpy.unique provide in general?  In this code, why do I use the unique function? 
# 
unique_all_xs,indices_unique_all_xs = np.unique(all_xs, return_index = True)
all_xs = unique_all_xs
all_ys = all_ys[indices_unique_all_xs]
all_zs = all_zs[indices_unique_all_xs]

# Now, we need to create the data to apply the KMeans on:
# Work on the vertices:
#data = np.array([all_xs, all_ys, all_zs, all_zs])
# Work on the normals:

all_normals_zs_planar = [1.]*len(all_normals_xs)


# Now that we get the normals, we can compare to get the reference vector (1,0)
# to measure the angle between each normal (components X and Y) to (1,0)
# Using the HSV (hue, saturation, and value), we can get a color per normal direction
# We do that for each normal
#
# What does the compass to compass_to_rgb function? (data visualization global knowledge)
#
color_list = []
angle_list = []
for indn in range(len(all_normals_xs)):
    angdeg = angle_between_vectors([all_normals_xs[indn], all_normals_ys[indn]],[1.0,.0])
    angle_list.append(angdeg)
    [currR, currG, currB] = compass_to_rgb(angdeg, s=1, v=1) #abs(all_normals_zs[indn]))
    color_list.append([currR, currG, currB])
    #print(f"angrad: {angrad}, angdeg: {angdeg}")

#Because we need a value between 0 and 1, we can divide each entry by 255. as RGB colors are 
# normally provided with a value 0 to 255 for each color channel
#
# Q: why do we want to have values between 0 and 1 instead of 0 to 255 for the colors?
#
list_of_colors = []
for inpt in range(len(all_normals_xs)):
    current_color = [color_list[inpt][0]/255., color_list[inpt][1]/255., color_list[inpt][2]/255.]
    list_of_colors.append(current_color)
list_of_colors = np.array(list_of_colors)

# Now we can create a matrix containing the normals of each triangle together with the color 
# as separate channel 
data = np.array([all_normals_xs, all_normals_ys, all_normals_zs_planar, list_of_colors[:,0]/255., list_of_colors[:,1]/255., list_of_colors[:,2]/255., angle_list])
data = data.T


# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
# Plot the original mesh
axes.scatter(all_normals_xs, all_normals_ys, all_normals_zs, c=list_of_colors) #edgecolors='k', alpha=1
# Auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
# Show the plot to the screen
pyplot.show()


# Decide the number of clusters:
nbclust = 6
# KMeans algorithm:
kmeans = KMeans(n_clusters=nbclust, random_state=1).fit(data)
# We now extract the centroids of the KMean clusters:
centroids = kmeans.cluster_centers_
            
# We now want to find all the normals that points with a direction 
# very close to the normals found via the KMeans through the centroids
# What we have in hand are:
#    - all the mesh normals
#    - 6 normals (hopefully pointing towards different directions)
#
#  Q: Do you think that all normals pointing to a similar orientation 
#     as the normal from one of the cluster centroids will be very close 
#     to each others?
#       
#   or
#     
#     Do you think that some normals pointing to a similar orientation 
#     as the normal from one of the cluster centroids may be located at 
#     different places?
#
#  Elaborate on your answer
#
#  Q: How do you perceive "similar orientation as the normal from one of 
#     the cluster centroids" in the previous question?
#
#  Q: How would you implement such idea?
#  
# include part 2 here
belonging_classes = {}
dist_list=[]
red_dist_list=[]
red_indx_list=[]
red_color_list = []
for incentr in range(len(centroids)):
    for indtria in range(len(your_mesh.points)):
        current_normal_x = your_mesh.normals[indtria][0]
        current_normal_y = your_mesh.normals[indtria][1]
        current_normal_z = your_mesh.normals[indtria][2]
        
        centroid_norml_x = centroids[incentr][0]
        centroid_norml_y = centroids[incentr][1]
        centroid_norml_z = centroids[incentr][2]
        
        curr_dist = ((current_normal_x+centroid_norml_x)**2+(current_normal_y+centroid_norml_y)**2+(current_normal_z+centroid_norml_z)**2)**.5 
        dist_list.append(curr_dist)
        
        #if curr_dist <= 2:
        red_dist_list.append(current_normal_z)
        red_indx_list.append(indtria)
        red_color_list.append(color_list[indtria])
    
    print(f"min dist: {np.amin(dist_list)}")
    print(f"max dist: {np.amax(dist_list)}")
         
    tmpdict={incentr : {'nb_normals' : len(red_dist_list), 'normals' : red_dist_list, 'tria_indices' : red_indx_list, 'colors' : red_color_list}}
    belonging_classes.update(tmpdict)
    
    # print(f"current centroid indx: {incentr}")
    # print(np.amin(dist_list))
    # print(np.amax(dist_list)) 
    
    dist_list = []
    red_dist_list = []
    red_indx_list = []
    red_color_list = []

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
color_kmeans = ['r', 'g', 'b', 'c', 'y', 'm', 'k', 'w']

for inkey in range(len(belonging_classes)):
    #if inkey > 2:
    #    break
    
    current_list_of_indices = belonging_classes[inkey]['tria_indices']
    for inpt in range(len(current_list_of_indices)):
        current_color = np.array([[belonging_classes[inkey]['colors'][inpt][0]/255., belonging_classes[inkey]['colors'][inpt][1]/255., belonging_classes[inkey]['colors'][inpt][2]/255.]])

        axes.scatter(your_mesh.points[current_list_of_indices[inpt]][0],
                    your_mesh.points[current_list_of_indices[inpt]][1],
                    0., #your_mesh.points[current_list_of_indices[inpt]][2],
                    c=current_color, s=1, label='centroid', zorder=1)
                    #c=color_kmeans[inkey], s=1, label='centroid', zorder=1)

# Plot the original mesh
#axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors, edgecolors=(0.45,0.45,0.45,0.9) ,facecolors=(0.75,0.75,0.75,0.9), zorder=2) ) #, alpha=0.99
    

# Auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()
