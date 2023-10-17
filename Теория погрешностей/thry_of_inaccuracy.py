import math

import task_functions as func


def main():
    x = 0.01

    while x <= 0.06:
        x = round(x * 1000) / 1000
        z = func.sqrt(2 * x + 0.4) * func.arctan(func.cos(3 * x + 1))
        z_ = math.sqrt(2 * x + 0.4) * math.atan(math.cos(3 * x + 1))

        print(f'x = {x}:\n'
              f'sqrt: |{func.sqrt(x)} - {math.sqrt(x)}| = {abs(func.sqrt(x) - math.sqrt(x))}\n'
              f'arctg: |{func.arctan(x)} - {math.atan(x)}| = {abs(func.arctan(x) - math.atan(x))}\n'
              f'cos: |{func.cos(x)} - {math.cos(x)}| = {abs(func.cos(x) - math.cos(x))}\n'
              f'z: |{z} - {z_}| = {abs(z - z_)}', end="\n\n")

        x += 0.005


if __name__ == '__main__':
    main()
