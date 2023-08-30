import math
import matplotlib.pyplot as plt
import numpy as np

from kanggenetools.transform import u_to_v  # 使用之前提到的模块和函数

def visualize_points(original_points, transformed_values_4D, transformed_values_5D):
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # 绘制原始点
    orig_x, orig_y, orig_z = zip(*original_points)
    axs[0].scatter(orig_x, orig_y, color='blue', label="Original values")
    axs[0].set_xlabel('u1')
    axs[0].set_ylabel('u2')
    axs[0].legend()

    # 绘制4D转换后的点
    t4D_x, t4D_y, t4D_z = zip(*transformed_values_4D)
    axs[1].scatter(t4D_x, t4D_y, color='red', label="Transformed 4D values")

    # 绘制5D转换后的点
    t5D_x, t5D_y, t5D_z = zip(*transformed_values_5D)
    axs[1].scatter(t5D_x, t5D_y, color='green', label="Transformed 5D values")
    axs[1].set_xlabel('v1')
    axs[1].set_ylabel('v2')
    axs[1].legend()

    plt.tight_layout()
    plt.show()

def user_side_test():
    u_1, u_2, u_3, u_4, u_5 = 0.6, 0.5, 0.4, 0.3, 0.2
    epsilon = 0.8

    v1_4D, v2_4D, v3_4D = u_to_v(u_1, u_2, u_3, u_4, epsilon)
    v1_5D, v2_5D, v3_5D = u_to_v(v1_4D, v2_4D, v3_4D, u_5, epsilon)

    original_points = [[u_1, u_2, u_3]]
    transformed_values_4D = [[v1_4D, v2_4D, v3_4D]]
    transformed_values_5D = [[v1_5D, v2_5D, v3_5D]]
    
    visualize_points(original_points, transformed_values_4D, transformed_values_5D)

    print("\nOriginal values:")
    print(f"u1: {u_1}, u2: {u_2}, u3: {u_3}, u4: {u_4}, u5: {u_5}")

    print("\nAfter first transformation (4D):")
    print(f"v1: {v1_4D}, v2: {v2_4D}, v3: {v3_4D}")

    print("\nAfter second transformation (5D):")
    print(f"v1: {v1_5D}, v2: {v2_5D}, v3: {v3_5D}")

if __name__ == "__main__":
    user_side_test()