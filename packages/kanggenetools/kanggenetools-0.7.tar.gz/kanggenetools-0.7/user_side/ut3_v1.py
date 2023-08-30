import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate


def generate_cube_edges(num_points_per_edge=20):
    # Define cube vertices
    vertices = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
                (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    
    # Define edges using vertex indices
    edges = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), 
             (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]
    
    # Get actual edge coordinates with interpolated points
    edge_coords = []
    for edge in edges:
        start, end = edge
        start_vertex = np.array(vertices[start])
        end_vertex = np.array(vertices[end])
        for t in np.linspace(0, 1, num_points_per_edge):
            point = (1 - t) * start_vertex + t * end_vertex
            edge_coords.append(point.tolist())
    
    return edge_coords



def transform_u_to_v(u_data, epsilon):
    dim = u_data.shape[0]
    M = np.zeros((dim, dim))
    for i in range(dim):
        M[i, i] = 1
        if i + 1 < dim:
            M[i, i + 1] = -epsilon
    return M @ u_data

def visualize_3D_data(data, title, fig, position, color='b', marker_size=1):
    ax = fig.add_subplot(2, 5, position, projection='3d')
    x_vals, y_vals, z_vals = data
    ax.scatter(x_vals, y_vals, z_vals, color=color, s=marker_size, marker='o')
    ax.set_title(title)

def main():
    epsilon = 0.8

    cube_data = generate_cube_edges()
    fig = plt.figure(figsize=(20, 15))

    dimensions_to_extract = [4, 5, 6, 7]
    epsilon_values = [0.1 for _ in dimensions_to_extract]

    for index, (dim, eps) in enumerate(zip(dimensions_to_extract, epsilon_values)):
        cube_data_extended = np.tile(cube_data, (dim//3, 1)).T  # replicate data to match required dimensions
        u_data = np.array(cube_data_extended)
        transformed_data = transform_u_to_v(u_data, eps)
        
        # Print first 10 transformed data
        headers = ["v_n", "v_n+1", "v_n+2"]
        list_format = [tuple(row) for row in transformed_data.T[:10]]
        print(f"\nFirst 10 transformed cube data from {dim}D to 3D:")
        print(tabulate(list_format, headers=headers, floatfmt=".4f"))
        
        visualize_3D_data(transformed_data[:3], f"Cube Data Transformed from {dim}D", fig, index+1)

    # Original cube data visualization
    visualize_3D_data(np.array(cube_data).T, "Original Cube Data", fig, len(dimensions_to_extract) + 1)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
