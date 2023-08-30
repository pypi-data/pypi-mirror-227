import math
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
        # Your cube edges go here, same as you provided.
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

def higherD_to_v3D(array_higherD, epsilon):
    if array_higherD.shape[0] < 4:
        raise ValueError("Input array must have at least shape 4xN")
    
    transformed = [transform_u_to_v(u, epsilon) for u in array_higherD.T]
    
    while len(transformed[0]) < 3:
        transformed = [transform_u_to_v(u, epsilon) for u in transformed]
        
    return np.array(transformed).T


def main():
    # 生成一些测试数据
    test_data_4D = np.array([
        [0.1, 0.5, 0.3, 0.7],  # u1
        [0.6, 0.4, 0.2, 0.8],  # u2
        [0.9, 0.3, 0.1, 0.5],  # u3
        [0.4, 0.6, 0.7, 0.2]   # u4
    ])
    
    epsilon = 0.01

    transformed_data = higherD_to_v3D(test_data_4D, epsilon)
    
    print("Transformed Data (3D):\n", transformed_data)

if __name__ == "__main__":
    main()

