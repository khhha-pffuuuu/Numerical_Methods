import numpy as np
from numpy.linalg import solve

from ..helpers import moment


def quad_newton_cotes(func, a: float, b: float, alpha: float = 0, beta: float = 0, num_partitions: int = 100):
    """Квадратичная формула Ньютона-Котса"""
    if alpha == 0:  # Для удобства подсчета моментов, заменим переменную интегрирования
        bias, func_ = b, lambda x: func(bias - x)
    else:
        bias, func_ = a, lambda x: func(x + bias)

    a, b = 0, b - a

    result = 0
    num_nodes = 3

    for i in range(num_partitions):
        nodes = [a + (b - a) * i / num_partitions,
                 a + (b - a) * (i + 1 / 2) / num_partitions,
                 a + (b - a) * (i + 1) / num_partitions]


        # Составляем СЛАУ и решаем
        mu_vector = np.array([moment(nodes[0], nodes[2], alpha, beta, i) for i in range(num_nodes)])

        nodes = np.array(nodes)
        nodes_matrix = np.array([nodes ** s for s in range(num_nodes)])

        A_coeffs = solve(nodes_matrix, mu_vector)

        result += A_coeffs @ func_(nodes)

    return result
