from .basic_methods import *
from .gauss_method import *
from .newton_cotes_method import *


def quad(func, a: float, b: float, method: str = 'Simpson',
         alpha: float = 0, beta: float = 0, num_partitions: int = 100) -> float:
    if method == 'Left Rectangle':
        return quad_left_rect(func, a, b, num_partitions)

    elif method == 'Right Rectangle':
        return quad_right_rect(func, a, b, num_partitions)

    elif method == 'Middle Rectangle':
        return quad_middle_rect(func, a, b, num_partitions)

    elif method == 'Trapezia':
        return quad_trapezia(func, a, b, num_partitions)

    elif method == 'Simpson':
        return quad_simpson(func, a, b, num_partitions)

    elif method == 'Gauss':
        return quad_gauss(func, a, b, alpha, beta, num_partitions)

    elif method == 'Newton Cotes':
        return quad_newton_cotes(func, a, b, alpha, beta, num_partitions)
