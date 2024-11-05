import numpy as np


def richardson(quad, gap_len: float, min_part: int = 1, max_part: int = np.inf, eps: float = 10 ** -12):
    """Метод Ричардсона для оценки погрешностей интегралов"""
    r, R = 2, np.inf  # Для начала считаем, что количество сеток равно 2, а погрешность равна бесконечности
    best_step, best_part = 0, 0

    while R > eps and 2 ** r * min_part <= max_part:
        # Значения интегралов при разных шагах разбиения
        values = [quad(n=2 ** i * min_part) for i in range(r + 1)]
        # По формуле Эйткена находим скорость сходимости
        m = -np.log((values[-1] - values[-2]) / (values[-2] - values[-3])) / np.log(2)

        steps = [gap_len / (2 ** i * min_part) for i in range(r + 1)]

        steps_matrix = np.array([[-1] + [steps[j] ** (m + i) for i in range(r)] for j in range(r + 1)])
        values_vector = np.array(values[:r + 1])

        # Находим уточненный по Ричардсону интеграл
        J, *_ = np.linalg.solve(steps_matrix, -values_vector)

        cur_R = abs(J - values_vector[-1])
        if cur_R < R:
            best_part = int(gap_len / steps[-1])
            best_step = steps[-1]
            R = cur_R

        r += 1

    return R, best_step, best_part
