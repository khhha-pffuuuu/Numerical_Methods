import package.helpers as hp
import package.adjuster as mtd

import matplotlib.pyplot as plt
from prettytable import PrettyTable


def main():
    print('∘ЗАДАНИЕ 1: Интерполяционные полиномы Лагранжа и Ньютона\n\n')
    a, b = -10, 10    # Концы промежутка, на котором будем рассматривать функцию
    nums = [4, 9, 19]

    plt.figure(figsize=(12, 6))
    for i in range(len(nums)):
        n = nums[i]  # Количество узлов: n + 1
        print(f'Количество узлов интерполирования n = {n + 1}:')

        # Равномерное приращение
        args = hp.uniform_points(a, b, n)
        vals = hp.func(args)

        L = mtd.LIP(args, vals)  # Полином Лагранжа при равномерном разбиении
        N = mtd.NIP(args, vals)  # Интерполяционный полином Ньютона при равномерном разбиении

        # "Оптимальное" приращение
        args_opt = hp.optimal_points(a, b, n)
        vals_opt = hp.func(args_opt)

        L_opt = mtd.LIP(args_opt, vals_opt)  # Полином Лагранжа при оптимальном разбиении
        N_opt = mtd.NIP(args_opt, vals_opt)  # Интерполяционный полином Ньютона при оптимальном разбиении

        # Строим табличку отклонений функций
        table = PrettyTable()
        table.field_names = [
            'Кол-во проверочных точек', 'ИП Лагранжа(равномерный)', 'ИП Лагранжа(оптимальный)',
            'ИП Ньютона(равномерный)', 'ИП Ньютона(оптимальный)'
        ]

        for m in [n * 3, n * 6, n * 9]:  # Кол-во проверочных точек: m + 1
            # Отклонения двух ИП Лагранжа
            L_devs = hp.deviations(hp.func, L, a, b, m)
            L_opt_devs = hp.deviations(hp.func, L_opt, a, b, m)

            # Отклонения двух ИП Ньютона
            N_devs = hp.deviations(hp.func, N, a, b, m)
            N_opt_devs = hp.deviations(hp.func, N_opt, a, b, m)

            table.add_row([m, max(L_devs), max(L_opt_devs), max(N_devs), max(N_opt_devs)])

        print(table, end='\n\n')

    #########################################################
    # Строим графики функций интерполяционных полиномов #####
    #########################################################

        k = 200  # Разбиение функции на m точек
        points = hp.uniform_points(b, a, k)  # Будем строить график по 200-м точкам
        func_vals = hp.func(points)  # Значения действительной функции в точках points
        L_vals, L_opt_vals = L(points), L_opt(points)  # Значения ИП Лагранжа в точках points
        N_vals, N_opt_vals = N(points), N_opt(points)  # Значения ИП Ньютона в точках points

        plt.subplot(231 + i)
        plt.grid(True)
        plt.plot(points, L_vals, label='Равномерно')
        plt.plot(points, L_opt_vals, label='"Оптимально"')
        plt.plot(points, func_vals, color='black', label='Действительно')
        min_val = min(min(L_vals), min(L_opt_vals))
        plt.text(0.4 * b, 0.8 * min_val, f'Узлов: {n + 1}', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 8})
        plt.legend()

        plt.subplot(234 + i)
        plt.grid(True)
        plt.plot(points, N_vals, label='Равномерно')
        plt.plot(points, N_opt_vals, label='"Оптимально"')
        plt.plot(points, func_vals, color='black', label='Действительно')
        min_val = min(min(N_vals), min(N_opt_vals))
        plt.text(0.4 * b, 0.8 * min_val, f'Узлов: {n + 1}', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 8})
        plt.legend()

    plt.suptitle('Графики для первого задания', fontsize=16, fontweight='bold')
    plt.subplot(232)
    plt.title('Интерполяционный полином Лагранжа')
    plt.subplot(235)
    plt.title('Интерполяционный полином Ньютона')

    print('\n∘ЗАДАНИЕ 2: Сплайны\n\n')
    for i in range(len(nums)):
        n = nums[i]  # Количество узлов: n + 1
        print(f'Количество узлов интерполирования n = {n + 1}:')

        # Равномерное приращение
        args = hp.uniform_points(a, b, n)
        vals = hp.func(args)

        lin = mtd.LSF(args, vals)  # Линейный сплайн при равномерном разбиении
        quad = mtd.QSF(args, vals, 6.5)  # Квадратичный сплайн при равномерном разбиении
        cube = mtd.CSF(args, vals)  # Кубический сплайн при равномерном разбиении

        # "Оптимальное" приращение
        args_opt = hp.optimal_points(a, b, n)
        vals_opt = hp.func(args_opt)

        lin_opt = mtd.LSF(args_opt, vals_opt)  # Линейный сплайн при "оптимальном" разбиении
        quad_opt = mtd.QSF(args_opt, vals_opt, 7.5)  # Квадратичный сплайн при "оптимальном" разбиении
        cube_opt = mtd.CSF(args_opt, vals_opt)  # Кубический сплайн при "оптимальном" разбиении

        # Строим табличку отклонений функций
        table = PrettyTable()
        table.field_names = [
            'Кол-во проверочных точек', 'Линейный сплайн(равномерный)', 'Линейный сплайн(оптимальный)',
            'Квадратический сплайн(равномерный)', 'Квадратический сплайн(оптимальный)',
            'Кубический сплайн(равномерный)', 'Кубический сплайн(оптимальный)'
        ]

        for m in [n * 3, n * 6, n * 9]:  # Кол-во проверочных точек: m + 1
            # Отклонения сплайнов при равномерном разбиении
            lin_devs = hp.deviations(hp.func, lin, a, b, m)
            quad_devs = hp.deviations(hp.func, quad, a, b, m)
            cube_devs = hp.deviations(hp.func, cube, a, b, m)

            # Отклонения сплайнов при оптимальном разбиении
            lin_opt_devs = hp.deviations(hp.func, lin_opt, a, b, m)
            quad_opt_devs = hp.deviations(hp.func, quad_opt, a, b, m)
            cube_opt_devs = hp.deviations(hp.func, cube_opt, a, b, m)

            table.add_row([m, max(lin_devs), max(lin_opt_devs),
                           max(quad_devs), max(quad_opt_devs),
                           max(cube_devs), max(cube_opt_devs)])

        print(table, end='\n\n')

    #########################################################
    # Строим графики распределения абсолютной погрешности ###
    #########################################################

    plt.figure(figsize=(12, 6))
    for i in range(len(nums)):
        n = nums[i]  # Количество узлов: n + 1

        # Будем через графики сравнивать отклонения ИП Ньютона и кубического сплайна
        # Графики построим так: каждому x сопоставляем абсолютное отклонение высчитанной функции от действительной

        args = hp.uniform_points(a, b, n)
        vals = hp.func(args)
        N, cube = mtd.NIP(args, vals), mtd.CSF(args, vals)

        args_opt = hp.optimal_points(a, b, n)
        vals_opt = hp.func(args_opt)
        N_opt, cube_opt = mtd.NIP(args_opt, vals_opt), mtd.CSF(args_opt, vals_opt)

        k = 200  # Разбиение функции на k + 1 точек

        points = hp.uniform_points(a, b, k)
        # Списки отклонений соответственно ИП Ньютона и кубического сплайна при равномерном распределении
        N_devs = hp.deviations(hp.func, N, a, b, k)
        cube_devs = hp.deviations(hp.func, cube, a, b, k)
        # Списки отклонений соответственно ИП Ньютона и кубического сплайна при оптимальном распределении
        N_opt_devs = hp.deviations(hp.func, N_opt, a, b, k)
        cube_opt_devs = hp.deviations(hp.func, cube_opt, a, b, k)

        plt.subplot(321 + i * 2)
        plt.grid(True)
        plt.plot(points, N_devs, label='Отклонение ИП Ньютона')
        plt.plot(points, cube_devs, label='Отклонение $S_{3,2}$')
        plt.legend()

        plt.subplot(322 + i * 2)
        plt.grid(True)
        plt.plot(points, N_opt_devs)
        plt.plot(points, cube_opt_devs)
        max_dev = max(max(N_opt_devs), max(cube_opt_devs))  # Верхняя граница 'оптимальных' функций
        plt.text((a - b) / 20, 0.8 * max_dev, f'Узлов: {n + 1}',
                 bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 8})

    plt.suptitle('Графики для второго задания', fontsize=16, fontweight='bold')
    plt.subplot(321)
    plt.title('Равномерное разбиение')
    plt.subplot(322)
    plt.title('Оптимальное разбиение')

    plt.show()


if __name__ == '__main__':
    main()
