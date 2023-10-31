from .helpers import sqrt


class Matrix(object):
    discard_index = 30  # Количество цифр после запятой

    def __new__(cls, matrix):
        """Объект матрицы можно создать, только если аргументом является либо файлом с матрицей,
        либо двумерным массивом"""
        try:
            if isinstance(matrix, list) and isinstance(matrix[0], list):
                return super().__new__(cls)
        except IndexError:
            pass

    def __init__(self, matrix):
        self.__matrix = matrix

        self.__r_count = len(self.__matrix)
        self.__c_count = len(self.__matrix[0])

    @property
    def dim(self):
        """Возвращает размерность матрицы в виде tuple (A.dim = (n, m))"""
        return self.__r_count, self.__c_count

    def __str__(self):
        """Вывод матрицы (print(A))"""
        str_matrix = []

        for row in self.__matrix:
            str_row = []
            for elem in row:
                format_elem = f"{elem:.{self.discard_index}f}" \
                    if f"{elem:.{self.discard_index}f}" != f'-{0:.{self.discard_index}f}' \
                    else f'{0:.{self.discard_index}f}'

                str_row.append(format_elem)
            str_matrix.append('   '.join(str_row))

        str_matrix = '\n'.join(str_matrix)

        return str_matrix

    def __eq__(self, other):
        """Проверка матриц на равенство (A == B)"""
        for i in range(self.__r_count):
            for j in range(self.__c_count):
                if self.__matrix[i][j] != other.__matrix[i][j]:
                    return False

        return True

    def __ne__(self, other):
        """Проверка матриц на неравенство (A != B)"""
        for i in range(self.__r_count):
            for j in range(self.__c_count):
                if self.__matrix[i][j] != other.__matrix[i][j]:
                    return True

        return False

    def __bool__(self):
        """Функция возвращает True, если матрица ненулевая"""
        for i in range(self.__r_count):
            for j in range(self.__c_count):
                if self.__matrix[i][j] != 0:
                    return True

        return False

    @property
    def is_pd(self):
        """Проверка матрицы на положительную определенность (только для квадратных матрицы)"""
        for i in range(self.__r_count):
            minor = self.copy
            for _ in range(i + 1, self.__c_count):
                m = minor.dim[0] - 1
                minor = minor[m: m]
            elem = minor.det // abs(minor.det) if minor.det != 0 else 0

            if elem <= 0:
                return False

        return True

    @property
    def is_dd(self):
        """Проверка матрицы на диагональное преобладание (только для квадратных матрицы)"""
        for i in range(self.__r_count):
            row_sum = 0
            for j in range(self.__c_count):
                row_sum = row_sum + abs(self.__matrix[i][j]) if i != j else row_sum

            if abs(self.__matrix[i][i]) <= row_sum:
                return False

        return True

    def __setitem__(self, index, value):
        """Функция задает значение либо элементу матрицы (A[i,j] = α),
        либо строке(столбцу) (A(i, None) = a, A(None, j) = a,
        либо всем элементам >= i и >= j(более понятным языком, меняет элементы
        'прямоугольника', ограниченного индексами i, j, внутри матрицы,
        использовать можно так: A[i; j: step] = B, если step = 1, тогда замена
        идет от индексов, если step == -1 - до)"""

        if isinstance(index, tuple):
            row, column = index

            if None not in index:
                self.__matrix[row][column] = value

            elif row is not None and column is None:
                for i in range(self.__c_count):
                    self.__matrix[row][i] = value.__matrix[0][i]

            elif row is None and column is not None:
                for i in range(self.__r_count):
                    self.__matrix[i][column] = value.__matrix[i][0]

        elif isinstance(index, slice):
            row_index = index.start
            column_index = index.stop
            side_index = index.step

            if side_index == 1:
                for i in range(row_index, self.__r_count):
                    for j in range(column_index, self.__c_count):
                        self.__matrix[i][j] = value.__matrix[i - row_index][j - column_index]

            elif side_index == -1:
                for i in range(row_index):
                    for j in range(column_index):
                        self.__matrix[i][j] = value.__matrix[i][j]

    def __getitem__(self, index):
        """Функция возвращает либо обрезанную матрицу (A[i:j], например,
        дана матрица A = [[1, 0], [0, 1]], тогда A[1: 1] = [[1]], к тому же,
        вырезать только строку или столбец можно таким образом: A[i: None],
        A[None: j]), либо один элемент (A[i,j]), либо вектор из матрицы
        (A[i, None] или A[None, i])"""
        if isinstance(index, slice):
            row_index = index.start
            column_index = index.stop

            matrix = []

            for i in range(self.__r_count):
                if i != row_index:
                    row = []
                    for j in range(self.__c_count):
                        if j != column_index:
                            row.append(self.__matrix[i][j])
                    matrix.append(row)

            return Matrix(matrix)

        elif isinstance(index, tuple):
            row, column = index

            if row is None and column is not None:
                matrix = []
                for i in range(self.__r_count):
                    matrix.append([self.__matrix[i][column]])

                return Matrix(matrix)

            elif column is None and row is not None:
                matrix = []

                row_list = []
                for i in range(self.__c_count):
                    row_list.append(self.__matrix[row][i])
                matrix.append(row_list)

                return Matrix(matrix)

            elif None not in index:
                return self.__matrix[row][column]

    def __mul__(self, other):
        """Функция умножает матрицу либо на число (A * α), либо на матрицу (A * B)"""
        if isinstance(other, float) or isinstance(other, int):
            matrix = []

            for i in range(self.__r_count):
                row = []
                for j in range(self.__c_count):
                    elem = self.__matrix[i][j] * other
                    row.append(elem)
                matrix.append(row)

            return Matrix(matrix)

        else:
            matrix = []

            for i in range(self.__r_count):
                row = []
                for j in range(other.__c_count):
                    elem = 0
                    for k in range(self.__c_count):
                        elem += self.__matrix[i][k] * other.__matrix[k][j]
                    row.append(elem)
                matrix.append(row)

            return Matrix(matrix)

    def __rmul__(self, other):
        """Функция позволяет коммутативно умножать матрицу на число"""
        if not isinstance(other, Matrix):
            return self.__mul__(other)

    def __imul__(self, other):
        """Перегрузка оператора *= для чисел"""
        if not isinstance(other, Matrix):
            return self.__mul__(other)

    def __truediv__(self, other):
        """Деление матрицы на число"""
        matrix = []

        for i in range(self.__r_count):
            row = []
            for j in range(self.__c_count):
                elem = self.__matrix[i][j] / other
                row.append(elem)
            matrix.append(row)

        return Matrix(matrix)

    def __idiv__(self, other):
        """Перегрузка оператора \="""
        return self.__truediv__(other)

    def __matmul__(self, other):
        """Скалярное произведение (a @ b)"""
        vec1 = ~self if self.__c_count == 1 else self
        vec2 = ~other if other.__r_count == 1 else other

        in_prod = 0

        for i in range(vec1.__c_count):
            in_prod += vec1.__matrix[0][i] * vec2.__matrix[i][0]

        return in_prod

    def __add__(self, other):
        """Сложение матриц (A + B), либо сложение векторов (a + b)"""
        if min(self.__r_count, other.__r_count, self.__c_count, other.__c_count) != 1:
            matrix = []

            for i in range(self.__r_count):
                row = []
                for j in range(self.__c_count):
                    elem = self.__matrix[i][j] + other.__matrix[i][j]
                    row.append(elem)
                matrix.append(row)

            return Matrix(matrix)

        else:
            vec1 = ~self if self.__r_count == 1 else self
            vec2 = ~other if other.__r_count == 1 else other

            matrix = []
            for i in range(vec1.__r_count):
                matrix.append([vec1.__matrix[i][0] + vec2.__matrix[i][0]])

            return Matrix(matrix)

    def __iadd__(self, other):
        """Перегрузка оператора +="""
        return self.__add__(other)

    def __sub__(self, other):
        """Разность матриц (A - B), либо разность векторов (a - b)"""
        return self + (-1) * other

    def __isub__(self, other):
        """Перегрузка оператора -="""
        return self.__sub__(other)

    def __pow__(self, power, modulo=None):
        """Возведение матрицы в степень (A ** α); эта функция достаточно точно работает, если power >= -14"""
        if power == 1:
            return self.copy
        elif power < -1:
            return (self ** -power) ** -1
        elif power == 0:
            return Matrix.E(self.__r_count)
        elif power == 2:
            return self * self
        elif power == -1:
            matrix = []
            for i in range(self.__c_count):
                row = []
                for j in range(self.__r_count):
                    elem = (-1) ** (i + j) * (self[j: i].det / self.det)
                    row.append(elem)
                matrix.append(row)

            return Matrix(matrix)

        if power % 2 == 0:
            return (self ** 2) * (self ** (power // 2))
        else:
            return self * (self ** (power - 1))

    def __ipow__(self, other):
        """Перегрузка оператора **="""
        return self.__pow__(other)

    def __invert__(self):
        """Транспонированние матрицы (~A)"""
        matrix = []

        for i in range(self.__c_count):
            row = []
            for j in range(self.__r_count):
                row.append(self.__matrix[j][i])
            matrix.append(row)

        return Matrix(matrix)

    @property
    def det(self):
        """Определитель матрицы (A.det)"""
        if self.__r_count == 1:
            return self.__matrix[0][0]
        elif self.__r_count == 2:
            return self.__matrix[0][0] * self.__matrix[1][1] - self.__matrix[1][0] * self.__matrix[0][1]

        det = 0
        for i in range(self.__c_count):
            det += (-1) ** i * self.__matrix[0][i] * self[0:i].det

        return det

    def __abs__(self):
        """Нахождение евклидовой нормы (abs(a))"""
        return sqrt(self @ self)

    def norm(self, norm_type):
        """Нахождение единичной нормы (A.norm(1)) и бесконечную норму (A.norm('inf'))"""
        if norm_type == 1:
            norm = 0

            for i in range(self.__c_count):
                column_sum = 0
                for j in range(self.__r_count):
                    column_sum += abs(self.__matrix[j][i])
                norm = column_sum if norm < column_sum else norm

            return norm

        if norm_type == 'inf':
            norm = 0

            for i in range(self.__r_count):
                row_sum = 0
                for j in range(self.__c_count):
                    row_sum += abs(self.__matrix[i][j])
                norm = row_sum if norm < row_sum else norm

            return norm

    @property
    def copy(self):
        """Копирует матрицу. Это необходимо, так как, например, new_matrix = A, ссылки на все элементы останутся теми
        же, то есть при изменении new_matrix будет изменяться и A"""
        matrix = []

        for i in range(self.__r_count):
            row = []
            for j in range(self.__c_count):
                row.append(self.__matrix[i][j])
            matrix.append(row)

        return Matrix(matrix)

    @staticmethod
    def E(n):
        """Возвращает единичную матрицу той же размерности, что и у матрицы"""
        matrix = []

        for i in range(n):
            row = []
            for j in range(n):
                elem = 0 if i != j else 1
                row.append(elem)
            matrix.append(row)

        return Matrix(matrix)

    @staticmethod
    def NULL_VECTOR(n):
        """Возвращает нулевой вектор"""
        return Matrix([[0] for _ in range(n)])
