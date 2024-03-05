def Newton_coefficients(args: list, vals: list, n: int) -> float:
    """Функция вычисляет n-ый коэффициент интерполяционного полинома Ньютона(при n>=2)"""
    coeff = 0

    # Для вычисления коэффициентов используем не классическую рекуррентную формулу с показательной
    # асимптотикой, а более быструю - с квадратичной
    for i in range(n):
        elem = vals[i]
        for j in range(n):  # Делим значение yi на все (xi - xj), где i - фиксированно и i!=j
            if j != i:
                elem /= args[i] - args[j]
        coeff += elem

    return coeff


def Newton_polynomial(x: float, args: list, coeffs: list) -> float:
    """Находим интерполяционный полином Ньютона"""
    n = len(args)
    result = 0

    for i in range(n):
        elem = coeffs[i]
        for j in range(i):
            elem *= x - args[j]
        result += elem

    return result


class NIP(object):  # NIP - Newton's interpolation polynomial
    def __init__(self, args: list, vals: list):
        self.__args = args

        self.__coeffs = [vals[0]]
        for i in range(2, len(args) + 1):  # Заполняем список коэффициентов
            self.__coeffs.append(Newton_coefficients(args[:i], vals[:i], i))

    def __call__(self, x):
        """При помощи метода можно обращаться к объекту класса, как к функции"""
        if isinstance(x, float) or isinstance(x, int):
            return Newton_polynomial(x, self.__args, self.__coeffs)
        else:  # Можно возвращать список значений
            return [Newton_polynomial(_, self.__args, self.__coeffs) for _ in x]
