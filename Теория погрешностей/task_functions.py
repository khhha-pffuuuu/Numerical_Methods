import math


def fact(n):
    res = 1
    for i in range(1, n + 1):
        res *= i

    return res


def sqrt(x):
    eps = 6.4 * 10**-7
    res = x / 2

    while True:
        res_ = 1 / 2 * (res + x / res)
        if abs(res - res_) < eps:
            return res_
        res = res_


def cos(x):
    eps = 1.1 * 10**-6
    res = 0
    n = 0

    while True:
        res_ = res + (-1)**n * x**(2 * n) / fact(2 * n)
        if abs(res_ - res) < eps:
            return res_
        res = res_
        n += 1


def arctan(x):
    eps = 3.5 * 10 ** -7
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
        res = math.pi / 2 * x / abs(x)
        while True:
            res_ = res - (-1) ** n * x ** -(2 * n + 1) / (2 * n + 1)
            if abs(res_ - res) < eps:
                return res_
            res = res_
            n += 1
