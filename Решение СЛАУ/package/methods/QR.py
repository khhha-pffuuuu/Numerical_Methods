from ..matrix import Matrix


def QR(A: Matrix, b: Matrix) -> Matrix:
    """Метод разложения матрицы на треугольную и ортонормированную."""
    n = A.dim[0]
    E = Matrix.E(n)

    # Проводим QR-разложение
    Q = E.copy
    R = A.copy
    for i in range(n - 1):
        # Выводим матрицу H
        y = Matrix([[R[j, i]] for j in range(i, n)])
        z = Matrix([[E[j, i]] for j in range(i, n)])

        a = abs(y)
        p = abs(y - z * a)
        w = (y - z * a) / p

        H = E.copy
        H_ = Matrix.E(n - i) - 2 * w * ~w
        for j in range(i, n):  # "Вкладываем" вычисленную нами матрицу в единичную матицу
            for k in range(i, n):
                H[j, k] = H_[j - i, k - i]

        Q = Q * ~H
        R = H * R

    # Решаем систему Rx = ~Qb
    y = ~Q * b
    x = Matrix.NULL_VECTOR(n)
    for k in reversed(range(n)):
        x[k, 0] = y[k, 0] / R[k, k]
        for i in range(k + 1, n):
            x[k, 0] -= R[k, i] * x[i, 0] / R[k, k]

    return x
