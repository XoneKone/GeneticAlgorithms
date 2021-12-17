import numpy

from GenAlgo.bees.main import Point

ANTIGENS_NUMBER = 0
ANTIBODIES_NUMBER = 0
BEST_ANTIGENS_NUMBER = 0
BEST_ANTIBODIES_NUMBER = 0
CLONES_NUMBER = 0
MUTATION_RATE = 0
SELECTION_RATE = 0
COMPRESSION_RATE = 0

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
        if rate > MUTATION_RATE:
            mutated.append(p + numpy.random.uniform(-0.5, 0.5))
    return numpy.array(mutated)


def next_iteration(antibodies):
    best_antibodies = sorted(antibodies, key=fittest, reverse=True)[BEST_ANTIBODIES_NUMBER]
    clones = []
    for antibody in best_antibodies:
        clones.extend([antibody[0]] * CLONES_NUMBER)

    mutated = sorted([mutation(clone) for clone in clones], key=fittest, reverse=True)[SELECTION_RATE]
    union = antibodies + mutated
    return sorted(union, key=fittest, reverse=True)[COMPRESSION_RATE]


def in_bounds(point: Point, lower_bound: Point, upper_bound: Point):
    return all(
        low <= coordinate <= up for coordinate, low, up in zip(point, lower_bound, upper_bound)
    )


def main(lower_bound: Point, upper_bound: Point, number_of_iterations):
    #antigens = random_in_bounds(ANTIGENS_NUMBER)
    antibodies = random_in_bounds(ANTIBODIES_NUMBER)
    history_plots = [antibodies]
    for _ in range(number_of_iterations):
        new_antibodies = next_iteration(antibodies)
        #  delete points which out bounds
        filtered = list(filter(lambda point: in_bounds(point, lower_bound, upper_bound), new_antibodies))
        current_max = fittest(max(filtered, key=fittest))
        previous_max = fittest(max(history_plots[-1], key=fittest))
        if not filtered or current_max <= previous_max:
            break

        history_plots.append(filtered)
        antibodies = new_antibodies
    return antibodies, history_plots
