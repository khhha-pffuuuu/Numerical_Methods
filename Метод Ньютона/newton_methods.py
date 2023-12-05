from package.matrix import Matrix

from package.tests.function import function as func, function_derivative as func_der
from package.tests.system import Function as Func, Function_derivative as Func_der

import package.adjuster as mtd


def main():
    root = mtd.root_search(func, func_der, -1, 1)  # Поиск корня функции на заданном промежутке
    print(f'Решение нелинейного уравнения:\n{root}', end='\n\n')
    sys_root = mtd.sys_root_search(Func, Func_der)  # Поиск решения системы уравнений около заданной точки
    print(f'Решение системы уравнений:\n{sys_root}', end='\n\n')


if __name__ == '__main__':
    main()
