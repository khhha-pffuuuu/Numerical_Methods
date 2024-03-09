import task_functions as tf

from math import sqrt, atan, cos
from prettytable import PrettyTable


def main():
    print('∘ТЕМА: Теория Погрешностей\n')
    table = PrettyTable()
    table.field_names = [
        'Значение аргумента x', 'Погрешность квадратного корня', 'Погрешность арктангенса',
        'Погрешность косинуса', 'Погрешность функции z'
    ]

    x = 0.01
    while x <= 0.06:  # Смотрим погрешности в промежутке [0.01, 0.06] с шагом 0.005
        x = round(x, 3)  # Отбрасываем случайно появившуюся дробную часть
        z = sqrt(2 * x + 0.4) * atan(cos(3 * x + 1))
        z_ = tf.sqrt(2 * x + 0.4) * tf.arctan(tf.cos(3 * x + 1))

        table.add_row([x, abs(tf.sqrt(x) - sqrt(x)), abs(tf.arctan(x) - atan(x)), abs(tf.cos(x) - cos(x)), abs(z_ - z)])

        x += 0.005

    print(table)


if __name__ == '__main__':
    main()
