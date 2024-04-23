class OP(object):
    def __init__(self, args: list[float] = None, prev = None, prev_ = None):
        """Высчитываем коэффициенты для полинома. Вообще говоря, каждый объект предложено считать рекуррентно, но
        здесь объект класса создает полиномы в привычном виде, то есть хранит только коэффициенты перед каждой
        степенью x"""
        self.poly_n = 0
        self.coeffs = []  # Коэффициенты полинома

        if any([prev, prev_]):  # Есть хотя бы один предшественник
            m = len(args)

            # Считаем a и b в соответствии с теорией
            if prev_ is None:  # Есть ровно один предшественник
                a = sum([args[i] for i in range(m)]) / m
                self.poly_n = 1
                self.coeffs = [-a, 1]

            else:  # Есть ровно два предшественника
                a = (sum([args[i] * prev(args[i]) ** 2 for i in range(m)]) /
                          sum([prev(args[i]) ** 2 for i in range(m)]))
                b = (sum([args[i] * prev(args[i]) * prev_(args[i]) for i in range(m)]) /
                          sum([prev_(args[i]) ** 2 for i in range(m)]))

                n = prev.poly_n
                self.poly_n = n + 1

                # Непосредственно сам алгоритм вычисления коэффициентов
                self.coeffs += [-a * prev.coeffs[0] - b * prev_.coeffs[0]]
                self.coeffs += [(prev.coeffs[i - 1] - a * prev.coeffs[i] - b * prev_.coeffs[i]) for i in range(1, n)]
                self.coeffs += [prev.coeffs[n - 1] - a * prev.coeffs[n], 1]

        else:  # Нет ни одного предшественника
            self.coeffs = [1]

    def __call__(self, x: float) -> float:
        return sum([self.coeffs[i] * x ** i for i in range(self.poly_n + 1)])


class OLS(object):
    def __init__(self, args: list[float], vals: list[float], n: int):
        """Сохраняем ортогональные многочлены и коэффициенты"""
        self.poly_n = n

        # Строим систему ортогональных многочленов
        self.ops = [OP(), OP(args, OP())]
        for i in range(2, n + 1):
            self.ops.append(OP(args, self.ops[i - 1], self.ops[i - 2]))

        # Теперь высчитываем коэффициенты перед многочленами
        m = len(args)
        self.coeffs = []
        for i in range(n + 1):
            self.coeffs.append(sum([self.ops[i](args[j]) * vals[j] for j in range(m)]) /
                               sum([self.ops[i](args[j]) ** 2 for j in range(m)]))

    def __call__(self, x: float or list[float]) -> float or list[float]:
        """Обращаемся к объекту как к функции"""
        if isinstance(x, int) or isinstance(x, float):
            return sum([self.coeffs[i] * self.ops[i](x) for i in range(self.poly_n + 1)])
        else:  # Можно возвращать список значений
            return [sum([self.coeffs[i] * self.ops[i](x_) for i in range(self.poly_n + 1)]) for x_ in x]
