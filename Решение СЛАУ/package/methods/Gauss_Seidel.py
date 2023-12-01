from ..matrix import Matrix


def Gauss_Seidel(A, b, eps):
    n = A.dim[0]
    E = Matrix.E(n)

    # Проверяем два достаточных условия сходимости
    if not A.is_dd:
        T = ~A
        A, b = T * A, T * b

    B = E.copy
    c = Matrix.NULL_VECTOR(n)
    for i in range(n):
        c[i, 0] = b[i, 0] / A[i, i]
        for j in range(n):
            B[i, j] = -A[i, j] / A[i, i] if i != j else 0

    x = c.copy

    k = 0
    # Выполняем итерации, пока не достигнем ответа достаточной точности
    while True:
        x_ = x.copy
        k += 1

        for i in range(n):
            row_sum = 0
            for j in range(n):
                if i != j:
                    row_sum += B[i, j] * x_[j, 0]
                else:
                    row_sum += c[i, 0]
            x_[i, 0] = row_sum

        if abs(A * x_ - b) < eps:
            return x_, k

        x = x_.copy
