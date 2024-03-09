from Интерполяция.package.matrix import Matrix
from ..helpers import LUP


def approach(Func, Func_der) -> Matrix:
    """Функция приближенного поиска решения системы с помощью метода Ньютона"""
    n = 10  # Ранг дробления Ф(x,y,l)

    # Начальные значения x, y
    values = Matrix.zeros(2, 1)
    x, y = values[0], values[1]

    i = 0
    while i <= n:
        # Обновляем x, y
        delta_x = LUP(Func_der(x, y, i / n), -1 * Func(x, y, i / n))
        values = delta_x + values

        x, y = [values[i] for i in range(values.dim[0])]  # Достаем значения из матрицы
        i += 1

    return values


def sys_root_search(Func, Func_der) -> Matrix:
    """Непосредственно сам метод Ньютона(классический) для систем уравнений"""
    eps = 10 ** -4  # Заданная погрешность

    # Высчитываем первое приближение к корню
    values = approach(Func, Func_der)
    x, y = values[0], values[1]

    while True:
        # Решаем систему derF * dx = F и обновляем значения x, y
        delta_x = LUP(Func_der(x, y), -1 * Func(x, y))
        values_ = delta_x + values

        if abs(values_ - values) < eps:
            return values_

        values = values_
        x, y = values[0], values[1]  # Достаем значения из матрицы
