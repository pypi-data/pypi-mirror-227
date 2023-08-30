import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import kanggenetools
kanggenetools.authorize("kangtools")
from kanggenetools.transform import u_to_v  # 使用之前提到的模块和函数




def generate_cube_edges(lower, upper, points_per_edge):
    edges = []
    for edge_start in [(lower, lower, lower), 
                       (lower, upper, lower), 
                       (upper, lower, lower), 
                       (upper, upper, lower),
                       (lower, lower, upper), 
                       (lower, upper, upper), 
                       (upper, lower, upper), 
                       (upper, upper, upper)]:
        for axis in range(3):  # x, y, z axis
            edge = []
            for i in range(points_per_edge):
                fraction = i / (points_per_edge - 1)
                point = list(edge_start)
                point[axis] = lower + fraction * (upper - lower)
                edge.append(tuple(point))
            edges.extend(edge)

    # Removing duplicate points
    edges = list(dict.fromkeys(edges))
    return edges



def visualize_3D(points_original, transformed_points_4D=None, transformed_points_5D=None):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    x_original, y_original, z_original = zip(*points_original)
    ax.scatter(x_original, y_original, z_original, color='blue', label='Original points')
    
    if transformed_points_4D:  # If the list is not empty
        x_4D, y_4D, z_4D = zip(*transformed_points_4D)
        ax.scatter(x_4D, y_4D, z_4D, color='green', marker='^', label='Transformed 4D points')
    
    if transformed_points_5D:  # If the list is not empty
        x_5D, y_5D, z_5D = zip(*transformed_points_5D)
        ax.scatter(x_5D, y_5D, z_5D, color='red', marker='s', label='Transformed 5D points')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.legend()

    plt.show()


def iterative_sequence(N):
    sequence = [0.5]
    for _ in range(N - 1):
        next_val = 0.5 * sequence[-1] + 0.5
        sequence.append(next_val)
    return sequence

def generate_point_sets(sequence):
    three_point_set = [(sequence[i], sequence[i+1], sequence[i+2]) for i in range(len(sequence) - 2)]
    four_point_set = [(sequence[i], sequence[i+1], sequence[i+2], sequence[i+3]) for i in range(len(sequence) - 3)]
    return three_point_set, four_point_set

def main():
    lower, upper = 0.1, 1
    points_per_edge = 10
    
    cube_edges = generate_cube_edges(lower, upper, points_per_edge)
    transformed_points_4D = [u_to_v(p[0], p[1], p[2], 0.1, 0.8)[:3] for p in cube_edges]
    transformed_points_5D = [u_to_v(p[0], p[1], p[2], 0.1, 0.2)[:3] for p in transformed_points_4D]

    # visualize_3D(cube_edges, transformed_points_4D, transformed_points_5D)

    # 3. Generate iterative sequence
    N = 500
    sequence = iterative_sequence(N)
    print("First 20 values of the sequence:", sequence[:20])

    # 4-5. Create point sets
    three_point_set, four_point_set = generate_point_sets(sequence)
    
    # 6. Compress 3-point set
    compressed_3point = [u_to_v(p[0], p[1], p[2], 0.1, 0.8)[:3] for p in three_point_set]
    visualize_3D(three_point_set, [], compressed_3point)
    
    # 7-8. Compress 4-point set
    compressed_4point = [u_to_v(p[0], p[1], p[2], p[3], 0.8)[:3] for p in four_point_set]
    visualize_3D(four_point_set, [], compressed_4point)

if __name__ == "__main__":
    main()

