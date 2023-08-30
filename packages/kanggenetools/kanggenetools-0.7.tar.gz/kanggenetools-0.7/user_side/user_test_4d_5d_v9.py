import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from mpl_toolkits.mplot3d import Axes3D

import kanggenetools
kanggenetools.authorize("kangtools")
from kanggenetools.transform import u_to_v

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


def print_backend_values(u_1, u_2, u_3, u_4, epsilon):
    """
    打印相关参数。
    """
    print(f"Value for u1 is {u_1} ")
    print(f"Value for u2 is {u_2} ")
    print(f"Value for u3 is {u_3} ")
    print(f"Value for u4 is {u_4} ")
    print(f"Value for epsilon is {epsilon} ")
    k = 1 / (math.pi / 2) * (1 - epsilon * u_3)
    print(f"Value for k = {k} ")



def visualize_transformed_values(cube_points, transformed_values_0, transformed_values_1, transformed_values_5D):
    """
    可视化原始的u值和转换后的v值。
    """
    # fig = plt.figure(figsize=(20, 5))

    # Original cube edge points
    ax1 = fig.add_subplot(141, projection='3d')
    ax1.scatter(*zip(*cube_points), c='b', marker='x', label="Original u values on cube edges")
    ax1.set_title('Original u values on cube edges')
    ax1.legend()

    # Transformed points with u_4=0
    ax2 = fig.add_subplot(142, projection='3d')
    ax2.scatter(*zip(*transformed_values_0), c='g', marker='o', label="Transformed v values (u_4=0)")
    ax2.scatter(*zip(*cube_points), c='b', marker='x', alpha=0.3, label="Original u values on cube edges")
    ax2.set_title('Transformed v values (u_4=0)')
    ax2.legend()

    # Transformed points with u_4=0.1
    ax3 = fig.add_subplot(143, projection='3d')
    ax3.scatter(*zip(*transformed_values_1), c='r', marker='o', label="Transformed v values (u_4=1)")
    ax3.scatter(*zip(*cube_points), c='b', marker='x', alpha=0.3, label="Original u values on cube edges")
    ax3.set_title('Transformed v values (u_4=1)')
    ax3.legend()

    # 5D transformed values
    ax4 = fig.add_subplot(144, projection='3d')
    ax4.scatter(*zip(*transformed_values_0), color=(0.7,0,0), s=0.2, marker='o', label="Transformed v values (u_4=0)")
    ax4.scatter(*zip(*transformed_values_1), color=(0.1,0.7,0.4), s=0.2, marker='o', label="Transformed v values (u_4=1)")
    ax4.scatter(*zip(*cube_points), c='b', s=1, marker='x', alpha=0.3, label="Original u values on cube edges")
    ax4.scatter(*zip(*transformed_values_5D), c='#FF9999', s=1, marker='o', label="5D Transformed v values")
    ax4.set_title('5D Transformed v values')
    ax4.legend()

    # Layout adjustment
    # plt.tight_layout()
    # plt.show()


def visualize_transformed_values_extended(cube_points, transformed_values_5D, transformed_values_6D, transformed_values_7D, transformed_values_8D, transformed_values_9D, transformed_values_10D):
    """
    可视化从3D到10D的转换效果。
    """
    fig = plt.figure(figsize=(25, 15))
    
    # 数据集
    datasets = [cube_points, transformed_values_5D, transformed_values_6D, transformed_values_7D, transformed_values_8D, transformed_values_9D, transformed_values_10D]
    titles = ['3D', '5D', '6D', '7D', '8D', '9D', '10D']
    
    # 创建前9个子图
    for i in range(6):
        ax = fig.add_subplot(2, 5, i+1, projection='3d')
        ax.scatter(*zip(*datasets[i]),s=1, marker='o', label=titles[i])
        ax.scatter(*zip(*cube_points), c='b',s=1, marker='x', alpha=0.3)
        ax.set_title(titles[i])
        ax.legend()
    
    # 创建第10个子图
    ax_last = fig.add_subplot(2, 5, 10, projection='3d')
    colors = ['#FF9999', '#FF66B2', '#FF33CC', '#FF00E6', '#CC00FF', '#9900FF', '#6600FF']
    
    for i in range(1, 6):
        ax_last.scatter(*zip(*datasets[i]), c=colors[i-1],s=1, marker='.', label=titles[i], alpha=0.7)
    
    ax_last.scatter(*zip(*cube_points), c='b',s=1,  marker='x', alpha=0.3, label='3D')
    ax_last.set_title('3D-10D Overlay')
    ax_last.legend()

    # Layout adjustment
    # plt.tight_layout()
    # plt.show()


def logistic_map(a, u_initial, N):
    u_values = [u_initial]
    for n in range(1, N):
        u_next = a * u_values[-1] * (1 - u_values[-1])
        u_values.append(u_next)
    return u_values

def extract_sequences(sequence, dim):
    return [tuple(sequence[i:i+dim]) for i in range(len(sequence) - dim + 1)]



def show_ref():
    start, end, num_points, epsilon = 0.1, 1, 100, 0.8

    # Generate cube edge points
    cube_points = generate_cube_edges_points(start, end, num_points)
    cube_points_array = np.array(cube_points).T

    print(cube_points_array.shape)

    sizeset=1200

    transformed_4D = u4D_to_v3D(np.vstack([cube_points_array, np.ones(sizeset)*0.1]), epsilon)
    # transformed_4D = u4D_to_v3D(cube_points_array, epsilon)
    print('hello')
    transformed_5D = u5D_to_v3D(np.vstack([cube_points_array, np.ones((2, sizeset))*0.1]), epsilon)
    transformed_6D = u6D_to_v3D(np.vstack([cube_points_array, np.ones((3, sizeset))*0.1]), epsilon)
    transformed_7D = u7D_to_v3D(np.vstack([cube_points_array, np.ones((4, sizeset))*0.1]), epsilon)
    transformed_8D = u8D_to_v3D(np.vstack([cube_points_array, np.ones((5, sizeset))*0.1]), epsilon)
    transformed_9D = u9D_to_v3D(np.vstack([cube_points_array, np.ones((6, sizeset))*0.1]), epsilon)
    
    visualize_transformed_values_extended(cube_points, transformed_5D.T, transformed_6D.T, transformed_7D.T, transformed_8D.T, transformed_9D.T, [])


def main():
    a = 4.0
    u_initial = 0.1
    N = 1000
    
    sequence = logistic_map(a, u_initial, N)

    # Extracting 3D data points
    three_dim_data = extract_sequences(sequence, 3)
    print(f"Total 3D data points: {len(three_dim_data)}")  # This should be N-2

    # Visualize 3D data points
    fig = plt.figure(figsize=(20, 15))
    ax1 = fig.add_subplot(3, 5, 1, projection='3d')
    xs, ys, zs = zip(*three_dim_data)
    ax1.scatter(xs, ys, zs, s=1)
    ax1.set_title("3D Data Points")
    


    # Extracting 4D data points
    four_dim_data = extract_sequences(sequence, 4)
    print(f"Total 4D data points: {len(four_dim_data)}")  # This should be N-3
    
    # Print first 10 4D data points
    headers = ["u_n", "u_n+1", "u_n+2", "u_n+3"]
    print("\nFirst 10 4D data points:")
    print(tabulate(four_dim_data[:10], headers=headers, floatfmt=".4f"))
    

    # 方法1： 直接法：Compress 4D data to 3D
    compressed_method1_4D_to_v3D = [u_to_v(p[0], p[1], p[2], p[3], 0.8)[:3] for p in four_dim_data]
    print('compressed_3D:')
    print(np.array(compressed_method1_4D_to_v3D).shape)

    # Print first 10 compressed_3D data points
    headers = ["v_n", "v_n+1", "v_n+2"]
    print("\n first 10 compressed_method1_4D_to_v3D data points:")
    print(tabulate(compressed_method1_4D_to_v3D[:10], headers=headers, floatfmt=".4f"))
    
    # 方法2： 套用既有函数法Transform4D_to_v3D：Compress 4D data to 3D-V空间显示 -方法2可行。well done
    epsilon = 0.8

    print('np.array(four_dim_data).T.shape:')
    print(np.array(four_dim_data).T.shape)

    transformed_4D = u4D_to_v3D(np.array(four_dim_data).T, epsilon)

    print('transformed_4D.shape:')
    print(transformed_4D.shape)

    # Print first 10 transformed_4D 
    headers = ["v_n", "v_n+1", "v_n+2"]
    print("\n first 10 transformed_4D:--------------------")
    list_format = [tuple(row) for row in transformed_4D.T[:10]]
    print(tabulate(list_format, headers=headers, floatfmt=".4f"))

    ax = fig.add_subplot(3, 5, 3, projection='3d')
    x_vals, y_vals, z_vals = transformed_4D
    ax.scatter(x_vals, y_vals, z_vals, color='r',s=3, marker='o', label='transformed_4D')

    # ax.scatter(*zip(*transformed_4D),color='r', marker='o', label='transformed_4D')

    # prepare 
    # Extracting 5D data points
    five_dim_data = extract_sequences(sequence, 5)
    print(f"preparefor 5D----Total 5D data points: {len(five_dim_data)}")  # This should be N-3
    
    # Print first 10 5D data points
    headers = ["u_n", "u_n+1", "u_n+2", "u_n+3", "u_n+4"]
    print("\nFirst 10 5D data points:")
    print(tabulate(five_dim_data[:10], headers=headers, floatfmt=".4f"))

    transformed_5D = u5D_to_v3D(np.array(five_dim_data).T, epsilon)

    print('transformed_5D.shape:')
    print(transformed_5D.shape)

    # Print first 10 transformed_5D 
    headers = ["v_n", "v_n+1", "v_n+2"]
    print("\n first 10 transformed_5D:--------------------")
    list_format = [tuple(row) for row in transformed_5D.T[:10]]
    print(tabulate(list_format, headers=headers, floatfmt=".4f"))

    ax = fig.add_subplot(3, 5, 4, projection='3d')
    x_vals, y_vals, z_vals = transformed_5D
    ax.scatter(x_vals, y_vals, z_vals, color='b',s=2, marker='o', label='transformed_5D')

    #-----------------------------------------------------------------------------------------
    # prepare 
    # Extracting 6D data points
    six_dim_data = extract_sequences(sequence, 6)
    print(f"preparefor 6D----Total 6D data points: {len(six_dim_data)}")  # This should be N-3
    
    # Print first 10 6D data points
    headers = ["u_n", "u_n+1", "u_n+2", "u_n+3", "u_n+4","u_n+5"]
    print("\nFirst 10 6D data points:")
    print(tabulate(six_dim_data[:10], headers=headers, floatfmt=".4f"))

    transformed_6D = u6D_to_v3D(np.array(six_dim_data).T, epsilon)

    print('transformed_6D.shape:')
    print(transformed_6D.shape)

    # Print first 10 transformed_6D 
    headers = ["v_n", "v_n+1", "v_n+2"]
    print("\n first 10 transformed_6D:--------------------")
    list_format = [tuple(row) for row in transformed_6D.T[:10]]
    print(tabulate(list_format, headers=headers, floatfmt=".4f"))

    fig6D = plt.figure(figsize=(20, 15))
    ax = fig6D.add_subplot(1, 1, 1, projection='3d')
    x_vals, y_vals, z_vals = transformed_6D
    ax.scatter(x_vals, y_vals, z_vals, color='r',s=1, marker='o', label='transformed_6D')

    #-----------------------------------------------------------------------------------------
    # prepare 
    # prepare 
    # Extracting 7D data points
    seven_dim_data = extract_sequences(sequence, 7)
    print(f"preparefor 7D----Total 7D data points: {len(seven_dim_data)}")  # This should be N-3
    
    # Print first 10 6D data points
    headers = ["u_n", "u_n+1", "u_n+2", "u_n+3", "u_n+4","u_n+5","u_n+6"]
    print("\nFirst 10 7D data points:")
    print(tabulate(seven_dim_data[:10], headers=headers, floatfmt=".4f"))


    transformed_7D = u7D_to_v3D(np.array(seven_dim_data).T, epsilon)

    print('transformed_7D.shape:')
    print(transformed_7D.shape)

    # Print first 10 transformed_6D 
    headers = ["v_n", "v_n+1", "v_n+2"]
    print("\n first 10 transformed_7D:--------------------")
    list_format = [tuple(row) for row in transformed_7D.T[:10]]
    print(tabulate(list_format, headers=headers, floatfmt=".4f"))

    fig7D = plt.figure(figsize=(20, 15))
    ax = fig7D.add_subplot(1, 1, 1, projection='3d')
    x_vals, y_vals, z_vals = transformed_7D
    ax.scatter(x_vals, y_vals, z_vals, color='r',s=1, marker='o', label='transformed_7D')





    # # Print first 10 compressed data points
    # print("\nFirst 10 compressed 3D data points from 4D:")
    # compressed_headers = ["x", "y", "z"]
    # print(tabulate(compressed_method1_4D_to_v3D[:10], headers=compressed_headers, floatfmt=".4f"))
    
    # Visualize compressed 3D data points
    ax2 = fig.add_subplot(3, 5, 2, projection='3d')
    xs, ys, zs = zip(*compressed_method1_4D_to_v3D)
    ax2.scatter(xs, ys, zs, s=1, c='r')
    ax2.set_title("Compressed 3D Data Points from 4D")

    show_ref()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
