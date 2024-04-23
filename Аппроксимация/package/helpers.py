from math import cos
import random


def func(x: float or list[float]) -> float or list[float]:
    """Заданная функция"""
    if isinstance(x, int) or isinstance(x, float):
        return x ** 2 * cos(x)
    else:  # Можно возвращать список значений
        return [x_ ** 2 * cos(x_) for x_ in x]


def uniform_points(a: float, b: float, m: int, k=1) -> list[float]:
    """Равномерное разбиение [a, b] на m точек с k повторениями"""
    points = []
    for i in range(m):
        points += [a + i * (b - a) / (m - 1)] * k
    return points


def values_generator(args: list[float]) -> list[float]:
    """Генератор данных. Каждой точке дает значение заданной выше функции с погрешностью не более 0.1"""
    vals = func(args)
    data_set = []

    for val in vals:
        data_set.append(val + (random.random() - 0.5) / 5)

    return data_set


def Loss(values: list[float], calculated_values: list[float]) -> float:
    """Функция потерь, то есть сумма квадратов разности отклонений"""
    loss = 0  # Значение потери

    for i in range(len(values)):
        loss += (values[i] - calculated_values[i]) ** 2

    return loss
