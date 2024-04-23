from math import acos, cos, pi


def func(x):
    """Заданная функция в лабораторной работе"""
    if isinstance(x, list):
        return [((x_ / 10) ** 2 + 1 - acos(x_ / 10)) * 10 for x_ in x]
    else:
        return ((x / 10) ** 2 + 1 - acos(x / 10)) * 10


def uniform_points(left: float, right: float, n: int) -> list:
    """Функция, вычисляющая точки равномерного разбиения(важно учесть, что список идет от right до left)"""
    return [right - i * (right - left) / n for i in range(n + 1)]


def optimal_points(left: float, right: float, n: int) -> list:
    """Функция, вычисляющая точки 'оптимального' разбиения(важно учесть, что список идет от right до left)"""
    points = [((right - left) * cos((2 * i + 1) / (2 * n + 2) * pi) + (right + left)) / 2 for i in range(n + 1)]
    points[0], points[-1] = right, left  # Чтобы полностью покрыть промежуток, меняем крайние элементы
    return points


def deviations(function, function_, left: float, right: float, n: int) -> list:
    """Функция вычисляет отклонение в m точках между двумя функциями(важно учесть, что список идет от right до left)"""
    args = uniform_points(left, right, n)
    res = []

    for arg in args:
        res.append(abs(function(arg) - function_(arg)))

    return res
