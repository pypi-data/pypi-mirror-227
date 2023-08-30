from tabulate import tabulate
import math
import matplotlib.pyplot as plt
import numpy as np


def transform_u_to_v(u, epsilon):
    if len(u) < 4:
        raise ValueError("u array must have at least 4 dimensions")
    u_1, u_2, u_3, u_4 = u[:4]
    result = u_to_v(u_1, u_2, u_3, u_4, epsilon)
    if None in result:
        return None
    return result


def u_to_v(u_1, u_2, u_3, u_4, epsilon):
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
        return None


def generate_cube_edges_points(start, end, num_points):
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

    for edge in cube_edges:
        start_point, end_point = edge
        x_values = np.linspace(start_point[0], end_point[0], num_points)
        y_values = np.linspace(start_point[1], end_point[1], num_points)
        z_values = np.linspace(start_point[2], end_point[2], num_points)

        for i in range(num_points):
            edges.append([x_values[i], y_values[i], z_values[i]])

    return edges


def transform_highD_to_v3D(array, epsilon):
    if not 4 <= array.shape[0] <= 9:
        raise ValueError("Input array must have shape between 4xN to 9xN")

    result = [transform_u_to_v(u, epsilon) for u in array[:, :4].T]

    for i in range(4, array.shape[0]):
        result = [transform_u_to_v(np.concatenate([v, [array[i, j]]]), epsilon) for j, v in enumerate(result)]

    return np.array(result).T


def logistic_map(a, u_initial, N):
    u_values = [u_initial]
    for n in range(1, N):
        u_next = a * u_values[-1] * (1 - u_values[-1])
        u_values.append(u_next)
    return u_values


def extract_sequences(sequence, dim):
    return [tuple(sequence[i:i+dim]) for i in range(len(sequence) - dim + 1)]


def visualize_3D(ax, data, title, color='blue'):
    """Visualize 3D data."""
    data_array = np.array(data)
    data_filtered = [d for d in data_array if d is not None and len(d) == 3]
    if not data_filtered:
        print(f"No valid data to visualize for: {title}")
        return
    x_vals, y_vals, z_vals = zip(*data_filtered)
    ax.scatter(x_vals, y_vals, z_vals, color=color, s=1)
    ax.set_title(title)




def main():
    a = 4
    u_initial = 0.1
    N = 1000
    epsilon = 0.8

    sequence = logistic_map(a, u_initial, N)

    fig = plt.figure(figsize=(20, 15))

    # Process 3D data
    ax1 = fig.add_subplot(3, 5, 1, projection='3d')
    visualize_3D(ax1, extract_sequences(sequence, 3), "3D Data Points")

    # Process 4D to 7D data
    titles = ["Compressed 3D Data Points from 4D", "transformed_5D", "transformed_6D", "transformed_7D"]
    colors = ['red', 'blue', 'red', 'red']
    positions = [2, 4, 6, 7]

    for i, (title, color, position) in enumerate(zip(titles, colors, positions)):
        ax = fig.add_subplot(3, 5, position, projection='3d')
        data = extract_sequences(sequence, i + 4)
        visualize_3D(ax, transform_highD_to_v3D(np.array(data).T, epsilon), title, color)

    # Direct Method for 4D data
    ax2 = fig.add_subplot(2, 5, 3, projection='3d')
    four_dim_data = extract_sequences(sequence, 4)
    compressed_4D = [u_to_v(p[0], p[1], p[2], p[3], epsilon)[:3] for p in four_dim_data]
    visualize_3D(ax2, compressed_4D, "Compressed 3D Data Points (Direct Method)", 'red')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()

