import math
import numpy as np

import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import math

def transform_u_to_v(u, epsilon):
    if len(u) < 4:
        raise ValueError("u array must have at least 4 dimensions")
    u_1, u_2, u_3, u_4 = u[:4]
    return u_to_v(u_1, u_2, u_3, u_4, epsilon)

def u_to_v(u_1, u_2, u_3, u_4, epsilon):
    """
    根据给定的u值计算对应的v值。
    """
    delta = math.asin(u_3 / math.sqrt(u_1**2 + u_2**2 + u_3**2))
    beta = math.asin(u_2 / math.sqrt(u_1**2 + u_2**2))
    k = 1 / (math.pi / 2) * (1 - epsilon * u_3)
    
    value_for_asin = epsilon * u_3 + k * math.atan(u_4)
    
    if -1 <= value_for_asin <= 1:
        theta_prime = math.asin(value_for_asin)
        v_1 = math.sin(theta_prime) * 1/math.tan(delta) * math.cos(beta)
        v_2 = math.sin(theta_prime) * 1/math.tan(delta) * math.sin(beta)
        v_3 = math.sin(theta_prime)
        return v_1, v_2, v_3
    else:
        return None, None, None

def higherD_to_v3D(array_higherD, epsilon):
    if array_higherD.shape[0] < 4:
        raise ValueError("Input array must have at least shape 4xN")
    
    transformed = [transform_u_to_v(u, epsilon) for u in array_higherD.T]
    
    while len(transformed[0]) < 3:
        transformed = [transform_u_to_v(u, epsilon) for u in transformed]
        
    return np.array(transformed).T


def generate_cube_edges():
    """
    生成正方体12条边上的所有点。
    """
    start, end, num_points = 0, 1, 10
    edges = []

    # 定义正方体每个边的两个端点
    cube_edges = [
        [[start, start, start], [end, start, start]],
        [[start, start, start], [start, end, start]],
        [[start, start, start], [start, start, end]],
        [[end, start, start], [end, end, start]],
        [[end, start, start], [end, start, end]],
        [[start, end, start], [end, end, start]],
        [[start, end, start], [start, end, end]],
        [[start, start, end], [end, start, end]],
        [[start, start, end], [start, end, end]],
        [[end, end, start], [end, end, end]],
        [[end, start, end], [end, end, end]],
        [[start, end, end], [end, end, end]]
    ]

    # 对于每条边，使用linspace生成10个点
    for edge in cube_edges:
        start_point, end_point = edge
        x_values = np.linspace(start_point[0], end_point[0], num_points)
        y_values = np.linspace(start_point[1], end_point[1], num_points)
        z_values = np.linspace(start_point[2], end_point[2], num_points)
        
        for i in range(num_points):
            edges.append([x_values[i], y_values[i], z_values[i]])

    return edges

def visualize_3D_data(data, title, fig, subplot_index):
    ax = fig.add_subplot(2, 3, subplot_index, projection='3d')
    ax.scatter(data[0], data[1], data[2], c='r', marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_title(title)

def main():
    epsilon = 0.8

    cube_data = generate_cube_edges()
    fig = plt.figure(figsize=(20, 15))

    dimensions_to_extract = [4, 5, 6, 7]
    epsilon_values = [0.1 for _ in dimensions_to_extract]

    # for index, (dim, eps) in enumerate(zip(dimensions_to_extract, epsilon_values)):
    #     cube_data_extended = np.tile(cube_data, (dim//3, 1)).T  # replicate data to match required dimensions
    #     u_data = np.array(cube_data_extended)
    #     transformed_data = transform_u_to_v(u_data, eps)
        
    #     # Print first 10 transformed data
    #     headers = ["v_n", "v_n+1", "v_n+2"]
    #     list_format = [tuple(row) for row in transformed_data.T[:10]]
    #     print(f"\nFirst 10 transformed cube data from {dim}D to 3D:")
    #     print(tabulate(list_format, headers=headers, floatfmt=".4f"))
        
    #     visualize_3D_data(transformed_data[:3], f"Cube Data Transformed from {dim}D", fig, index+1)


    for index, (dim, eps) in enumerate(zip(dimensions_to_extract, epsilon_values)):
        # cube_data_extended = np.tile(cube_data, (dim//3, 1)).T  # replicate data to match required dimensions
        cube_data_extended = np.repeat(cube_data, dim//3, axis=0)  # replicate data to match required dimensions
        # u_data = np.array(cube_data_extended)   
        u_data = np.array(cube_data_extended)
        
        # 使用higherD_to_v3D函数而不是transform_u_to_v
        # transformed_data = higherD_to_v3D(u_data, eps)
        transformed_data = higherD_to_v3D(u_data, eps)

        
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

