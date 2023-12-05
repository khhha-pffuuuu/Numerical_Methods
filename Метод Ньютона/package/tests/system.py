from math import cos, sin

from ..matrix import Matrix


def Function(x, y, l=1.0) -> Matrix:
    return Matrix([[l * cos(y) + x - 3 / 2], [2 * y - l * sin(x - 0.5) - 1]]) * -1


def Function_derivative(x, y) -> Matrix:
    return Matrix([[1, -cos(x - 0.5)], [-sin(y), 2]])
