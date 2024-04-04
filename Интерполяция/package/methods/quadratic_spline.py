from СЛАУ.package.matrix import Matrix
from СЛАУ.package.methods.LUP import LUP


def quadratic_spline_coeffs(args: list, vals: list, cond: float) -> Matrix:
    """Функция поиска коэффициентов квадратичного сплайна"""
    n = len(args)

    # (Вкратце) Представляем систему уравнений в виде СЛАУ и решим ее
    X = Matrix.zeros(3 * (n - 1))
    y = Matrix.zeros(3 * (n - 1), 1)
    y[-1] = cond  # Граничное условие

    for i in range(n - 1):
        X[3 * i, 3 * i], X[3 * i, 3 * i + 1], X[3 * i, 3 * i + 2] = args[i] ** 2, args[i], 1
        X[3 * i + 1, 3 * i], X[3 * i + 1, 3 * i + 1], X[3 * i + 1, 3 * i + 2] = args[i + 1] ** 2, args[i + 1], 1
        X[3 * i + 2, 3 * i], X[3 * i + 2, 3 * i + 1] = 2 * args[i + 1], 1
        if i != n - 2:
            X[3 * i + 2, 3 * i + 3], X[3 * i + 2, 3 * i + 4] = -2 * args[i + 1], -1

        y[3 * i], y[3 * i + 1] = vals[i], vals[i + 1]

    return LUP(X, y)  # Возвращаем решение СЛАУ - вектор, содержащий коэффициенты уравнений системы


def quadratic_spline(x: float, args: list, coeffs: Matrix) -> int:
    """Функция квадратичного сплайна"""
    n = len(args)

    for i in range(n - 1):
        if min(args[i], args[i + 1]) <= x <= max(args[i], args[i + 1]):
            return coeffs[3 * i] * x ** 2 + coeffs[3 * i + 1] * x + coeffs[3 * i + 2]


class QSF(object):  # QSF - Quadratic spline function
    def __init__(self, args: list, vals: list, cond: float = 0.0):
        self.__args = args
        self.__coeffs = quadratic_spline_coeffs(args, vals, cond)

    def __call__(self, x):
        """При помощи метода можно обращаться к объекту класса, как к функции"""
        if isinstance(x, float) or isinstance(x, int):
            return quadratic_spline(x, self.__args, self.__coeffs)
        else:  # Можно возвращать список значений
            return [quadratic_spline(_, self.__args, self.__coeffs) for _ in x]
