import numpy as np
from random import random as rnd
from genmodel.test_functions import TestFunctions


class Chromosome:
    def __init__(self, upper_limit, lower_limit):
        self.x = round(rnd() * (upper_limit - lower_limit) + lower_limit, 1)
        self.y = round(rnd() * (upper_limit - lower_limit) + lower_limit, 1)
        self.fitness_value = -TestFunctions.rosenbrock_function(self.x, self.y)

    def fitness_calculation(self):
        self.fitness_value = -TestFunctions.rosenbrock_function(self)

    def __str__(self):
        return f"Chromosome [#{self.x}, #{self.y}] gives value: #{self.fitness_value}"


class Population:
    def __init__(self, number_of_individuals, upper_limit, lower_limit):
        self.chromosomes = [Chromosome(upper_limit, lower_limit) for _ in range(number_of_individuals)]

    def __str__(self):
        s = ""
        for chromosome in self.chromosomes:
            s += str(chromosome) + "\n"
        return s


class Generation:
    def __init__(self, population: Population):
        self.individuals = sorted(population.chromosomes, key=lambda x: x.fitness_value, reverse=True)
        self.fitness = [c.fitness_value for c in self.individuals]
        self.normalized_fitness = sorted(
            [self.fitness[x] / sum(self.fitness) for x in range(len(self.fitness))],
            reverse=True)

        self.cumulative_sum = np.array(self.normalized_fitness).cumsum()
