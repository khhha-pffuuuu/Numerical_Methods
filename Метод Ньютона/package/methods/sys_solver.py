from ..matrix import Matrix


def LUP(A: Matrix, b: Matrix) -> Matrix:
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
    y = Matrix.NULL_VECTOR(n)
    for k in range(n):
        y[k, 0] = Pb[k, 0]
        for i in range(k):
            y[k, 0] -= L[k, i] * y[i, 0]

    x = Matrix.NULL_VECTOR(n)
    for k in reversed(range(n)):
        x[k, 0] = y[k, 0] / U[k, k]
        for i in range(k + 1, n):
            x[k, 0] -= U[k, i] * x[i, 0] / U[k, k]

    return x


def approach(Function, Function_derivative) -> Matrix:
    """Функция приближенного поиска решения системы с помощью метода Ньютона"""
    n = 10  # Ранг дробления Ф(x,y,l)

    # Начальные значения x, y
    x, y = 0, 0
    values = Matrix([[x], [y]])

    i = 1
    while i <= 10:
        # Обновляем x, y
        delta_x = LUP(Function_derivative(x, y), Function(x, y, i / n))
        values = delta_x + values

        x, y = [values[i, 0] for i in range(values.dim[0])]  # Достаем значения из матрицы
        i += 1

    return values


def sys_root_search(Function, Function_derivative) -> Matrix:
    """Непосредственно сам метод Ньютона(классический) для систем уравнений"""
    eps = 10 ** -4  # Заданная погрешность

    # Высчитываем первое приближение к корню
    values = approach(Function, Function_derivative)
    x, y = [values[i, 0] for i in range(values.dim[0])]

    while True:
        # Решаем систему derF * dx = F и обновляем значения x, y
        delta_x = LUP(Function_derivative(x, y), Function(x, y))
        values_ = delta_x + values

        if abs(values_ - values) < eps:
            return values_

        values = values_
        x, y = [values[i, 0] for i in range(values.dim[0])]  # Достаем значения из матрицы
