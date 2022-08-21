import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.neighbors import NearestNeighbors 

np.random.seed(19)

data = np.random.random_sample((10,3))
point = [0.5,0.5,0.5]
print(data)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.set_xlabel('x', labelpad=10)
# ax.set_ylabel('y', labelpad=10)
# ax.set_zlabel('z', labelpad=10)

# ax.scatter([i[0] for i in data], [i[1] for i in data], [i[2] for i in data], cmap='jet',label="z")
# ax.scatter(point[0],point[1],point[2])

knn_model = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(data) 
distance, nearestID = knn_model.kneighbors([point])
print(nearestID[0])
