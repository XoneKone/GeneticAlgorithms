import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets, uic

import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox, QRadioButton, QButtonGroup, QPushButton

matplotlib.use('QT5Agg')

import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import constants


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, task):
        super(MyWindow, self).__init__()
        uic.loadUi('gui.ui', self)

        self.task = task
        self.functions = QButtonGroup()
        self.functions.addButton(self.khvan, constants.KHVAN)
        self.functions.addButton(self.shishkina, constants.SHISHKINA)
        self.functions.addButton(self.rosenbrock, constants.ROSENBROCK)

        launch_button: QPushButton = self.lauch_button
        launch_button.clicked.connect(lambda: self.task.lauch(self))

        self.plotWidget = FigureCanvas()
        self.lay = QtWidgets.QHBoxLayout(self.content_plot)
        self.content_plot.layout().addWidget(self.plotWidget)
        self.addToolBar(Qt.BottomToolBarArea, NavigationToolbar(self.plotWidget, self))
        # self.lay = QtWidgets.QHBoxLayout(self.content_plot)
        # self.lay.addWidget(QtWidgets.QFrame())
        # self.content_plot.layout().addWidget(self.plotWidget)
        # self.addToolBar(Qt.BottomToolBarArea, NavigationToolbar(self.plotWidget, self))

    def draw_figure(self, fig: plt.Figure):
        self.plotWidget.figure.axes.clear()
        #self.plotWidget.figure.canvas = None
        fig.subfigs.clear()
#        self.plotWidget.figure.clear()

        self.plotWidget.figure = fig
        fig.set_canvas(self.plotWidget)
        self.plotWidget.draw()


    def get_number_of_chromosomes(self):
        number_of_chromosomes: QSpinBox = self.number_of_chromosomes
        return int(number_of_chromosomes.text())

    def get_number_of_individuals(self):
        number_of_individuals: QSpinBox = self.number_of_individuals
        return int(number_of_individuals.text())

    def get_number_of_generations(self):
        number_of_generations: QSpinBox = self.number_of_generations
        return int(number_of_generations.text())

    def get_checked_function(self):
        return self.functions.checkedId()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())