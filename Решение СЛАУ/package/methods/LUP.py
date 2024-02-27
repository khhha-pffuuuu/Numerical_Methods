from ..matrix import Matrix


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
        y[k] = Pb[k]
        for i in range(k):
            y[k] -= L[k, i] * y[i]

    x = Matrix.zeros(n, 1)
    for k in reversed(range(n)):
        x[k] = y[k] / U[k, k]
        for i in range(k + 1, n):
            x[k] -= U[k, i] * x[i] / U[k, k]

    return x
