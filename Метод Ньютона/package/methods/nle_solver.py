def enumeration(function, segment) -> tuple:
    """Поиск приближения промежутка, в котором лежит корень, при помощи последовательного перебора"""
    n = 1  # Начальная длина дробления
    start, end = segment
    x = start

    while True:
        if x == end:  # Если мы достигли конца заданной области значений, но никак не локализовали корень, то начинаем
            # сначала и ранг дробления увеличиваем вдвое
            x = start
            n /= 2

        x_ = x + n

        if function(x) * function(x_) < 0:  # Это неравенство показывает, что в заданном промежутке находится корень
            return x, x_
        elif function(x) * function(x_) == 0:  # Случай, если корень уже находится на границе
            return (x, x) if function(x) == 0 else (x_, x_)

        x = x_


def root_search(function, function_derivative, segment) -> float:
    """Поиск корней при помощи комбинации метода Ньютона и метода половинного деления"""
    eps = 10 ** -4  # Заданная погрешность

    a, b = enumeration(function, segment)  # Приближенный промежуток
    x = a

    while True:
        # Если производная равна нулю в точке x, тогда смещаем точку внутрь промежутка меньше, чем на eps
        if function_derivative(x) == 0:
            x = x + 10 ** -5 if x == a else x - 10 ** -5

        x_ = x - function(x) / function_derivative(x)

        # Если x_ "вылетел" за пределы заданного промежутка, то возвращаем его внутрь
        if not (a <= x_ <= b):
            x_ = (a + b) / 2

        # Сжимаем промежуток [a,b]
        if function(a) * function(x_) < 0:
            b = x_
        else:
            a = x_

        if abs(x_ - x) < eps:  # Критерий остановки
            return x_

        x = x_
