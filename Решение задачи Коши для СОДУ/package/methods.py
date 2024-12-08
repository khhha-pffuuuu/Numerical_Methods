import numpy as np
from numpy.linalg import norm
from copy import deepcopy


class ODE(object):
    def __init__(self, method='BASE'):
        self.method = method

        if self.method not in ['BASE', 'RUNGE_KUTTA']:
            raise ValueError('Method must be BASE or RUNGE_KUTTA')

    @staticmethod
    def __my_var(f, x_start: float, y_start: np.ndarray, x_end: float, step: float) -> (np.ndarray, int):
        """Реализованный метод из моего варианта"""
        zeta = 1 / 17
        a, c, b = zeta, zeta, np.array([1 - 1 / 2 / zeta, 1 / 2 / zeta])

        x_curr, y_curr = deepcopy(x_start), deepcopy(y_start)
        calc_count = 0
        while x_curr < x_end:
            k1 = step * f(x_curr, y_curr)
            k2 = step * f(x_curr + step * c, y_curr + a * k1)

            calc_count += 2

            k = np.vstack([k1, k2]).T

            x_curr = min(x_curr + step, x_end)
            y_curr = y_curr + k @ b

        return y_curr, calc_count

    @staticmethod
    def __runge_kutta(f, x_start: float, y_start: np.ndarray, x_end: float, step: float) -> (np.ndarray, int):
        """Реализованный метод Рунге-Кутты из справочника"""
        x_curr, y_curr = deepcopy(x_start), deepcopy(y_start)
        calc_count = 0
        while x_curr < x_end:
            k1 = step * f(x_curr, y_curr)
            k2 = step * f(x_curr + step / 2, y_curr + k1 / 2)
            k3 = step * f(x_curr + step / 2, y_curr + k2 / 2)
            k4 = step * f(x_curr + step, y_curr + k3)

            calc_count += 4

            x_curr = min(x_curr + step, x_end)
            y_curr = y_curr + (k1 + 2 * k2 + 2 * k3 + k4) / 6

        return y_curr, calc_count

    def __call__(self, f, x_start: float, y_start: np.ndarray, x_end: float, step: float = None,
                 steps_type: str = 'adaptive', eps: float = 10 ** -4) -> (list, list, list, int):

        if self.method == 'BASE':
            ode_base = self.__my_var
            degree = 2
        else:  # Рунге-Кутта
            ode_base = self.__runge_kutta
            degree = 4

        if step is None:
            # Если не задан шаг, то автоматически его выбираем
            delta = 1 / max(abs(x_start), abs(x_end)) ** (degree + 1) + np.linalg.norm(y_start) ** (degree + 1)
            step = (eps / delta) ** (1 / (degree + 1))

        x_curr, y_curr = deepcopy(x_start), deepcopy(y_start)
        calc_count = 0  # Количество вычислений f(x, y)

        if steps_type == 'none':
            return ode_base(f, x_start, y_start, x_end, step)

        # Метод постоянного шага
        elif steps_type == 'const':
            while True:
                y_curr, calcs = ode_base(f, x_start, y_start, x_end, step)
                y_curr_half, calcs_half = ode_base(f, x_start, y_start, x_end, step / 2)

                calc_count += calcs + calcs_half

                # Считаем погрешность по методу Рунге
                error = (y_curr_half - y_curr) / (1 - 2 ** -degree)
                error_norm = np.linalg.norm(error)

                if error_norm < eps:
                    return y_curr, error, step, calc_count

                step = step / 2

        # Метод автоматического выбора шага
        elif steps_type == 'adaptive':
            values = []  # Список последовательно высчитанных значений
            local_errors = []  # Список локальных погрешностей
            steps = []  # Список шагов

            while x_curr < x_end:
                step = min(step, x_end - x_curr)  # Если шаг "вылетает" за пределы, то возвращаем его"

                y_curr_whole, calcs = ode_base(f, x_curr, y_curr, x_curr + step, step)
                y_curr_half, calcs_half = ode_base(f, x_curr, y_curr, x_curr + step, step / 2)

                calc_count += calcs + calcs_half

                local_error = (y_curr_half - y_curr_whole) / (1 - 2 ** -degree)
                error_norm = np.linalg.norm(local_error)

                # Критерии выбора шага
                if error_norm > 2 ** degree * eps:
                    step = step / 2

                elif eps < error_norm < 2 ** degree * eps:
                    x_curr = x_curr + step
                    y_curr = y_curr_half

                    values.append(y_curr)
                    local_errors.append(error_norm)
                    steps.append(step)
                    step = step / 2

                elif eps / 2 ** (degree + 1) < error_norm < eps:
                    x_curr = x_curr + step
                    y_curr = y_curr_whole

                    values.append(y_curr)
                    local_errors.append(error_norm)
                    steps.append(step)

                else:
                    x_curr = x_curr + step
                    y_curr = y_curr_whole

                    values.append(y_curr)
                    local_errors.append(error_norm)
                    steps.append(step)
                    step = 2 * step

            return values, local_errors, steps, calc_count
