from math import pi


def sqrt(x: float) -> float:
    """Поиск значения корня при помощи формулы Герона"""
    eps = 6.4 * 10 ** -7  # Высчитанная точность функции
    val = x / 2

    while True:
        val_ = 1 / 2 * (val + x / val)
        if abs(val - val_) < eps:
            return val_
        val = val_


def cos(x: float) -> float:
    """Разложение в ряд Тейлора функции cos"""
    eps = 1.1 * 10 ** -6  # Высчитанная точность функции
    val = 0
    fact = 1
    n = 0

    while True:
        val_ = val + (-1) ** n * x ** (2 * n) / fact
        if abs(val_ - val) < eps:
            return val_
        val = val_
        fact *= 2 * (n + 1) * (2 * n + 1)
        n += 1


def arctan(x: float) -> float:
    """Разложение в ряд Тейлора функции sin"""
    eps = 3.5 * 10 ** -7  # Высчитанная точность функции
    n = 0

    if abs(x) < 1:
        val = 0
        while True:
            val_ = val + (-1) ** n * x ** (2 * n + 1) / (2 * n + 1)
            if abs(val_ - val) < eps:
                return val_
            val = val_
            n += 1
    else:
        val = pi / 2 * x / abs(x)
        while True:
            val_ = val - (-1) ** n * x ** -(2 * n + 1) / (2 * n + 1)
            if abs(val_ - val) < eps:
                return val_
            val = val_
            n += 1
