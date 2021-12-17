import sys
import numpy as np

from PyQt5 import QtWidgets, uic

import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox, QButtonGroup, QPushButton, QPlainTextEdit, QTabWidget, QTextBrowser
from matplotlib import animation, cm

from GenAlgo.test_functions import TestFunctions

matplotlib.use('QT5Agg')

import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from GenAlgo import constants


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('GenAlgo/gui.ui', self)

        self.functions = QButtonGroup()
        self.functions.addButton(self.khvan, constants.KHVAN)
        self.functions.addButton(self.shishkina, constants.SHISHKINA)
        self.functions.addButton(self.rosenbrock, constants.ROSENBROCK)

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

    def show_output(self, points_by_iterations):
        output: QTextBrowser = self.output
        output.clear()

        for i, iteration in enumerate(points_by_iterations):
            points_str = [
                '{} fitness: {:.3f}'.format(point, fitness)
                for point, fitness in zip(iteration['Individuals'], iteration['Fitness'])
            ]
            output.append('Итерация {}\n{}\n'.format(i + 1, '\n'.join(points_str)))

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
        return float(self.elite_plot_radius.text())

    def bees_algorithm_get_perspective_plot_radius(self):
        return float(self.perspective_plot_radius.text())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
