import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

# Load point clouds
pcd1 = o3d.io.read_point_cloud("scan.ply")
mesh = o3d.io.read_triangle_mesh ("part.stl")

# Visualize the downsampled point cloud
o3d.visualization.draw_geometries([pcd1, mesh])

# Convert the mesh to a point cloud
point_cloud = mesh.sample_points_uniformly(number_of_points=10000)

# Downsample the point cloud using voxel sampling
downsampled = point_cloud.voxel_down_sample(voxel_size=0.1)

# Visualize the downsampled point cloud
o3d.visualization.draw_geometries([downsampled])

# Compute distances
dists = np.asarray(downsampled.compute_point_cloud_distance(pcd1))

# Draw heatmap of distances
norm = plt.Normalize(dists.min(), dists.max())
cmap = plt.colormaps.get_cmap('jet')
colors = cmap(norm(dists))
downsampled.colors = o3d.utility.Vector3dVector(colors[:, :3])

# generate random colors for each point
n_points = len(downsampled.points)
colors = cmap(norm(dists))[:, :3]

# set colors for each point
downsampled.colors = o3d.utility.Vector3dVector(colors)

# visualize point cloud
o3d.visualization.draw_geometries([pcd1, downsampled])

# Create a boolean mask for points with distance less than 4 mm
mask = dists < 10

# Initialize color array to all red
colors = np.zeros((len(downsampled.points), 3))
colors[:, 0] = 1.0

# Set color to green for points with distance less than 4 mm
colors[mask, 0] = 0.0
colors[mask, 1] = 1.0

# set colors for each point
downsampled.colors = o3d.utility.Vector3dVector(colors)

# visualize point cloud
o3d.visualization.draw_geometries([pcd1, downsampled])
