from math import sqrt

from СЛАУ.package.matrix import Matrix
from ..helpers import HQR, Hessenberg


def QR_algorithm(A: Matrix) -> list:
    """QR-алгоритм со сдвигом и понижением размерности"""
    eps = 10 ** -8
    n = A.dim[0]
    E = Matrix.E(n)

    H = Hessenberg(A)  # Приводим к Хессенберговой форме, так как для такой матрицы разложение в QR работает за
    # квадратичное время

    eig_vals = []  # Список собственных значений
    while True:
        corner = H[-1, -1]
        Q, R = HQR(H - corner * E)  # При помощи сдвига ускоряем стремление поддиагонального элемента к нулю
        H = R * Q + corner * E

        if abs(H[n - 1, n - 2]) < eps:
            if n > 2:  # Если поддиагональный элемент меньше заданного eps, то уменьшаем размер матрицы
                eig_vals.append(H[n - 1, n - 1])
                H = H[n - 1: n - 1]
                n -= 1
            else:  # Если размерность матрицы равна двум, то возвращаем диагональные элементы
                eig_vals.append(H[0, 0])
                eig_vals.append(H[1, 1])

                return eig_vals
