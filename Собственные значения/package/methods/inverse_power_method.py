from СЛАУ.package.matrix import Matrix
from СЛАУ.package.methods.LUP import LUP


def IPM_algorithm(A: Matrix, shift: float = 0) -> (float, Matrix):
    """Обратный степенной метод со сдвигами"""
    delta, eps = 10 ** -8, 10 ** -10
    n = A.dim[0]
    E = Matrix.E(n)

    y = Matrix([[1] for _ in range(n)])
    z = y / abs(y)

    sigma = shift  # Значение sigma будет стремиться к собственному числу
    while True:
        y = LUP(A - sigma * E, z)

        mu_list = []  # Вектор, усреднение координат которого ≈ минимальному собственному числу A - sigma * E
        for i in range(n):
            if y[i] >= delta:  # Если y[i] меньше заданного delta, то мы считаем его вычислительным нулем
                mu_list.append(z[i] / y[i])

        z = y / abs(y)

        if len(mu_list) != 0:
            sigma_ = sigma + sum(mu_list) / len(mu_list)

            if abs(sigma_ - sigma) <= eps:  # Проверяем малость приращения
                return sigma_, z  # Вектор z стремится к собственному вектору соответствующего с.ч. sigma

            sigma = sigma_
