from .matrix import Matrix
from math import acos, cos, pi


def func(x: float) -> float:
    """Заданная функция в лабораторной работе"""
    return ((x / 10) ** 2 + 1 - acos(x / 10)) * 10


def uniform_points(left: float, right: float, n: int) -> list:
    """Функция, вычисляющая точки равномерного разбиения(важно учесть, что список идет от right до left)"""
    return [right - i * (right - left) / n for i in range(n + 1)]


def optimal_points(left: float, right: float, n: int) -> list:
    """Функция, вычисляющая точки 'оптимального' разбиения(важно учесть, что список идет от right до left)"""
    return [((right - left) * cos((2 * i + 1) / (2 * n + 2) * pi) + (right + left)) / 2 for i in range(n + 1)]


def deviations(function, function_, left: float, right: float, n: int) -> list:
    """Функция вычисляет отклонение в m точках между двумя функциями"""
    args = [left] + [left + (right - left) / n * i for i in range(1, n)] + [right]
    res = []

    for arg in args:
        res.append(abs(function(arg) - function_(arg)))

    return res


def LUP(A: Matrix, b: Matrix) -> Matrix:
    """Имплементация метода Гаусса. Метод разложения матрицы на треугольные."""
    n = A.dim[0]
    E = Matrix.E(n)

    M = A.copy
    P = E.copy

    for i in range(n - 1):
        # Определяем строку с максимальным по модулю элементом
        max_i = i

        for j in range(i, n):
            max_i = j if abs(M[max_i, i]) < abs(M[j, i]) else max_i

        # Выполняем перестановку в матрицах P и M, меняя строки местами
        for matrix in [P, M]:
            add_vector = matrix[max_i, None]
            matrix[max_i, None] = matrix[i, None]
            matrix[i, None] = add_vector

        # Преобразуем матрицу M
        for j in range(i + 1, n):
            M[j, i] = M[j, i] / M[i, i]
            for k in range(i + 1, n):
                M[j, k] = M[j, k] - M[j, i] * M[i, k]

    # Проводим LU-разложение
    L = E.copy
    U = E.copy
    for i in range(n):
        for j in range(n):
            if i > j:
                L[i, j] = M[i, j]
            elif i < j:
                U[i, j] = M[i, j]
            else:
                L[i, i] = 1
                U[i, i] = M[i, i]

    # Решаем систему Ly = Pb и Ux = y
    Pb = P * b
    y = Matrix.zeros(n, 1)
    for k in range(n):
        y[k, 0] = Pb[k, 0]
        for i in range(k):
            y[k, 0] -= L[k, i] * y[i, 0]

    x = Matrix.zeros(n, 1)
    for k in reversed(range(n)):
        x[k, 0] = y[k, 0] / U[k, k]
        for i in range(k + 1, n):
            x[k, 0] -= U[k, i] * x[i, 0] / U[k, k]

    return x
