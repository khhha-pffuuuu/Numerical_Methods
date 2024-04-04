import random
from math import sqrt

from СЛАУ.package.matrix import Matrix


def generate_random_matrix(n: int) -> tuple:
    """Функция генерирует n случайных вещественных чисел, которые будут являться собственными значениями
    случайно сгенерированной матрицы"""
    e_vals = [random.random() * 10 for _ in range(n)]

    L = Matrix.diag(e_vals)  # Диагональная матрица собственных значений
    C = Matrix([[random.random() for _ in range(n)] for _ in range(n)])  # Произвольная квадратная матрица

    while C.det >= 0:  # В случае, если определитель C равен нулю, то генерируем матрицу снова
        C = Matrix([[random.random() for _ in range(n)] for _ in range(n)])

    A = C ** -1 * L * C

    return A, sorted(e_vals)


def Hessenberg(A: Matrix) -> Matrix:
    """Метод приведения матрицы к Хессенберговой форме методом отражений"""
    n = A.dim[0]
    E = Matrix.E(n)
    A_Hess = A.copy

    # Зануляем ненужные нам элементы методом отражений
    for i in range(n - 2):
        v = A_Hess[None, i]
        for j in range(i + 1):
            v[j] = 0
        v[i + 1] = v[i + 1] - abs(v)
        v = v / abs(v)

        H = E - 2 * v * ~v
        A_Hess = H * A_Hess * H  # Домножение слева и справа на H не только сохраняет Хесенбергову форму, но
        # и сохраняет собственные числа A

    return A_Hess


def HQR(A: Matrix) -> (Matrix, Matrix):
    """Метод разложения Хессенберговой матрицы на треугольную и ортонормированную."""
    n = A.dim[0]
    E = Matrix.E(n)

    R = A.copy
    Q = E.copy

    # Строим матрицу методом вращений Гивенса
    for i in range(n - 1):
        c = abs(R[i, i]) / sqrt(R[i, i] ** 2 + R[i + 1, i] ** 2)
        s = -c * R[i + 1, i] / R[i, i]

        # Вместо обычного умножения за кубическое время, в методе вращений можно его производить за квадратичное время
        for j in range(n):
            R[i, j], R[i + 1, j] = R[i, j] * c - R[i + 1, j] * s, R[i, j] * s + R[i + 1, j] * c
            Q[j, i], Q[j, i + 1] = Q[j, i] * c - Q[j, i + 1] * s, Q[j, i] * s + Q[j, i + 1] * c

    return Q, R
