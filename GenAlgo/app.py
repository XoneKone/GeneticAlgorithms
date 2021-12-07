import sys

import numpy
from PyQt5 import QtWidgets
from matplotlib import pyplot as plt, cm, animation

import main
import bees.main as bees
from GenAlgo import gui, settings, constants
from GenAlgo.test_functions import TestFunctions


class AlgorithmLauncher:
    def launch(self, window: gui.MyWindow):
        selected_algorithm = window.get_selected_algorithm()
        if selected_algorithm == settings.GENETIC_ALGORITHM:
            self.genetic_algorithm(window)
            
        elif selected_algorithm == settings.BEES_ALGORITHM:
            self.bees_algorithm(window)

        #window.draw_figure(gen, generation_number)
        window.show()
        
    def genetic_algorithm(self, window):
        main.task = window.get_selected_mode()
        gen, generation_number = main.main(
            window.get_number_of_generations(),
            window.get_number_of_individuals(),
            1,
            -1
        )
        
    def bees_algorithm(self, window):
        bees.NUMBER_OF_SCOUT_BEES = window.bees_algorithm_get_number_of_scout_bees()
        bees.NUMBER_OF_ELITE_PLOTS = window.bees_algorithm_get_number_of_elite_plots()
        bees.NUMBER_OF_PERSPECTIVE_PLOTS = window.bees_algorithm_get_number_of_perspective_plots()
        bees.NUMBER_OF_BEES_ON_ELITE_PLOTS = window.bees_algorithm_get_number_of_bees_on_elite_plots()
        bees.NUMBER_OF_BEES_ON_PERSPECTIVE_PLOTS = window.bees_algorithm_get_number_of_bees_on_perspective_plots()
        bees.ELITE_PLOT_RADIUS = window.bees_algorithm_get_elite_plot_radius()
        bees.PERSPECTIVE_PLOT_RADIUS = window.bees_algorithm_get_perspective_plot_radius()

        selected_function = window.get_selected_function()
        if selected_function == constants.ROSENBROCK:
            function = TestFunctions.rosenbrock_function
        elif selected_function == constants.KHVAN:
            function = TestFunctions.kkhvan_function
        else:
            function = TestFunctions.dshishkina_function

        bees.fittest = lambda point: -function(point[0], point[1])
        
        lower_bound = numpy.array([-5, -5])
        upper_bound = numpy.array([5, 5])
        _, iterator = bees.main(lower_bound, upper_bound, 50)

        X = numpy.arange(-2, 2, 0.1)
        Y = numpy.arange(-3, 3, 0.1)
        X, Y = numpy.meshgrid(X, Y)

        Z = function(X, Y)
        fig = plt.figure(figsize=(6, 6), num='GA animation')

        ax = fig.add_subplot(projection='3d')
        ax.view_init(45, 45)
        surf = ax.plot_surface(X, Y, Z, cmap=cm.Spectral,
                               linewidth=0, antialiased=True, alpha=0.6)

        title = ax.set_title('GA-optimizer plot')

        def update_graph(num):
            df = {
                'x': numpy.array([point[0] for point in iterator[num]]),
                'y': numpy.array([point[1] for point in iterator[num]]),
                'f(x, y)': numpy.array([function(point[0], point[1]) for point in iterator[num]])
            }
            graph.set_data(df['x'], df['y'])
            graph.set_3d_properties(df['f(x, y)'])
            title.set_text('iteration={}'.format(num + 1))

            return title, graph,

        df = {
            'x': numpy.array([point[0] for point in iterator[0]]),
            'y': numpy.array([point[1] for point in iterator[0]]),
            'f(x, y)': numpy.array([function(point[0], point[1]) for point in iterator[0]])
        }
        graph, = ax.plot(numpy.array(df['x']), numpy.array(df['y']), numpy.array(df['f(x, y)']),
                         linestyle="", c='black', marker='2', ms=2)
        surf = ax.plot_surface(X, Y, Z, cmap=cm.Spectral, linewidth=0, antialiased=True, alpha=0.6)
        anim = animation.FuncAnimation(
            fig, update_graph, len(iterator), interval=100, save_count=True)
        #
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        window.draw_plot(fig, anim)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    launcher = AlgorithmLauncher()
    window = gui.MyWindow()
    window.set_algorithm_launcher(launcher)
    #  window.draw_figure(main())
    window.show()
    sys.exit(app.exec_())



