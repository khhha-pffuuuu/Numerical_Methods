from math import cos, sin

from Интерполяция.package.matrix import Matrix


def Function(x, y, l=1.0) -> Matrix:
    return Matrix([[l * cos(y) + x - 3 / 2], [2 * y - l * sin(x - 0.5) - 1]])


def Function_derivative(x, y, l=1.0) -> Matrix:
    return Matrix([[1, l * -cos(x - 0.5)], [l * -sin(y), 2]])
