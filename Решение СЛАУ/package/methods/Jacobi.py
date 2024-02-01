from ..matrix import Matrix


def Jacobi(A: Matrix, b: Matrix, eps: float) -> tuple:
    """В методе мы раскладываем матрицу A на три матрицы с элементами под, на и над элементами диагонали."""
    n = A.dim[0]

    B = Matrix([[0 for _ in range(n)] for _ in range(n)])
    c = Matrix.NULL_VECTOR(n)

    # Строим матрицу B и вектор c в соответствии с алгоритмом из курса
    for i in range(n):
        c[i, 0] = b[i, 0] / A[i, i]
        for j in range(n):
            if i != j:
                B[i, j] = -A[i, j] / A[i, i]

    B_norm = B.norm('inf')  # Затем используется для критерия остановки
    x = c.copy  # За начальное приближение берут часто именно вектор c

    k = 0
    # Выполняем итерации, пока не достигнем ответа достаточной точности
    while True:
        x_ = B * x + c
        k += 1

        # Проверяем, меньше ли норма B единицы, если да, то используем апостериорную оценку, иначе смотрим неявку
        if B_norm < 1 and B_norm / (1 - B_norm) * (x_ - x).norm('inf') < eps:
            return x_, k
        elif B_norm >= 1 and abs(A * x_ - b) < eps:
            return x_, k

        x = x_.copy
