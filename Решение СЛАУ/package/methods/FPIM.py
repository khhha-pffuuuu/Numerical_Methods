from ..matrix import Matrix


def FPIM(A: Matrix, b: Matrix, eps):
    n = A.dim[0]
    E = Matrix.E(n)

    mu = 1 / A.norm('inf')
    B = E - mu * A

    # Проверяем два достаточных условия сходимости МПИ
    if B.norm('inf') >= 1:
        if not A.is_pd:
            T = ~A
            A, b = T * A, T * b

            mu = 1 / A.norm('inf')
            B = E - mu * A

    c = mu * b
    x = c.copy

    k = 0
    # Выполняем итерации, пока не достигнем ответа достаточной точности
    while True:
        x_ = B * x + c
        k += 1

        if abs(A * x_ - b) < eps:
            return x_, k

        x = x_.copy
