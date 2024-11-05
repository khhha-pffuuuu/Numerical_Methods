from package.linker import *
import package.helpers as hp

from scipy.integrate import quad as exact_quad

from tqdm import trange


def main():  # Первая часть задания
    a, b = 1, 3  # Пределы интегрирования
    alpha, beta = 0, 1 / 6

    # Создаем список методов
    methods = ['Left Rectangle', 'Right Rectangle', 'Middle Rectangle', 'Trapezia', 'Simpson', 'Gauss', 'Newton Cotes']

    print('∘ЗАДАНИЕ 1: Вычисление интегралов при помощи составных квадратурных формул.')
    real_value, *_ = exact_quad(hp.func, a, b)
    real_value_weight, *_ = exact_quad(lambda x: hp.func(x) / (x - a) ** alpha / (b - x) ** beta, a, b)

    methods_residues = {mtd: [] for mtd in methods}  # Список погрешностей методов
    table = hp.Table(methods)  # Таблица лучших значений методов

    for n_part in trange(1, 101, desc='Вычисление'):  # Будем увеличивать разбиение и смотреть на поведение погрешности
        for method in methods:
            calc_value = quad(hp.func, a, b, method=method, alpha=alpha, beta=beta, num_partitions=n_part)
            residue = abs(real_value_weight - calc_value) if method in ['Gauss', 'Newton Cotes'] \
                else abs(real_value - calc_value)

            table.update_column(column=method, values=(n_part, calc_value, residue))
            methods_residues[method].append(residue)

    # Таблица погрешностей методов
    table.show(highlight_best=True)

    # Строим графики погрешностей
    hp.plot_residues_graphics(methods_residues)

    print('\n∘ЗАДАНИЕ 2: Методы оценки составных квадратурных формул.')
    # Погрешность для метода Ньютона-Котса
    nc_quad = lambda n: quad(hp.func, a, b, alpha=alpha, beta=beta, method='Newton Cotes', num_partitions=n)
    nc_residue, nc_step, nc_partition = richardson(nc_quad, gap_len=b - a, min_part=3, eps=10 ** -6)

    print(hp.red_string('Метод Ньютона-Котса'))
    print(f'Длина шага разбиения: {hp.green_string(nc_step)}')
    print(f'Разбиение: {hp.green_string(nc_partition)} точек')
    print(f'Погрешность: {hp.green_string(nc_residue)}\n')

    # Погрешность для метода Гаусса
    gs_quad = lambda n: quad(hp.func, a, b, alpha=alpha, beta=beta, method='Gauss', num_partitions=n)
    gs_residue, gs_step, gs_partition = richardson(gs_quad, gap_len=b - a, min_part=3, eps=10 ** -6)

    print(hp.red_string('Метод Гаусса'))
    print(f'Длина шага разбиения: {hp.green_string(gs_step)}')
    print(f'Разбиение: {hp.green_string(gs_partition)} точек')
    print(f'Погрешность: {hp.green_string(gs_residue)}\n')


if __name__ == '__main__':
    main()
