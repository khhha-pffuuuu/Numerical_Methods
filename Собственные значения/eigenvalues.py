import package.helpers as hp
import package.linker as mtd
from СЛАУ.package.matrix import Matrix


def main():
    print('∘ТЕМА: Поиск собственных чисел матрицы')
    print('Введите размерность матрицы:', end=' ')
    n = int(input())

    A, real_eig_vals = hp.generate_random_matrix(n)

    print(f'\nСлучайно сгенерированная матрица:\n{A}\n')
    print(f'Ее собственные числа:\n{real_eig_vals}')

    print("\n\n∘Степенной метод")  # Находит пару с максимальным по модулю собственным числом
    eig_pair_PM = mtd.PM_algorithm(A)
    print(f'Собственная пара: ({eig_pair_PM[0]}, [{~eig_pair_PM[1]}])')
    print(f'Погрешность метода: {abs(real_eig_vals[-1] - eig_pair_PM[0])}')

    print("\n\n∘QR-алгоритм")  # Алгоритм находит все собственные числа
    eig_vals_QR = sorted(mtd.QR_algorithm(A))
    print(f'Собственные числа:\n{eig_vals_QR}')
    print(f'Погрешность метода: {abs(Matrix([real_eig_vals]) - Matrix([eig_vals_QR]))}')

    print("\n\n∘Обратный степенной метод")  # Уточняем собственные числа из QR алгоритма + находим собственные вектора
    eig_vals_IPM = []
    for eig_val in eig_vals_QR:
        eig_pair_IPM = mtd.IPM_algorithm(A, eig_val)
        print(f'Собственная пара: ({eig_pair_IPM[0]}, [{~eig_pair_IPM[1]}])')

        eig_vals_IPM.append(eig_pair_IPM[0])
    print(f'Погрешность метода: {abs(Matrix([real_eig_vals]) - Matrix([eig_vals_IPM]))}')


if __name__ == '__main__':
    main()
