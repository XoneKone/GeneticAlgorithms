import sys

import numpy
from PyQt5 import QtWidgets
from matplotlib import pyplot as plt, cm, animation

from GenAlgo import main
import GenAlgo.bees.main as bees
from GenAlgo import gui, settings, constants
from GenAlgo.test_functions import TestFunctions


def plot(name: str, function, points: list[numpy.ndarray]):
    """
    Строит заданную функцию и выводит точки
    :param name: подпись графика
    :param function: функция вида z = f(x, y)
    :param points: список точек по поколениям, итерациям и т.д.
    :return:
    """
    X = numpy.arange(-2, 2, 0.1)
    Y = numpy.arange(-3, 3, 0.1)
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
    

class AlgorithmLauncher:
    def launch(self, window: gui.MyWindow):
        selected_algorithm = window.get_selected_algorithm()
        if selected_algorithm == settings.GENETIC_ALGORITHM:
            self.genetic_algorithm(window)
            
        elif selected_algorithm == settings.BEES_ALGORITHM:
            self.bees_algorithm(window)

        #window.draw_figure(gen, generation_number)
        window.show()

    def get_selected_function(self):
        selected_function = window.get_selected_function()
        if selected_function == constants.ROSENBROCK:
            function = TestFunctions.rosenbrock_function
        elif selected_function == constants.KHVAN:
            function = TestFunctions.kkhvan_function
        else:
            function = TestFunctions.dshishkina_function

        return function
        
    def genetic_algorithm(self, window):
        gen = main.main(
            window.genetic_algorithm_get_number_of_generations(),
            window.genetic_algorithm_get_number_of_individuals(),
            1,
            -1
        )
        points = [generation['Individuals'] for generation in gen]
        plot('Genetic algorithm', self.get_selected_function(), points)
        
    def bees_algorithm(self, window):
        bees.NUMBER_OF_SCOUT_BEES = window.bees_algorithm_get_number_of_scout_bees()
        bees.NUMBER_OF_ELITE_PLOTS = window.bees_algorithm_get_number_of_elite_plots()
        bees.NUMBER_OF_PERSPECTIVE_PLOTS = window.bees_algorithm_get_number_of_perspective_plots()
        bees.NUMBER_OF_BEES_ON_ELITE_PLOTS = window.bees_algorithm_get_number_of_bees_on_elite_plots()
        bees.NUMBER_OF_BEES_ON_PERSPECTIVE_PLOTS = window.bees_algorithm_get_number_of_bees_on_perspective_plots()
        bees.ELITE_PLOT_RADIUS = window.bees_algorithm_get_elite_plot_radius()
        bees.PERSPECTIVE_PLOT_RADIUS = window.bees_algorithm_get_perspective_plot_radius()

        function = self.get_selected_function()

        bees.fittest = lambda point: function(point[0], point[1])
        
        lower_bound = numpy.array([-5, -5])
        upper_bound = numpy.array([5, 5])
        _, points = bees.main(lower_bound, upper_bound, 50)

        plot("Bees algorithm", function, points)
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    launcher = AlgorithmLauncher()
    window = gui.MyWindow()
    window.set_algorithm_launcher(launcher)
    #  window.draw_figure(main())
    window.show()
    sys.exit(app.exec_())



