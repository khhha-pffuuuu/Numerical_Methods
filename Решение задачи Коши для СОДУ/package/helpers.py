import numpy as np


def diff_equation(x: float, y: np.ndarray) -> np.ndarray:
    """Дифференциальное уравнение"""
    dy = np.array([
        y[1] / 35,
        -y[0] / 10
    ])

    return dy


def real_y(x_start: float, y_start: np.ndarray, x_end: float) -> np.ndarray:
    """Реальное решение задачи Коши"""

    # Подбор констант для решения задачи Коши
    C = (y_start[1] * np.sin(x_start / 5 / np.sqrt(14)) / 7 -
         y_start[0] * np.cos(x_start / 5 / np.sqrt(14)) / np.sqrt(14))
    C1 = (y_start[1] * np.cos(x_start / 5 / np.sqrt(14)) / 7 +
          y_start[0] * np.sin(x_start / 5 / np.sqrt(14)) / np.sqrt(14))

    # Решение задачи Коши
    y_end = np.array([
        np.sqrt(14) * C1 * np.sin(x_end / 5 / np.sqrt(14)) - np.sqrt(14) * C * np.cos(x_end / 5 / np.sqrt(14)),
        7 * C * np.sin(x_end / 5 / np.sqrt(14)) + 7 * C1 * np.cos(x_end / 5 / np.sqrt(14)),
    ])

    return y_end


def compact_list(a: list or np.ndarray, length: int) -> list:
    """Сжимаем список до заданной длины length"""
    return [np.mean(a[i * len(a) // length: (i + 1) * len(a) // length]) for i in range(length)]
