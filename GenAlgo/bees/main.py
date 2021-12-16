import numpy
from numpy import ndarray

NUMBER_OF_SCOUT_BEES = 0
NUMBER_OF_ELITE_PLOTS = 0
NUMBER_OF_PERSPECTIVE_PLOTS = 0
NUMBER_OF_BEES_ON_ELITE_PLOTS = 0
NUMBER_OF_BEES_ON_PERSPECTIVE_PLOTS = 0
ELITE_PLOT_RADIUS = 0
PERSPECTIVE_PLOT_RADIUS = 0

Point = ndarray

fittest = None


def go_to_slot(lower_bound: Point, upper_bound: Point, number_of_bees: int):
    p = [
        numpy.array([numpy.random.uniform(low, up) for low, up in zip(lower_bound, upper_bound)])
        for _ in range(number_of_bees)
    ]
    return p


def next_iteration(plots):
    sorted_by_fitness = sorted(plots, key=fittest)
    elite_plots = sorted_by_fitness[:NUMBER_OF_ELITE_PLOTS]
    perspective_plots = sorted_by_fitness[NUMBER_OF_ELITE_PLOTS:NUMBER_OF_ELITE_PLOTS + NUMBER_OF_PERSPECTIVE_PLOTS]
    new_plots = []
    for plot in elite_plots:
        new_plots.extend(go_to_slot(
            plot - ELITE_PLOT_RADIUS,
            plot + ELITE_PLOT_RADIUS,
            NUMBER_OF_BEES_ON_ELITE_PLOTS),
        )

    for plot in perspective_plots:
        new_plots.extend(go_to_slot(
            plot - PERSPECTIVE_PLOT_RADIUS,
            plot + PERSPECTIVE_PLOT_RADIUS,
            NUMBER_OF_BEES_ON_PERSPECTIVE_PLOTS),
        )

    return new_plots


def in_bounds(point: Point, lower_bound: Point, upper_bound: Point):
    return all(
        low <= coordinate <= up for coordinate, low, up in zip(point, lower_bound, upper_bound)
    )


def main(lower_bound: Point, upper_bound: Point, number_of_iterations):
    plots = go_to_slot(lower_bound, upper_bound, NUMBER_OF_SCOUT_BEES)
    history_plots = [plots]
    for _ in range(number_of_iterations):
        new_plots = next_iteration(plots)
        #  delete points which out bounds
        filtered = list(filter(lambda point: in_bounds(point, lower_bound, upper_bound), new_plots))
        if not filtered:
            break

        history_plots.append(filtered)
        plots = new_plots
    return plots, history_plots
