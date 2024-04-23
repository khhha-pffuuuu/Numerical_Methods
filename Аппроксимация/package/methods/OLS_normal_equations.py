from СЛАУ.package.matrix import Matrix
from СЛАУ.package.methods.LUP import LUP


def coeffs_calculation(args: list[float], vals: list[float], n: int) -> Matrix:
    """Функция поиска коэффициентов для МНК с нормальными уравнениями"""
    V = Matrix([[x ** j for j in range(n + 1)] for x in args])  # Матрица Вандермонда
    f = ~Matrix([vals])

    # Матрица Вандермонда V имеет как минимум n + 1 различных значений x, поэтому ~V * V является квадратной и
    # невырожденной матрицей
    A, b = ~V * V, ~V * f
    coeffs = LUP(A, b)

    return coeffs


class OLS(object):
    def __init__(self, args: list[float], vals: list[float], n: int):
        self.coeffs = coeffs_calculation(args, vals, n)
        self.poly_n = n

    def __call__(self, x: float or list) -> float or list:
        """Обращаемся к объекту как к функции"""
        if isinstance(x, int) or isinstance(x, float):
            return sum([self.coeffs[i] * x ** i for i in range(self.poly_n + 1)])
        else:  # Можно возвращать список значений
            return [sum([self.coeffs[i] * x_ ** i for i in range(self.poly_n + 1)]) for x_ in x]
