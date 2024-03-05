from ..matrix import Matrix
from ..helpers import LUP


def linear_spline_coeffs(args: list, vals: list) -> Matrix:
    """Функция поиска коэффициентов линейного сплайна"""
    n = len(args)

    # Представляем каждое уравнение сплайна в виде СЛАУ. Её решением будут коэффициенты уравнений системы.
    X = Matrix.E(2)
    y = Matrix.zeros(2, 1)

    coeffs = Matrix.zeros(2 * (n - 1), 1)

    for i in range(n - 1):
        # Поочередно находим коэффициенты уравнений при
        X[0, 0], X[1, 0], X[0, 1] = args[i], args[i + 1], 1
        y[0], y[1] = vals[i], vals[i + 1]

        solve = LUP(X, y)
        coeffs[2 * i], coeffs[2 * i + 1] = solve[0], solve[1]

    return coeffs  # Возвращаем вектор коэффициентов


def linear_spline(x: float, args: list, coeffs: Matrix) -> int:
    """Функция линейного сплайна"""
    n = len(args)

    for i in range(n - 1):
        # По построению, промежутку [args[i], args[i + 1]] будут соответствовать коэффициенты
        # coeffs[2 * i](коэффициент при x) и coeffs[2 * i + 1](свободный член) линейного уравнения
        if min(args[i], args[i + 1]) <= x <= max(args[i], args[i + 1]):
            return coeffs[2 * i] * x + coeffs[2 * i + 1]


class LSF(object):  # LSF - Linear spline function
    def __init__(self, args: list, vals: list):
        self.__args = args
        self.__coeffs = linear_spline_coeffs(args, vals)

    def __call__(self, x):
        """При помощи метода можно обращаться к объекту класса, как к функции"""
        if isinstance(x, float) or isinstance(x, int):
            return linear_spline(x, self.__args, self.__coeffs)
        else:  # Можно возвращать список значений
            return [linear_spline(_, self.__args, self.__coeffs) for _ in x]
