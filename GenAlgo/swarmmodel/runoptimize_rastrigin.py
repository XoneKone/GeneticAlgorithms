#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
from matplotlib import cm, pyplot as plt, animation

from swarmmodel.swarm_rastrigin import Swarm_Rastrigin
from swarmmodel.utils import printResult
from test_functions import TestFunctions
import numpy


def run(iterCount=1000,
        eps=0.0001,
        dimension=2,
        swarmsize=500,
        currentVelocityRatio=0.5,
        localVelocityRatio=2.0,
        globalVelocityRatio=5.0):
    minvalues = numpy.array([-5.12] * dimension)
    maxvalues = numpy.array([5.12] * dimension)

    swarm = Swarm_Rastrigin(swarmsize,
                            minvalues,
                            maxvalues,
                            currentVelocityRatio,
                            localVelocityRatio,
                            globalVelocityRatio
                            )
    fitness_values = [swarm.globalBestFinalFunc]
    best_positions = [swarm.get_swarm()]
    result_print = []
    print(printResult(swarm, 0))
    similarty = 0
    for n in range(1, iterCount):

        result_print.append(printResult(swarm, n))

        swarm.nextIteration()
        best_positions.append(swarm.get_swarm())
        fitness_values.append(swarm.globalBestFinalFunc)
        print(printResult(swarm, n))

        if abs(fitness_values[-1] - fitness_values[-2]) <= eps:
            similarty += 1
        else:
            similarty = 0
        if similarty == 3 :
            break

    return best_positions, result_print


if __name__ == '__main__':
    best_positions, result_print = run()
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
    plt.show()
