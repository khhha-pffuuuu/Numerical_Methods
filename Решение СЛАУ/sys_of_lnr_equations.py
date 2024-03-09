import package.adjuster as mtd
import package.helpers as hp
from package.matrix import Matrix


def main():
    print('∘ТЕМА: Решение систем линейных алгебраических уравнений\n')

    # Тесты от нулевого до четвертого
    for i in range(5):
        print(f'ТЕСТ {i}')
        m_A = hp.file_adapting(open(f'package/tests/test{i}-A.txt', 'r+'))
        m_b = hp.file_adapting(open(f'package/tests/test{i}-b.txt', 'r+'))
        A, b = Matrix(m_A), Matrix(m_b)

        x = Matrix(hp.exact_solution(m_A, m_b))
        print(f'Точное решение:\n{x}\n')

        x_LUP = mtd.LUP(A, b)
        inc_LUP = abs(x - x_LUP)
        print(f'Метод LU-разложения:\n{x_LUP}\n'
              f'Погрешность решения: {inc_LUP}\n')

        x_QR = mtd.QR(A, b)
        inc_QR = abs(x - x_QR)
        print(f'Метод QR-разложения:\n{x_QR}\n'
              f'Погрешность решения: {inc_QR}\n')

        print(f'Метод простой итерации:')
        for degree in range(2, 5):  # Несколько тестов с разными точностями
            x_FPIM, iter_count = mtd.FPIM(A, b, 10 ** -degree)
            inc_FPIM = abs(x - x_FPIM)
            print(f'Точность 10^-{degree}:\n{x_FPIM}\n'
                  f'Погрешность решения: {inc_FPIM}\n'
                  f'Количество итераций: {iter_count}\n')

        if hp.is_dd(A):  # Только для матриц с диагональным преобладанием
            print(f'Метод Якоби:')
            for degree in range(2, 5):  # Несколько тестов с разными точностями
                x_Jacobi, iter_count = mtd.Jacobi(A, b, 10 ** -degree)
                inc_Jacobi = abs(x - x_Jacobi)
                print(f'Точность 10^-{degree}:\n{x_Jacobi}\n'
                      f'Погрешность решения: {inc_Jacobi}\n'
                      f'Количество итераций: {iter_count}\n')

        print(f'Метод Гаусса-Зейделя:')
        for degree in range(2, 5):
            x_GS, iter_count = mtd.Gauss_Seidel(A, b, 10 ** -degree)
            inc_GS = abs(x - x_GS)
            print(f'Точность 10^-{degree}:\n{x_GS}\n'
                  f'Погрешность решения: {inc_GS}\n'
                  f'Количество итераций: {iter_count}\n')

    # Пятый тест
    print('ТЕСТ 5:')
    for n in range(4, 8):  # Размерность от 4 до 7
        for eps in [-3, -6]:  # В задании A = A1 + n * eps * A2
            print(f'Размерность матрицы = {n}; ε = 10^{eps}')

            m_A, m_b = hp.fifth_task_helper(n, 10 ** eps)
            A, b = Matrix(m_A), Matrix(m_b)

            x = Matrix(hp.exact_solution(m_A, m_b))
            print(f'Точное решение:\n{x}\n')

            x_LUP = mtd.LUP(A, b)
            inc_LUP = abs(x - x_LUP)
            print(f'Метод LU-разложения:\n{x_LUP}\n'
                  f'Погрешность решения: {inc_LUP}\n')

            x_QR = mtd.QR(A, b)
            inc_QR = abs(x - x_QR)
            print(f'Метод QR-разложения:\n{x_QR}\n'
                  f'Погрешность решения: {inc_QR}\n')

            print(f'Метод простой итерации:')
            for degree in range(2, 5):  # Несколько тестов с разными точностями
                x_FPIM, iter_count = mtd.FPIM(A, b, 10 ** -degree)
                inc_FPIM = abs(x - x_FPIM)
                print(f'Точность 10^-{degree}:\n{x_FPIM}\n'
                      f'Погрешность решения: {inc_FPIM}\n'
                      f'Количество итераций: {iter_count}\n')

            if hp.is_dd(A):
                print(f'Метод Якоби:')
                for degree in range(2, 5):  # Несколько тестов с разными точностями
                    x_Jacobi, iter_count = mtd.Jacobi(A, b, 10 ** -degree)
                    inc_Jacobi = abs(x - x_Jacobi)
                    print(f'Точность 10^-{degree}:\n{x_Jacobi}\n'
                          f'Погрешность решения: {inc_Jacobi}\n'
                          f'Количество итераций: {iter_count}\n')

            print(f'Метод Гаусса-Зейделя:')
            for degree in range(2, 5):
                x_GS, iter_count = mtd.Gauss_Seidel(A, b, 10 ** -degree)
                inc_GS = abs(x - x_GS)
                print(f'Точность 10^-{degree}:\n{x_GS}\n'
                      f'Погрешность решения: {inc_GS}\n'
                      f'Количество итераций: {iter_count}\n')


if __name__ == '__main__':
    main()
