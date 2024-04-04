from ..matrix import Matrix
from ..helpers import is_dd


def Gauss_Seidel(A: Matrix, b: Matrix, eps: float) -> tuple:
    """Метод Якоби + итерации Зейделя(ищем новое приближение не сразу, а покоординатно)"""
    n = A.dim[0]
    E = Matrix.E(n)

    # Проверяем два достаточных условия сходимости
    if not is_dd(A):
        T = ~A
        A, b = T * A, T * b

    B = E.copy
    c = Matrix.zeros(n, 1)
    for i in range(n):
        c[i] = b[i] / A[i, i]
        for j in range(n):
            B[i, j] = -A[i, j] / A[i, i] if i != j else 0

    B_norm = B.norm('inf')  # Затем используется для критерия остановки
    x = c.copy  # За начальное приближение берут часто именно вектор c

    k = 0
    # Выполняем итерации, пока не достигнем ответа достаточной точности
    while True:
        x_ = x.copy
        k += 1

        # Покоординатно считаем новое приближение x
        for i in range(n):
            row_sum = 0
            for j in range(n):
                if i != j:
                    row_sum += B[i, j] * x_[j]
                else:
                    row_sum += c[i]
            x_[i] = row_sum

        # Проверяем, меньше ли норма B единицы, если да, то используем апостериорную оценку, иначе смотрим неявку
        if B_norm < 1 and B_norm / (1 - B_norm) * (x_ - x).norm('inf') < eps:
            return x_, k
        elif B_norm >= 1 and abs(A * x_ - b) < eps:
            return x_, k

        x = x_.copy
