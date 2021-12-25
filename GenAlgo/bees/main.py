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
    sorted_by_fitness = sorted(plots, key=fittest, reverse=True)[:NUMBER_OF_SCOUT_BEES]
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

    new_plots.extend(plots)
    return sorted(new_plots, key=fittest, reverse=True)[:NUMBER_OF_SCOUT_BEES]


def in_bounds(point: Point, lower_bound: Point, upper_bound: Point):
    return all(
        low <= coordinate <= up for coordinate, low, up in zip(point, lower_bound, upper_bound)
    )


def main(lower_bound: Point, upper_bound: Point, number_of_iterations):
    plots = go_to_slot(lower_bound, upper_bound, NUMBER_OF_SCOUT_BEES)
    previous_fitness = [fittest(plot) for plot in plots]
    history_plots = [{'Individuals': plots, 'Fitness': previous_fitness}]
    num = 0
    for _ in range(number_of_iterations):
        new_plots = next_iteration(plots)
        #  delete points which out bounds
        filtered = list(filter(lambda point: in_bounds(point, lower_bound, upper_bound), new_plots))
        filtered_fitness = [fittest(plot) for plot in filtered]
        if filtered_fitness and max(filtered_fitness) <= max(previous_fitness):
            num += 1
        else:
            num = 0

        if not filtered or num >= 3:
            break

        history_plots.append({'Individuals': filtered, 'Fitness': filtered_fitness})
        plots = new_plots
        previous_fitness = filtered_fitness
    return plots, history_plots
