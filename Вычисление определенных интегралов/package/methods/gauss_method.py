import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt

from ..helpers import cardano_formula, moment


def quad_gauss(func, a: float, b: float, alpha: float = 0, beta: float = 0, num_partitions: int = 100) -> float:
    """Квадратичная формула Гаусса"""
    if alpha == 0:  # Для удобства подсчета моментов, заменим переменную интегрирования
        bias, func_ = b, lambda x: func(bias - x)
    else:
        bias, func_ = a, lambda x: func(x + bias)

    a, b = 0, b - a

    result = 0
    num_nodes = 3

    for i in range(num_partitions):
        l_border = a + (b - a) * i / num_partitions
        r_border = a + (b - a) * (i + 1) / num_partitions

        # Вычисляем моменты 0,...,2n-1
        moments = np.array([moment(l_border, r_border, alpha, beta, i) for i in range(2 * num_nodes)])

        # Решим СЛАУ для нахождения коэффициентов уравнения
        n_range = np.arange(num_nodes)
        mu_matrix = moments[n_range.reshape(-1, 1) + n_range]
        mu_vector = moments[num_nodes:]
        a_coeffs = solve(mu_matrix, -mu_vector).flatten()

        # Корни уравнения являются узлами
        poly_coeffs = np.append([1], a_coeffs[::-1])
        nodes = cardano_formula(poly_coeffs)

        # Решаем последнюю СЛАУ и получаем квадратурные коэффициенты
        nodes_matrix = np.array([nodes ** s for s in range(num_nodes)])

        mu_vector = moments[:num_nodes]
        A_coeffs = solve(nodes_matrix, mu_vector)

        result += A_coeffs @ func_(nodes)

    return result
