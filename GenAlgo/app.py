import sys

from PyQt5 import QtWidgets

import main
from GenAlgo import gui


class AlgorithmLauncher:
    def lauch(self, gui: gui.MyWindow):
        fig = main.main(
            gui.get_number_of_generations(),
            gui.get_number_of_individuals(),
            gui.get_number_of_chromosomes(),
            -1,
            -1
        )
        gui.draw_figure(fig)
        gui.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = gui.MyWindow(AlgorithmLauncher())
    #window.draw_figure(main())
    window.show()
    sys.exit(app.exec_())



