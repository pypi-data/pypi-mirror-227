import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


import kanggenetools
kanggenetools.authorize("kangtools")
from kanggenetools.transform import u_to_v  # 使用之前提到的模块和函数



def generate_cube_points(lower, upper, points_per_edge):
    coordinates = [lower, upper]
    points = []

    for coord in coordinates:
        for i in range(points_per_edge):
            fraction = i / (points_per_edge - 1)
            point = [
                lower + fraction * (upper - lower),
                coord,
                coord
            ]
            points.append(point)
            
            point = [
                coord,
                lower + fraction * (upper - lower),
                coord
            ]
            points.append(point)

            point = [
                coord,
                coord,
                lower + fraction * (upper - lower)
            ]
            points.append(point)

    return points

def visualize_3D(points_original, points_transformed):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    x_original, y_original, z_original = zip(*points_original)
    x_transformed, y_transformed, z_transformed = zip(*points_transformed)

    ax.scatter(x_original, y_original, z_original, color='blue', label='Original points')
    ax.scatter(x_transformed, y_transformed, z_transformed, color='red', marker='^', label='Transformed points')
    
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.legend()

    plt.show()

def main():
    lower, upper = 0.1, 1
    points_per_edge = 10

    cube_points = generate_cube_points(lower, upper, points_per_edge)
    transformed_points = [u_to_v(p[0], p[1], p[2], 0.1, 0.8)[:3] for p in cube_points]

    visualize_3D(cube_points, transformed_points)

if __name__ == "__main__":
    main()
