def basis_polynomial(x: float, args: list, k: int) -> int:
    """Функция вычисляет k-ый базис полинома Лагранжа"""
    n = len(args)
    basis = 1

    for i in [i for i in range(n) if i != k]:
        basis *= (x - args[i]) / (args[k] - args[i])

    return basis


def Lagrange_polynomial(x: float, args: list, vals: list) -> float:
    """При помощи предыдущей функции вычисляем полином"""
    n = len(args)

    result = 0
    for i in range(n):
        result += basis_polynomial(x, args, i) * vals[i]

    return result


class LIP(object):  # LIP - Lagrange interpolation polynomial
    def __init__(self, args: list, vals: list):
        self.__args = args
        self.__vals = vals

    def __call__(self, x):
        """При помощи метода можно обращаться к объекту класса, как к функции"""
        if isinstance(x, float) or isinstance(x, int):
            return Lagrange_polynomial(x, self.__args, self.__vals)
        else:  # Можно возвращать список значений
            return [Lagrange_polynomial(_, self.__args, self.__vals) for _ in x]
