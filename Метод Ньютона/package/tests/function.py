import math


def function(x) -> float:
    return x ** 2 + 1 - math.acos(x)


def function_derivative(x) -> float:
    return 2 * x + x / math.sqrt(1 - x ** 2)
