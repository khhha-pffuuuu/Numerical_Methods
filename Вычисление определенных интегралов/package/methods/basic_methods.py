def quad_left_rect(func, a: float, b: float, num_partitions: int = 100) -> float:
    """Квадратурная формула левого прямоугольника. АСТ = 0"""
    result = 0

    for i in range(num_partitions):
        l_border = a + (b - a) * i / num_partitions
        r_border = a + (b - a) * (i + 1) / num_partitions

        result += (r_border - l_border) * func(l_border)

    return result


def quad_right_rect(func, a: float, b: float, num_partitions: int = 100) -> float:
    """Квадратурная формула правого прямоугольника. АСТ = 0"""
    result = 0

    for i in range(num_partitions):
        l_border = a + (b - a) * i / num_partitions
        r_border = a + (b - a) * (i + 1) / num_partitions

        result += (r_border - l_border) * func(r_border)

    return result


def quad_middle_rect(func, a: float, b: float, num_partitions: int = 100) -> float:
    """Квадратурная формула среднего прямоугольника. АСТ = 1"""
    result = 0

    for i in range(num_partitions):
        l_border = a + (b - a) * i / num_partitions
        r_border = a + (b - a) * (i + 1) / num_partitions

        result += (r_border - l_border) * func((l_border + r_border) / 2)

    return result


def quad_trapezia(func, a: float, b: float, num_partitions: int = 100) -> float:
    """Квадратурная формула трапеции. АСТ = 1"""
    result = 0

    for i in range(num_partitions):
        l_border = a + (b - a) * i / num_partitions
        r_border = a + (b - a) * (i + 1) / num_partitions

        result += (r_border - l_border) * (func(l_border) + func(r_border)) / 2

    return result


def quad_simpson(func, a: float, b: float, num_partitions: int = 100) -> float:
    """Квадратурная формула Симпсона. АСТ = 3"""
    result = 0

    for i in range(num_partitions):
        l_border = a + (b - a) * i / num_partitions
        r_border = a + (b - a) * (i + 1) / num_partitions

        result += (r_border - l_border) * (func(l_border) + 4 * func((l_border + r_border) / 2) + func(r_border)) / 6

    return result
