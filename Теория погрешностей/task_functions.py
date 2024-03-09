from math import pi


def fact(n: int) -> int:
    """Вычисление факториала(только для натуральных чисел)"""
    res = 1
    for i in range(1, n + 1):
        res *= i

    return res


def sqrt(x: float) -> float:
    """Поиск значения корня при помощи формулы Герона"""
    eps = 6.4 * 10**-7  # Высчитанная точность функции
    res = x / 2

    while True:
        res_ = 1 / 2 * (res + x / res)
        if abs(res - res_) < eps:
            return res_
        res = res_


def cos(x: float) -> float:
    """Разложение в ряд Тейлора функции cos"""
    eps = 1.1 * 10**-6  # Высчитанная точность функции
    res = 0
    n = 0

    while True:
        res_ = res + (-1)**n * x**(2 * n) / fact(2 * n)
        if abs(res_ - res) < eps:
            return res_
        res = res_
        n += 1


def arctan(x: float) -> float:
    """Разложение в ряд Тейлора функции sin"""
    eps = 3.5 * 10 ** -7  # Высчитанная точность функции
    n = 0

    if abs(x) < 1:
        res = 0
        while True:
            res_ = res + (-1) ** n * x ** (2 * n + 1) / (2 * n + 1)
            if abs(res_ - res) < eps:
                return res_
            res = res_
            n += 1
    else:
        res = pi / 2 * x / abs(x)
        while True:
            res_ = res - (-1) ** n * x ** -(2 * n + 1) / (2 * n + 1)
            if abs(res_ - res) < eps:
                return res_
            res = res_
            n += 1
