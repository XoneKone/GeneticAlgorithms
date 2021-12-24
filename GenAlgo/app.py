import sys

import numpy
from PyQt5 import QtWidgets
from matplotlib import pyplot as plt, cm, animation

import bees.main as bees
import artificial_immune_system.main as ais
import constants
import gui
import genetic_algo
import settings
from swarmmodel import runoptimize_rastrigin
from test_functions import TestFunctions


def plot(name: str, function, points):
    """
    Строит заданную функцию и выводит точки
    :param name: подпись графика
    :param function: функция вида z = f(x, y)
    :param points: список точек по поколениям, итерациям и т.д.
    :return:
    """
    lower_bound = AlgorithmLauncher.lower_bound
    upper_bound = AlgorithmLauncher.upper_bound
    X = numpy.arange(lower_bound[0], upper_bound[0], 0.1)
    Y = numpy.arange(lower_bound[1], upper_bound[1], 0.1)
    X, Y = numpy.meshgrid(X, Y)

    Z = function(X, Y)
    fig = plt.figure(figsize=(6, 6), num=name)
    fig.clf()

    ax = fig.add_subplot(projection='3d')
    ax.view_init(45, 45)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.Spectral,
                           linewidth=0, antialiased=True, alpha=0.6)

    title = ax.set_title(name)

    def update_graph(num):
        df = {
            'x': numpy.array([point[0] for point in points[num]]),
            'y': numpy.array([point[1] for point in points[num]]),
            'f(x, y)': numpy.array([function(point[0], point[1]) for point in points[num]])
        }
        graph.set_data(df['x'], df['y'])
        graph.set_3d_properties(df['f(x, y)'])
        title.set_text('iteration={}'.format(num + 1))

        return title, graph,

    df = {
        'x': numpy.array([point[0] for point in points[0]]),
        'y': numpy.array([point[1] for point in points[0]]),

        'f(x, y)': numpy.array([function(point[0], point[1]) for point in points[0]])
    }
    graph, = ax.plot(numpy.array(df['x']), numpy.array(df['y']), numpy.array(df['f(x, y)']),
                     linestyle="", c='black', marker='2', ms=2)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.Spectral, linewidth=0, antialiased=True, alpha=0.6)
    anim = animation.FuncAnimation(
        fig, update_graph, len(points), interval=100, save_count=True)
    #
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    window.draw_plot(fig, anim)


def plot_rastrigin(params):
    """

    :param params: [iterCount, eps, dimension,swarmsize,currentVelocityRatio,localVelocityRatio,globalVelocityRatio]
    :return:
    """
    best_positions, result_print = runoptimize_rastrigin.run(*params) # Во второй переменной хранится строка для вывода инфы
    X = numpy.arange(-5.12, 5.12, 0.01)
    Y = numpy.arange(-5.12, 5.12, 0.01)

    X, Y = numpy.meshgrid(X, Y)

    Z = TestFunctions.rastrigin(X, Y, 2)
    fig = plt.figure(figsize=(6, 6), num="pso")
    fig.clf()

    ax = fig.add_subplot(projection='3d')
    ax.view_init(45, 45)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.Spectral,
                           linewidth=0, antialiased=True, alpha=0.6)

    title = ax.set_title("pso")

    def update_graph(num):
        df = {
            'x': numpy.array([point[0][0] for point in best_positions[num]]),
            'y': numpy.array([point[0][1] for point in best_positions[num]]),
            'f(x, y)': numpy.array([point[1] for point in best_positions[num]])
        }
        graph.set_data(df['x'], df['y'])
        graph.set_3d_properties(df['f(x, y)'])
        title.set_text('iteration={}'.format(num + 1))

        return title, graph,

    df = {
        'x': numpy.array([point[0][0] for point in best_positions[0]]),
        'y': numpy.array([point[0][1] for point in best_positions[0]]),
        'f(x, y)': numpy.array([point[1] for point in best_positions[0]])
    }
    graph, = ax.plot(numpy.array(df['x']), numpy.array(df['y']), numpy.array(df['f(x, y)']),
                     linestyle="", c='black', marker='2', ms=2)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.Spectral, linewidth=0, antialiased=True, alpha=0.6)
    anim = animation.FuncAnimation(
        fig, update_graph, len(best_positions), interval=100, save_count=True)
    #
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    window.output_text(result_print)
    window.draw_plot(fig, anim)


class AlgorithmLauncher:

    def launch(self, window: gui.MyWindow):
        selected_algorithm = window.get_selected_algorithm()
        if selected_algorithm == settings.GENETIC_ALGORITHM:
            self.genetic_algorithm(window)

        elif selected_algorithm == settings.BEES_ALGORITHM:
            self.bees_algorithm(window)

        elif selected_algorithm == settings.SWARM_ALGORITHM:
            self.swarm_algorithm(window)

        elif selected_algorithm == settings.ARTIFICIAL_IMMUNE_SYSTEM:
            self.ais_algorithm(window)

        # window.draw_figure(gen, generation_number)
        window.show()

    def get_selected_function(self):
        selected_function = window.get_selected_function()
        if selected_function == constants.ROSENBROCK:
            mode = -1
            function = TestFunctions.rosenbrock_function
        elif selected_function == constants.KHVAN:
            mode = 1
            function = TestFunctions.kkhvan_function
        elif selected_function == constants.HIMMELBLAU:
            mode = -1
            function = TestFunctions.himmelblau_function
        elif selected_function == constants.RASTRIGIN:
            mode = -1
            function = TestFunctions.rastrigin
        else:
            mode = 1
            function = TestFunctions.dshishkina_function

        return function, mode

    def genetic_algorithm(self, window):
        gen = genetic_algo.run(
            window.genetic_algorithm_get_number_of_generations(),
            window.genetic_algorithm_get_number_of_individuals(),
            2,
            -2,
            task=self.get_selected_function()[1]
        )
        points = [generation['Individuals'] for generation in gen]
        window.show_output(gen, None)
        plot('Genetic algorithm', self.get_selected_function()[0], points)

    def swarm_algorithm(self, window):
        plot_rastrigin(
            [
                window.swarm_get_iter_count(),
                window.swarm_get_eps(),
                window.swarm_get_dimension(),
                window.swarm_get_swarm_size(),
                window.swarm_get_current_velocity_ratio(),
                window.swarm_get_local_velocity_ratio(),
                window.swarm_get_global_velocity_ratio(),
            ]
        )

    def bees_algorithm(self, window):
        bees.NUMBER_OF_SCOUT_BEES = window.bees_algorithm_get_number_of_scout_bees()
        bees.NUMBER_OF_ELITE_PLOTS = window.bees_algorithm_get_number_of_elite_plots()
        bees.NUMBER_OF_PERSPECTIVE_PLOTS = window.bees_algorithm_get_number_of_perspective_plots()
        bees.NUMBER_OF_BEES_ON_ELITE_PLOTS = window.bees_algorithm_get_number_of_bees_on_elite_plots()
        bees.NUMBER_OF_BEES_ON_PERSPECTIVE_PLOTS = window.bees_algorithm_get_number_of_bees_on_perspective_plots()
        bees.ELITE_PLOT_RADIUS = window.bees_algorithm_get_elite_plot_radius()
        bees.PERSPECTIVE_PLOT_RADIUS = window.bees_algorithm_get_perspective_plot_radius()

        function, mode = self.get_selected_function()

        bees.fittest = lambda point: mode * function(point[0], point[1])

        lower_bound = numpy.array([*self.lower_bound])
        upper_bound = numpy.array([*self.upper_bound])
        _, iterations = bees.main(lower_bound, upper_bound, 50)
        points = [iteration['Individuals'] for iteration in iterations]
        better_points = [max(iteration['Individuals'], key=lambda x: bees.fittest(x)) for iteration in iterations]

        if mode == -1:
            for iteration in iterations:
                iteration['Fitness'] = [-1 * f for f in iteration['Fitness']]
            better = [(point, -1 * bees.fittest(point)) for point in better_points]

        else:
            better = [(point, bees.fittest(point)) for point in better_points]

        window.show_output(iterations, better)
        plot("Bees algorithm", function, points)

    def ais_algorithm(self, window):
        ais.ANTIBODIES_NUMBER = window.ais_get_number_of_antibodies()
        ais.CLONES_NUMBER = window.ais_get_number_of_clones()
        ais.MUTATION_RATIO = window.ais_get_mutation_ratio()
        ais.THRESHOLD_COMPRESSION_RATIO = window.ais_get_threshold_compression_ratio()

        function, mode = self.get_selected_function()

        ais.fittest = lambda point: mode * function(point[0], point[1])

        lower_bound = numpy.array([*self.lower_bound])
        upper_bound = numpy.array([*self.upper_bound])
        _, iterations = ais.main(lower_bound, upper_bound, 50)
        points = [iteration['Individuals'] for iteration in iterations]
        better_points = [max(iteration['Individuals'], key=lambda x: ais.fittest(x)) for iteration in iterations]

        if mode == -1:
            for iteration in iterations:
                iteration['Fitness'] = [-1 * f for f in iteration['Fitness']]
            better = [(point, -1 * ais.fittest(point)) for point in better_points]

        else:
            better = [(point, ais.fittest(point)) for point in better_points]

        window.show_output(iterations, better)
        plot("AIS algorithm", function, points)

    def swarm_particles(self, window):
        # TODO: Сделать тут обработчик значений
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    launcher = AlgorithmLauncher()
    window = gui.MyWindow()
    window.set_algorithm_launcher(launcher)
    #  window.draw_figure(main())
    window.show()
    sys.exit(app.exec_())
