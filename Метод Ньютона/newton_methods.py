from package.tests.function import function as func, function_derivative as func_der
from package.tests.system import Function as Func, Function_derivative as Func_der

import package.adjuster as mtd


def main():
    print('∘ТЕМА: Метод Ньютона\n')

    start_segment = -1, 1
    root = mtd.root_search(func, func_der, start_segment)  # Поиск корня функции на заданном промежутке
    print(f'Решение нелинейного уравнения:\n {root}')
    print(f'Погрешность решения:\n {func(root)}', end='\n\n')

    sys_root = mtd.sys_root_search(Func, Func_der)  # Поиск решения системы уравнений
    print(f'Решение системы уравнений:\n{~sys_root}', end='\n')
    print(f'Погрешность решения: \n{abs(Func(sys_root[0], sys_root[1]))}')


if __name__ == '__main__':
    main()
