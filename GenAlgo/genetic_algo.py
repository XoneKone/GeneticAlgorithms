import sys

import numpy as np
from PyQt5 import QtWidgets
from numpy.random import randint
from random import random as rnd
from random import gauss
from test_functions import TestFunctions
import test

import constants


def individual(number_of_genes, upper_limit, lower_limit):
    individual = [round(rnd() * (upper_limit - lower_limit) + lower_limit, 2) for x in range(number_of_genes)]
    return individual


def population(number_of_individuals, number_of_genes, upper_limit, lower_limit):
    return [individual(number_of_genes, upper_limit, lower_limit) for x in range(number_of_individuals)]


# TODO: Сделать универсальную фукнцию.
# TODO:  Возможно, вынести параметры, для которых будут вызываться вычисление соотвествующей функции
# TODO: Поменять в функциях соответсвующие вызовы этого метода
# Сюда поставлю глобальную переменную, чтобы определять находим мы min, max
mode = constants.MAX
# А сюда, чтобы определять чью задачу решать
task = constants.KHVAN  # R - Rosenbrok, K - Khvan, S - Shishkina


def fitness_calculation(individual):
    global mode
    if task == constants.ROSENBROCK:
        return -TestFunctions.rosenbrock_function(individual[0], individual[1])
    elif task == constants.KHVAN:
        return -TestFunctions.kkhvan_function(individual[0], individual[1])
    elif task == constants.SHISHKINA:
        return -TestFunctions.dshishkina_function(individual[0], individual[1])


def selection(generation, method='Fittest Half'):
    if method == 'Fittest Half':
        selected_individuals = [generation['Individuals'][-x - 1]
                                for x in range(int(len(generation['Individuals']) // 2))]
        selected_fitnesses = [generation['Fitness'][-x - 1]
                              for x in range(int(len(generation['Individuals']) // 2))]
        selected = {'Individuals': selected_individuals,
                    'Fitness': selected_fitnesses
                    }
    elif method == 'Random':
        selected_individuals = [generation['Individuals'][randint(1, len(generation['Fitness']))] for x in
                                range(int(len(generation['Individuals']) // 2))]
        selected_fitnesses = [generation['Fitness'][-x - 1]
                              for x in range(int(len(generation['Individuals']) // 2))]
        selected = {'Individuals': selected_individuals,
                    'Fitness': selected_fitnesses
                    }
    return selected


def pairing(elit, selected, method='Fittest'):
    individuals = [elit['Individuals']] + selected['Individuals']
    fitness = [elit['Fitness']] + selected['Fitness']
    if method == 'Fittest':
        parents = [[individuals[x], individuals[x + 1]] for x in range(len(individuals) // 2)]
    if method == 'Random':
        parents = []
        for x in range(len(individuals) // 2):
            parents.append(
                [individuals[randint(0, (len(individuals) - 1))], individuals[randint(0, (len(individuals) - 1))]])
            while parents[x][0] == parents[x][1]:
                parents[x][1] = individuals[randint(0, (len(individuals) - 1))]
    return parents


def mating(parents, method='Single Point'):
    if method == 'Single Point':
        pivot_point = randint(1, len(parents[0]))
        offsprings = [parents[0][0:pivot_point] + parents[1][pivot_point:],
                      parents[1][0:pivot_point] + parents[0][pivot_point:]]
    if method == 'Two Points':
        pivot_point_1 = randint(1, len(parents[0] - 1))
        pivot_point_2 = randint(1, len(parents[0]))
        while pivot_point_2 < pivot_point_1:
            pivot_point_2 = randint(1, len(parents[0]))
        offsprings = [
            parents[0][0:pivot_point_1] + parents[1][pivot_point_1:pivot_point_2] + [parents[0][pivot_point_2:]],
            [parents[1][0:pivot_point_1] + parents[0][pivot_point_1:pivot_point_2] + [parents[1][pivot_point_2:]]]]
    return offsprings


def mutation(individual, upper_limit, lower_limit, muatation_rate=2, method='Gauss', standard_deviation=0.06):
    mutated_individual = individual.copy()
    if method == 'Gauss':
        for x in range(muatation_rate):
            mutated_individual[x] = round(individual[x] + gauss(0, standard_deviation), 2)
    if method == 'Reset':
        for x in range(muatation_rate):
            mutated_individual[x] = round(rnd() * (upper_limit - lower_limit) + lower_limit, 2)
    return mutated_individual


def next_generation(gen, upper_limit, lower_limit):
    elit = {}
    next_gen = {}
    elit['Individuals'] = gen['Individuals'].pop(-1)
    elit['Fitness'] = gen['Fitness'].pop(-1)
    selected = selection(gen)
    parents = pairing(elit, selected)
    offsprings = [[[mating(parents[x]) for x in range(len(parents))][y][z] for z in range(2)]
                  for y in range(len(parents))]
    offsprings1 = [offsprings[x][0] for x in range(len(parents))]
    offsprings2 = [offsprings[x][1] for x in range(len(parents))]
    unmutated = selected['Individuals'] + offsprings1 + offsprings2
    # mutated = unmutated
    # print(mutated)
    mutated = [mutation(unmutated[x], upper_limit, lower_limit) for x in range(len(gen['Individuals']))]
    unsorted_individuals = mutated + [elit['Individuals']]
    unsorted_next_gen = [fitness_calculation(mutated[x]) for x in range(len(mutated))]
    unsorted_fitness = [unsorted_next_gen[x] for x in range(len(gen['Fitness']))] + [elit['Fitness']]
    sorted_next_gen = sorted([[unsorted_individuals[x], unsorted_fitness[x]]
                              for x in range(len(unsorted_individuals))],
                             key=lambda x: x[1])
    next_gen['Individuals'] = [sorted_next_gen[x][0] for x in range(len(sorted_next_gen))]
    next_gen['Fitness'] = [sorted_next_gen[x][1] for x in range(len(sorted_next_gen))]
    gen['Individuals'].append(elit['Individuals'])
    gen['Fitness'].append(elit['Fitness'])
    return next_gen


def fitness_similarity_check(max_fitness, number_of_similarity):
    result = False
    similarity = 0
    for n in range(len(max_fitness) - 1):
        if max_fitness[n] == max_fitness[n + 1]:
            similarity += 1
        else:
            similarity = 0
    if similarity == number_of_similarity - 1:
        result = True
    return result


def first_generation(pop):
    fitness = [fitness_calculation(pop[x]) for x in range(len(pop))]
    sorted_fitness = sorted([[pop[x], fitness[x]] for x in range(len(pop))], key=lambda x: x[1])
    population = [sorted_fitness[x][0] for x in range(len(sorted_fitness))]
    fitness = [sorted_fitness[x][1] for x in range(len(sorted_fitness))]
    return {'Individuals': population, 'Fitness': sorted(fitness)}


def run(generations_number, number_of_individuals, upper_limit, lower_limit):
    global mode
    number_of_genes = 2
    pop = population(number_of_individuals, number_of_genes, upper_limit, lower_limit)
    gen = [first_generation(pop)]
    fitness_avg = np.array([0.0, sum(gen[0]['Fitness']) / len(gen[0]['Fitness'])])
    fitness_max = np.array([0.0, max(gen[0]['Fitness'])])
    finish = False
    similarity = 0
    while not finish:
        # if abs(fitness_max[-1] - fitness_max[-2]) <= eps_max:
        #     break
        # if abs(fitness_avg[-1] - fitness_avg[-2]) <= eps_avg:
        #     break
        if fitness_max[-1] == fitness_max[-2]:
            similarity += 1
        if similarity == 12:
            break
        if len(gen) >= generations_number:
            break
        gen.append(next_generation(gen[-1], 1, 0))
        fitness_avg = np.append(fitness_avg, sum(gen[-1]['Fitness']) / len(gen[-1]['Fitness']))
        fitness_max = np.append(fitness_max, max(gen[-1]['Fitness']))
    ## Для минимума нужно сделать инверсию значений
    for gener in gen:
        gener["Fitness"] = [-x for x in gener["Fitness"]]
    with open("GA_results.txt", "w") as res:
        for index, generation in enumerate(gen, 1):
            res.write("INFO about generation " + str(index) + ':\n')
            for indiv in zip(generation['Individuals'], generation['Fitness']):
                res.write("Individual " + str(indiv[0]) + " gives value: " + str(indiv[1]) + "\n")
            res.write("\nmin value for this generation: " + str(min(generation['Fitness'])) + "\n\n")
    return gen


# TODO: Переделать, сделать настоящую GUI. Вынести рисование графиков в отдельную функцию


# TODO: Необходимо для этой проги вывоводить 3 функции: мою, Дианы, Розенброка
if __name__ == '__main__':
    # main(50, 20, 2, -1, -1)
    app = QtWidgets.QApplication(sys.argv)
    window = test.MyWindow()
    window.draw_figure(run(50, 20, 2, -1, -1))
    window.show()
    sys.exit(app.exec_())
