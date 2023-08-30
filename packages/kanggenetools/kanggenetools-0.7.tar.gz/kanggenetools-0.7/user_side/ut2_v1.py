import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

import math
import matplotlib.pyplot as plt
import numpy as np

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

def generate_cube_edges_points(start, end, num_points):
    """
    生成正方体12条边上的所有点。
    """
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

def u4D_to_v3D(array_4D, epsilon):
    if array_4D.shape[0] != 4:
        raise ValueError("Input array must have shape 4xN")
    return np.array([transform_u_to_v(u, epsilon) for u in array_4D.T]).T

def u5D_to_v3D(array_5D, epsilon):
    if array_5D.shape[0] != 5:
        raise ValueError("Input array must have shape 5xN")
    transformed = u4D_to_v3D(array_5D[:4], epsilon)
    return np.array([transform_u_to_v(np.concatenate([v, [array_5D[4][i]]]), epsilon) for i, v in enumerate(transformed.T)]).T

def u6D_to_v3D(array_6D, epsilon):
    if array_6D.shape[0] != 6:
        raise ValueError("Input array must have shape 6xN")
    transformed = u5D_to_v3D(array_6D[:5], epsilon)
    return np.array([transform_u_to_v(np.concatenate([v, [array_6D[5][i]]]), epsilon) for i, v in enumerate(transformed.T)]).T

def u7D_to_v3D(array_7D, epsilon):
    if array_7D.shape[0] != 7:
        raise ValueError("Input array must have shape 7xN")
    transformed = u6D_to_v3D(array_7D[:6], epsilon)
    return np.array([transform_u_to_v(np.concatenate([v, [array_7D[6][i]]]), epsilon) for i, v in enumerate(transformed.T)]).T

def u8D_to_v3D(array_8D, epsilon):
    if array_8D.shape[0] != 8:
        raise ValueError("Input array must have shape 8xN")
    transformed = u7D_to_v3D(array_8D[:7], epsilon)
    return np.array([transform_u_to_v(np.concatenate([v, [array_8D[7][i]]]), epsilon) for i, v in enumerate(transformed.T)]).T

def u9D_to_v3D(array_9D, epsilon):
    if array_9D.shape[0] != 9:
        raise ValueError("Input array must have shape 9xN")
    transformed = u8D_to_v3D(array_9D[:8], epsilon)
    return np.array([transform_u_to_v(np.concatenate([v, [array_9D[8][i]]]), epsilon) for i, v in enumerate(transformed.T)]).T

def logistic_map(a, u_initial, N):
    u_values = [u_initial]
    for n in range(1, N):
        u_next = a * u_values[-1] * (1 - u_values[-1])
        u_values.append(u_next)
    return u_values

def extract_sequences(sequence, dim):
    return [tuple(sequence[i:i+dim]) for i in range(len(sequence) - dim + 1)]

def visualize_3D_data(ax, data, title, color='blue', marker='o'):
    x_vals, y_vals, z_vals = zip(*data) if isinstance(data[0], tuple) else data
    ax.scatter(x_vals, y_vals, z_vals, color=color, s=1, marker=marker)
    ax.set_title(title)

def transform_and_visualize(data, epsilon, fig, position, title, color='blue'):
    dim = len(data[0])
    transformed_func_map = {
        4: u4D_to_v3D,
        5: u5D_to_v3D,
        6: u6D_to_v3D,
        7: u7D_to_v3D,
        8: u8D_to_v3D,
        9: u9D_to_v3D
    }
    if dim in transformed_func_map:
        transformed_data = transformed_func_map[dim](np.array(data).T, epsilon)
        ax = fig.add_subplot(2, 5, position, projection='3d')
        visualize_3D_data(ax, transformed_data.T, title, color)
        return transformed_data
    return []

def main():
    a = 4
    u_initial = 0.1
    N = 1000
    epsilon = 0.8

    sequence = logistic_map(a, u_initial, N)

    fig = plt.figure(figsize=(20, 15))

    # Process 3D data
    three_dim_data = extract_sequences(sequence, 3)
    ax1 = fig.add_subplot(3, 5, 1, projection='3d')
    visualize_3D_data(ax1, three_dim_data, "3D Data Points")

    # Process 4D to 7D data
    titles = ["Compressed 3D Data Points from 4D", "transformed_5D", "transformed_6D", "transformed_7D"]
    colors = ['red', 'blue', 'red', 'red']
    positions = [2, 4, 6, 7]
    for i in range(4, 8):
        data = extract_sequences(sequence, i)
        transform_and_visualize(data, epsilon, fig, positions[i-4], titles[i-4], colors[i-4])
    
    # Using Direct Method to compress 4D data
    four_dim_data = extract_sequences(sequence, 4)
    compressed_4D = [u_to_v(p[0], p[1], p[2], p[3], epsilon)[:3] for p in four_dim_data]
    ax2 = fig.add_subplot(2, 5, 3, projection='3d')
    visualize_3D_data(ax2, compressed_4D, "Compressed 3D Data Points (Direct Method)", 'red')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
