import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from mpl_toolkits.mplot3d import Axes3D

import kanggenetools
kanggenetools.authorize("kangtools")
from kanggenetools.transform import u_to_v

def logistic_map(a, u_initial, N):
    u_values = [u_initial]
    for n in range(1, N):
        u_next = a * u_values[-1] * (1 - u_values[-1])
        u_values.append(u_next)
    return u_values

def extract_sequences(sequence, dim):
    return [tuple(sequence[i:i+dim]) for i in range(len(sequence) - dim + 1)]

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
    ax1 = fig.add_subplot(4, 4, 1, projection='3d')
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
    
    # Compress 4D data to 3D
    compressed_3D = [u_to_v(p[0], p[1], p[2], p[3], 0.8)[:3] for p in four_dim_data]

    # prepare 
    # Extracting 5D data points
    five_dim_data = extract_sequences(sequence, 5)
    print(f"preparefor 5D----Total 5D data points: {len(five_dim_data)}")  # This should be N-3
    
    # Print first 10 5D data points
    headers = ["u_n", "u_n+1", "u_n+2", "u_n+3", "u_n+4"]
    print("\nFirst 10 5D data points:")
    print(tabulate(five_dim_data[:10], headers=headers, floatfmt=".4f"))


    # Print first 10 compressed data points
    print("\nFirst 10 compressed 3D data points from 4D:")
    compressed_headers = ["x", "y", "z"]
    print(tabulate(compressed_3D[:10], headers=compressed_headers, floatfmt=".4f"))
    
    # Visualize compressed 3D data points
    ax2 = fig.add_subplot(4, 4, 2, projection='3d')
    xs, ys, zs = zip(*compressed_3D)
    ax2.scatter(xs, ys, zs, s=1, c='r')
    ax2.set_title("Compressed 3D Data Points from 4D")

    plt.tight_layout()
    # plt.show()

if __name__ == '__main__':
    main()
