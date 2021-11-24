from genmodel.model import Chromosome


class TestFunctions:
    @classmethod
    def rosenbrock_function(cls, chromosome: Chromosome):
        """
        Функция Розенброка
        :rtype: float
        """
        return (1 - chromosome.x) ** 2 + 100 * (chromosome.y - chromosome.x ** 2) ** 2

    @classmethod
    def rosenbrock_function(cls, x, y):
        """
        Функция Розенброка
        :rtype: float
        """
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2
