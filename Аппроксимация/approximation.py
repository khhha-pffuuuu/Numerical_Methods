import package.helpers as hp
import package.linker as mtd

import matplotlib.pyplot as plt
from prettytable import PrettyTable

def main():
    a, b = -1, 1  # Границы промежутка
    m, k = 100, 5  # m - кол-во различных значений точек на заданном промежутке, k - кол-во "повторений эксперимента"
    args = hp.uniform_points(a, b, m, k)
    real_vals = hp.func(args)  # Реальные значения функции в заданных точках
    vals = hp.values_generator(args)  # Значения функции с погрешностью(не более 0.1)

    # Цвета точек, зависящее от расстояния точек от кривой(чем ближе, тем они более серые, чем дальше - тем краснее)
    # Воспользуемся этим немного ниже
    hex_ = '606e6c'
    r_ = int(hex_[0: 2], 16)
    col_ = [f'#{hex(r_ + round((200 - r_) * abs(real_vals[i] - vals[i]) * 10))[2:]}{hex_[2:]}' for i in range(k * m)]

    # Таблица для задания
    table = PrettyTable()
    table.field_names = [
        'Степень полинома', 'Loss для МНК с нормальными уравнениями', 'Loss для МНК с ортогональными многочленами'
    ]
    for n in range(1, 6):
        # Задаем функции, полученные соответственно при помощи МНК с нормальными уравнениями и ортогональными
        # многочленами
        normal = mtd.OLS_NE(args, vals, n)
        orthogonal = mtd.OLS_OP(args, vals, n)

        # Считаем функцию потерь
        ne_loss = hp.Loss(normal(args), vals)
        op_loss = hp.Loss(orthogonal(args), vals)
        table.add_row([n, ne_loss, op_loss])

        # Строим графики
        plt.figure(figsize=(12, 6))
        points = hp.uniform_points(-1, 1, 200)
        real_points = hp.func(points)
        normal_points = normal(points)

        plt.title(f'Метод наименьших квадратов при n={n}')
        plt.scatter(args, vals, s=5, c=col_)
        plt.plot(points, real_points, color='#606E6C', linestyle='dashdot')
        plt.plot(points, normal_points, color='#F47F17')
        plt.grid()

    plt.show()
    print(table)


if __name__ == '__main__':
    main()
