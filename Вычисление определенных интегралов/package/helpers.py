from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

from colorama import Fore, Style



def red_string(var):
    """Возвращает красный текст"""
    return Fore.RED + str(var) + Style.RESET_ALL


def green_string(var):
    """Возвращает зеленый текст"""
    return Fore.GREEN + str(var) + Style.RESET_ALL


class Table:
    """Класс таблицы, созданный для удобного им пользования в пределах задачи и для красивого вывода"""
    def __init__(self, columns):
        self.__column_names = columns
        self.__rows = [[np.inf for _ in range(len(columns))] for _ in range(3)]

    def update_column(self, column: str or int, values: tuple[float, float, float]):
        idx = self.__column_names.index(column)

        if values[2] < self.__rows[2][idx]:
            self.__rows[0][idx] = values[0]
            self.__rows[1][idx] = values[1]
            self.__rows[2][idx] = values[2]

    def show(self, highlight_best: bool = False):
        column_names = deepcopy(self.__column_names)
        rows = deepcopy(self.__rows)

        if highlight_best:
            best_column_idx = rows[2].index(min(rows[2]))

            column_names[best_column_idx] = Fore.GREEN + str(column_names[best_column_idx]) + Style.RESET_ALL
            rows[0][best_column_idx] = Fore.GREEN + str(rows[0][best_column_idx]) + Style.RESET_ALL
            rows[1][best_column_idx] = Fore.GREEN + str(rows[1][best_column_idx]) + Style.RESET_ALL
            rows[2][best_column_idx] = Fore.GREEN + str(rows[2][best_column_idx]) + Style.RESET_ALL

        quadratic_info_table = PrettyTable([''] + column_names)
        quadratic_info_table.add_row(['Partitions'] + rows[0])
        quadratic_info_table.add_row(['Value'] + rows[1])
        quadratic_info_table.add_row(['Residue'] + rows[2])

        print(quadratic_info_table)


def func(x: float or np.ndarray) -> float or np.ndarray:
    return 3 * np.cos(3.5 * x) * np.exp(4 * x / 3) + 2 * np.sin(3.5 * x) * np.exp(-2 * x / 3) + 4 * x


def moment(a: float, b: float, alpha: float, beta: float, degree: int) -> float:
    coeff = max(alpha, beta)
    moment_val = lambda x: x ** (degree - coeff + 1) / (degree - coeff + 1)

    return moment_val(b) - moment_val(a)


def cardano_formula(poly: np.ndarray) -> np.ndarray:
    """Формула Кардано для нахождения корней кубического уравнения"""
    q = (2 * poly[1] ** 3 / (54 * poly[0] ** 3)
         - poly[1] * poly[2] / (6 * poly[0] ** 2)
         + poly[3] / poly[0] / 2)

    p = (3 * poly[0] * poly[2] - poly[1] ** 2) / (9 * poly[0] ** 2)

    # Нас интересует только та часть формулы, где (q ** 2 + p ** 3) < 0. В методе Гаусса при разумном
    # числе разбиений, это всегда выполняется
    r = np.sign(q) * np.sqrt(np.abs(p))
    phi = np.arccos(q / r ** 3)

    y_roots = np.array([
        -2 * r * np.cos(phi / 3),
        2 * r * np.cos(np.pi / 3 - phi / 3),
        2 * r * np.cos(np.pi / 3 + phi / 3)
    ])

    roots = y_roots - poly[1] / poly[0] / 3
    return roots


def plot_residues_graphics(methods_residues: dict[str, list[float]]):
    plt.figure(figsize=(15, 6))

    plt.subplot(1, 2, 1)
    plt.title('График погрешности')
    for method, residues in methods_residues.items():
        plt.plot(range(len(residues)), residues, label=f'{method} Residues')

    plt.ylabel('Погрешность')
    plt.xlabel('Разбиения')
    plt.grid()
    plt.legend()            

    plt.subplot(1, 2, 2)
    plt.title('График погрешности(в логарифмической форме)')
    for method, residues in methods_residues.items():
        plt.plot(range(len(residues)), np.log(np.array(residues)), label=f'{method} Residues')

    plt.ylabel('Погрешность(в логарифмической форме)')
    plt.xlabel('Разбиения')
    plt.grid()
    plt.legend()

    plt.show()
