import numpy as np


class TestFunctions:
    @classmethod
    def rosenbrock_function(cls, x, y):
        """
        Функция Розенброка
        :rtype: float
        """
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

    @classmethod
    def kkhvan_function(cls, x, y):
        """
        Функция z(x,y) = exp(-(x^2) - (y^2))
        :rtype: float
        """
        return -np.exp(-x ** 2 - y ** 2)

    # TODO: Прописать функцию для Дианы
    @classmethod
    def dshishkina_function(cls, x, y):
        """
        Функция z(x,y) = exp(-(x^2) - (y^2))
        :rtype: float
        """

        return np.sin(x ** 2) + np.cos(y ** 2)

    @classmethod
    def rastrigin(cls, x, y, n):
        """
        это для двумерного случая
        :param x:
        :param y:
        :param n: размерность
        :return:
        """
        return 10.0 * n + (x * x - 10.0 * np.cos(2 * np.pi * x)) + (y * y - 10.0 * np.cos(2 * np.pi * y))
