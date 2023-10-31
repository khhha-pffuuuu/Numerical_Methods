from numpy import array
from scipy.linalg import solve


def sqrt(x):
    """Квадратный корень по формуле Герона"""
    if x == 0:
        return 0

    eps = 10 ** -10
    res = x / 2

    while True:
        res_ = 1 / 2 * (res + x / res)
        if abs(res - res_) < eps:
            return res_
        res = res_


def file_adapting(file):
    """Файл -> list"""
    matrix = []

    for string in file:
        matrix.append([float(elem) for elem in string.strip('\n').split(' ')])

    return matrix


def exact_solution(m_A, m_b):
    """Функция, стилизующая вывод матрицы из numpy"""
    x = solve(array(m_A), array(m_b))
    matrix = []

    for i in range(len(x)):
        matrix.append([elem for elem in x[i]])

    return matrix


def fifth_task_helper(n, eps):
    """Функция возвращает две плохо обусловленные матрицы (нужно для 5-ого задания)"""
    m_A, m_b = [], []

    for i in range(n):
        b_elem = -1 if i != n - 1 else 1
        m_b.append([b_elem])

        row = []
        for j in range(n):
            if i > j:
                elem_A = 4 * eps
            elif i == j:
                elem_A = 1 + 4 * eps
            else:
                elem_A = -1 - 4 * eps
            row.append(elem_A)
        m_A.append(row)

    return m_A, m_b
