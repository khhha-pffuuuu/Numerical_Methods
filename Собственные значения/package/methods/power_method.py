from СЛАУ.package.matrix import Matrix


def PM_algorithm(A: Matrix) -> (float, Matrix):
    """Степенной метод"""
    delta, rtol = 10 ** -8, 10 ** -10
    n = A.dim[0]

    y = Matrix([[1] for _ in range(n)])  # Начальное приближение
    z = y / abs(y)

    lamda_vec = Matrix.zeros(n, 1)  # Вектор, усреднение ненулевых координат которого равно максимальному собственному
    # числу (по модулю)

    while True:
        y = A * z

        lamda_vec_ = Matrix.zeros(n, 1)
        suited_amount = 0  # Количество нужных нам координат
        for i in range(n):
            if z[i] >= delta:  # Если z[i] меньше заданного delta, то мы считаем его вычислительным нулем
                lamda_vec_[i] = y[i] / z[i]
                suited_amount += 1

        z = y / abs(y)

        if (lamda_vec_ - lamda_vec).norm('inf') <= rtol * max(lamda_vec_.norm('inf'), lamda_vec.norm('inf')):
            # Пользуемся относительной точностью, так как считаем, что максимальное по модулю собственное число
            # достаточно далеко от нуля
            eig_val = sum([lamda_vec_[i] for i in range(n)]) / suited_amount

            return eig_val, z  # Вектор z стремится к собственному вектору соответствующего с.ч. eig_val

        lamda_vec = lamda_vec_.copy
