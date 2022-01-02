import numpy

from bees.main import Point

ANTIGENS_NUMBER = 0
CLONES_NUMBER = 0
MUTATION_RATIO = 0
THRESHOLD_COMPRESSION_RATIO = 0

ANTIBODIES_NUMBER = 0
BEST_ANTIGENS_NUMBER = 0
BEST_ANTIBODIES_NUMBER = 0
SELECTION_RATIO = 0


fittest = None


def random_in_bounds(lower_bound: Point, upper_bound: Point, number: int):
    return [
        numpy.array([numpy.random.uniform(low, up) for low, up in zip(lower_bound, upper_bound)])
        for _ in range(number)
    ]


def mutation(point: Point):
    mutated = []
    for p in point:
        rate = numpy.random.uniform()
        if rate < MUTATION_RATIO:
            mutated.append(p + numpy.random.uniform(-0.5, 0.5))
        else:
            mutated.append(p)
    return numpy.array(mutated)


def next_iteration(antibodies):
    best_antibodies = sorted(antibodies, key=fittest, reverse=True)[:BEST_ANTIBODIES_NUMBER]
    clones = []
    for antibody in best_antibodies:
        clones.extend([antibody] * CLONES_NUMBER)

    mutated = sorted([mutation(clone) for clone in clones], key=fittest, reverse=True)
    threshold = slice(int(THRESHOLD_COMPRESSION_RATIO * len(mutated)))
    union = antibodies + mutated[threshold]
    return sorted(union, key=fittest, reverse=True)[:ANTIBODIES_NUMBER]

# def next_iteration(antibodies):
#     new_population = []
#     for antibody in antibodies:
#         clones = [antibody] * CLONES_NUMBER
#         mutated = [mutation(clone) for clone in clones]
#         max_mutated = max(mutated, key=fittest)
#         if fittest(max_mutated) > fittest(antibody):
#             new_population.append(max_mutated)
#         else:
#             new_population.append(antibody)
#
#     for i, antibody in enumerate(new_population):
#         for j, another_antibody in enumerate(new_population):
#             if antibody is not another_antibody:
#                 if numpy.linalg.norm(antibody - another_antibody) > THRESHOLD_COMPRESSION_RATIO:
#                     if fittest(antibody) > fittest(another_antibody):
#                         del new_population[j]
#                     else:
#                         del new_population[i]
#
#     return new_population


def in_bounds(point: Point, lower_bound: Point, upper_bound: Point):
    return all(
        low <= coordinate <= up for coordinate, low, up in zip(point, lower_bound, upper_bound)
    )


def main(lower_bound: Point, upper_bound: Point, number_of_iterations):
    antibodies = random_in_bounds(lower_bound, upper_bound, ANTIBODIES_NUMBER)
    previous_fitness = [fittest(antibody) for antibody in antibodies]
    history = [{'Individuals': antibodies, 'Fitness': previous_fitness}]
    num = 0
    for _ in range(number_of_iterations):
        new_population = next_iteration(antibodies)
        #  delete points which out bounds
        filtered = list(filter(lambda point: in_bounds(point, lower_bound, upper_bound), new_population))

        filtered.extend(random_in_bounds(lower_bound, upper_bound, ANTIBODIES_NUMBER - len(filtered)))
        filtered_fitness = [fittest(antibody) for antibody in filtered]
        if filtered_fitness and max(filtered_fitness) <= max(previous_fitness):
            num += 1
        else:
            num = 0

        if not filtered or num >= 3:
            break

        history.append({'Individuals': filtered, 'Fitness': filtered_fitness})
        antibodies = filtered
        previous_fitness = filtered_fitness
    return antibodies, history
