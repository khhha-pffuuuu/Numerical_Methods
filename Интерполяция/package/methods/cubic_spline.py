from СЛАУ.package.matrix import Matrix
from СЛАУ.package.methods.LUP import LUP


def cubic_spline_coeffs(args: list, vals: list, cond: tuple) -> Matrix:
    """Функция поиска коэффициентов кубического сплайна"""
    n = len(args)
    args_incs = [args[i + 1] - args[i] for i in range(n - 1)]  # Прирост соседних аргументов
    vals_incs = [vals[i + 1] - vals[i] for i in range(n - 1)]  # Прирост соседних значений

    # Используем метод прогонки
    H = Matrix.zeros(n - 2)
    gamma = Matrix.zeros(n - 2, 1)
    for i in range(n - 2):
        H[i, i] = 2 * (args_incs[i + 1] + args_incs[i])
        if i > 0:
            H[i, i - 1] = args_incs[i]
            H[i - 1, i] = args_incs[i]

        gamma[i] = 6 * (vals_incs[i + 1] / args_incs[i + 1] - vals_incs[i] / args_incs[i])

    solve = LUP(H, gamma)
    vals__ = [cond[0]] + [solve[i] for i in range(n - 2)] + [cond[1]]  # Вторые производные

    vals_ = []  # Первые производные
    for i in range(n - 1):
        vals_.append(vals_incs[i] / args_incs[i] - vals__[i + 1] * args_incs[i] / 6 - vals__[i] * args_incs[i] / 3)

    coeffs = Matrix.zeros(4 * (n - 1), 1)
    for i in range(n - 1):
        coeffs[4 * i] = vals[i]
        coeffs[4 * i + 1] = vals_[i]
        coeffs[4 * i + 2] = vals__[i] / 2
        coeffs[4 * i + 3] = (vals__[i + 1] - vals__[i]) / (6 * args_incs[i])

    return coeffs


def cubic_spline(x: float, args: list, coeffs: Matrix) -> float:
    """Функция кубического сплайна"""
    n = len(args)

    for i in range(n - 1):
        if min(args[i], args[i + 1]) <= x <= max(args[i], args[i + 1]):
            return coeffs[4 * i] + coeffs[4 * i + 1] * (x - args[i]) + \
                   coeffs[4 * i + 2] * (x - args[i]) ** 2 + coeffs[4 * i + 3] * (x - args[i]) ** 3


class CSF(object):  # LSF - Cubic spline function
    def __init__(self, args: list, vals: list, cond: tuple = (0, 0)):
        self.__args = args
        self.__coeffs = cubic_spline_coeffs(args, vals, cond)

    def __call__(self, x):
        """При помощи метода можно обращаться к объекту класса, как к функции"""
        if isinstance(x, float) or isinstance(x, int):
            return cubic_spline(x, self.__args, self.__coeffs)
        else:  # Можно возвращать список значений
            return [cubic_spline(_, self.__args, self.__coeffs) for _ in x]
