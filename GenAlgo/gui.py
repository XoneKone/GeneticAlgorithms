import sys
import numpy as np

from PyQt5 import QtWidgets, uic

import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox, QButtonGroup, QPushButton, QPlainTextEdit, QTabWidget, QTextBrowser
from matplotlib import animation, cm
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import constants
from test_functions import TestFunctions

matplotlib.use('QT5Agg')


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('gui.ui', self)

        self.functions = QButtonGroup()
        self.functions.addButton(self.khvan, constants.KHVAN)
        self.functions.addButton(self.shishkina, constants.SHISHKINA)
        self.functions.addButton(self.rosenbrock, constants.ROSENBROCK)
        self.functions.addButton(self.himmelblau, constants.HIMMELBLAU)
        self.functions.addButton(self.rastrigin, constants.RASTRIGIN)

        self.plotWidget = FigureCanvas()
        self.lay = QtWidgets.QHBoxLayout(self.content_plot)
        self.content_plot.layout().addWidget(self.plotWidget)
        self.addToolBar(Qt.BottomToolBarArea, NavigationToolbar(self.plotWidget, self))

        self.fig = None
        self.anim = None

    def set_algorithm_launcher(self, launcher):
        self.lauch_button.clicked.connect(lambda: launcher.launch(self))

    def build(self, generations, generations_number):
        X = np.arange(-2, 2, 0.1)
        Y = np.arange(-3, 3, 0.1)
        X, Y = np.meshgrid(X, Y)

        if self.get_selected_mode() == constants.ROSENBROCK:
            Z = TestFunctions.rosenbrock_function(X, Y)
        elif self.get_selected_mode() == constants.KHVAN:
            Z = TestFunctions.kkhvan_function(X, Y)
        else:
            Z = TestFunctions.dshishkina_function(X, Y)

        fig = plt.figure(figsize=(6, 6), num='GA animation')

        ax = fig.add_subplot(projection='3d')
        ax.view_init(45, 45)
        surf = ax.plot_surface(X, Y, Z, cmap=cm.Spectral,
                               linewidth=0, antialiased=True, alpha=0.6)

        title = ax.set_title('GA-optimizer plot')

        def update_graph(num):
            df = {
                'x': np.array([i[0] for i in generations[num]['Individuals']]),
                'y': np.array([i[1] for i in generations[num]['Individuals']]),
                'f(x, y)': np.array([i for i in generations[num]['Fitness']])
            }
            graph.set_data(df['x'], df['y'])
            graph.set_3d_properties(df['f(x, y)'])
            title.set_text('generation={}'.format(num + 1))

            return title, graph,

        df = {
            'x': np.array([i[0] for i in generations[0]['Individuals']]),
            'y': np.array([i[1] for i in generations[0]['Individuals']]),
            'f(x, y)': np.array([i for i in generations[0]['Fitness']])
        }
        graph, = ax.plot(np.array(df['x']), np.array(df['y']), np.array(df['f(x, y)']),
                         linestyle="", c='black', marker='2', ms=2)
        surf = ax.plot_surface(X, Y, Z, cmap=cm.Spectral, linewidth=0, antialiased=True, alpha=0.6)
        anim = animation.FuncAnimation(
            fig, update_graph, generations_number, interval=100, save_count=True)
        #
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # plt.show()
        self.fig = fig
        self.anim = anim

    def draw_plot(self, fig, anim):

        if self.anim:
            self.anim.__del__()

        self.fig = fig
        self.anim = anim
        self.plotWidget.figure = self.fig
        self.fig.set_canvas(self.plotWidget)
        self.plotWidget.draw()

    def draw_figure(self, gen, generation_number):
        if self.fig:
            self.fig.clf()
        if self.anim:
            self.anim.__del__()

        self.build(gen, generation_number)
        # self.plotWidget.figure.axes.clear()
        # fig.subfigs.clear()

        self.plotWidget.figure = self.fig
        self.fig.set_canvas(self.plotWidget)
        self.plotWidget.draw()

    def show_output(self, points_by_iterations, better_points):
        output: QTextBrowser = self.output
        output.clear()

        for i, iteration in enumerate(points_by_iterations):
            points_with_fitness = zip(iteration['Individuals'], iteration['Fitness'])
            point_format = '{} fitness: {:.3f}'
            points_str = [
                point_format.format(point, fitness)
                for point, fitness in points_with_fitness
            ]
            output.append('Итерация {}\n{}\n'.format(i + 1, '\n'.join(points_str)))
            if better_points is None:
                output.append(f'\nBest: {points_str[-1]}\n')
            else:
                better_point = point_format.format(better_points[i][0], better_points[i][1])
                output.append('\n{}\n'.format(better_point))

    def output_text(self, text):
        output: QTextBrowser = self.output
        output.clear()
        for string in text:
            output.append(string)

    def get_selected_function(self):
        return self.functions.checkedId()

    def get_selected_algorithm(self):
        return self.algorithms.currentIndex()

    #  get data for genetic algorithm
    def genetic_algorithm_get_number_of_individuals(self):
        return int(self.number_of_individuals.text())

    def genetic_algorithm_get_number_of_generations(self):
        return int(self.number_of_generations.text())

    # get data for bees algorithm
    def bees_algorithm_get_number_of_scout_bees(self):
        return int(self.number_of_scout_bees.text())

    def bees_algorithm_get_number_of_elite_plots(self):
        return int(self.number_of_elite_plots.text())

    def bees_algorithm_get_number_of_perspective_plots(self):
        return int(self.number_of_perspective_plots.text())

    def bees_algorithm_get_number_of_bees_on_elite_plots(self):
        return int(self.number_of_bees_on_elite_plots.text())

    def bees_algorithm_get_number_of_bees_on_perspective_plots(self):
        return int(self.number_of_bees_on_perspective_plots.text())

    def bees_algorithm_get_elite_plot_radius(self):
        return float(str(self.elite_plot_radius.text()).replace(',', '.'))

    def bees_algorithm_get_perspective_plot_radius(self):
        return float(str(self.perspective_plot_radius.text()).replace(',', '.'))

    # get data for swarm algorithm
    def swarm_get_iter_count(self):
        return int(self.number_of_iterations.text())

    def swarm_get_eps(self):
        return float(self.eps.text())

    def swarm_get_dimension(self):
        return int(self.dimension.text())

    def swarm_get_swarm_size(self):
        return int(self.swarm_size.text())

    def swarm_get_current_velocity_ratio(self):
        return float(self.current_velocity_ratio.text())

    def swarm_get_local_velocity_ratio(self):
        return float(self.local_velocity_ratio.text())

    def swarm_get_global_velocity_ratio(self):
        return float(self.global_velocity_ratio.text())

    # get data for ais algorithm
    def ais_get_number_of_antibodies(self):
        return int(self.number_of_antibodies.text())

    def ais_get_number_of_best_antibodies(self):
        return int(self.number_of_best_antibodies.text())

    def ais_get_number_of_clones(self):
        return int(self.number_of_clones.text())

    def ais_get_mutation_ratio(self):
        return float(self.mutation_ratio.text())

    def ais_get_threshold_compression_ratio(self):
        return float(self.threshold_compression_ratio.text())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
