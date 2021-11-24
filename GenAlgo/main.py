import numpy as np
from numpy.random import randint
from random import random as rnd
from random import gauss, randrange
from genmodel.model import Chromosome, Population, Generation
from genmodel.test_functions import TestFunctions


def selection(generation: Generation, method='Fittest Half'):
    if method == 'Fittest Half':
        selected_individuals = [generation.individuals[x] for x in range(int(len(generation.individuals) // 2))]
        selected_fitness = [generation.fitness[x] for x in range(int(len(generation.individuals) // 2))]
        selected = {'Individuals': selected_individuals,
                    'Fitness': selected_fitness}
    elif method == 'Random':
        selected_individuals = [generation.individuals[randint(1, len(generation.individuals))] for x in
                                range(int(len(generation.individuals) // 2))]
        selected_fitness = [generation.fitness[x] for x in range(int(len(generation.individuals) // 2))]
        selected = {'Individuals': selected_individuals,
                    'Fitness': selected_fitness}
    return selected


def main():
    generations = [Generation(Population(20, 8, 1))]
    fitness_avg = np.array([sum(generations[0].fitness) / len(generations[0].fitness)])
    fitness_max = np.array([max(generations[0].fitness)])

    # Это из примера в интернете
    # finish = False
    # while not finish:
    #     if max(fitness_max) > 6:
    #         break
    #     if max(fitness_avg) > 5:
    #         break
    #     if fitness_similarity_check(fitness_max, 50):
    #         break
    #     generations.add(next_generation(gen[-1], 1, 0))
    #     fitness_avg = np.append(fitness_avg, sum(
    #         gen[-1]['Fitness']) / len(gen[-1]['Fitness']))
    #     fitness_max = np.append(fitness_max, max(gen[-1]['Fitness']))
    #     res = open(result_file, 'a')
    #     res.write('\n' + str(gen[-1]) + '\n')
    #     res.close()


if __name__ == "main":
    main()
