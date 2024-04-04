from ..matrix import Matrix


def FPIM(A: Matrix, b: Matrix, eps: float) -> tuple:
    """Базовый итерационный метод решения СЛАУ"""
    n = A.dim[0]
    E = Matrix.E(n)

    mu = 1 / A.norm('inf')
    B = E - mu * A
    B_norm = B.norm('inf')  # Затем используется для критерия остановки

    # Проверяем два достаточных условия сходимости МПИ
    if B_norm >= 1:
        T = ~A
        A, b = T * A, T * b

        mu = 1 / A.norm('inf')
        B = E - mu * A
        B_norm = B.norm('inf')

    c = mu * b
    x = c.copy   # За начальное приближение берут часто именно вектор c

    k = 0
    # Выполняем итерации, пока не достигнем ответа достаточной точности
    while True:
        x_ = B * x + c
        k += 1

        if B_norm < 1 and B_norm / (1 - B_norm) * (x_ - x).norm('inf') < eps:
            return x_, k
        elif B_norm >= 1 and abs(A * x_ - b) < eps:
            return x_, k

        x = x_.copy
