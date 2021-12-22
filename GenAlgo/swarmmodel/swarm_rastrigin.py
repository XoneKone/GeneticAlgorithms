#!/usr/bin/python
# -*- coding: UTF-8 -*-

from swarm import Swarm

import numpy


class Swarm_Rastrigin(Swarm):
    def __init__(self,
                 swarmsize,
                 minvalues,
                 maxvalues,
                 currentVelocityRatio,
                 localVelocityRatio,
                 globalVelocityRatio):
        Swarm.__init__(self,
                       swarmsize,
                       minvalues,
                       maxvalues,
                       currentVelocityRatio,
                       localVelocityRatio,
                       globalVelocityRatio)

    def _finalFunc(self, position):
        function = 10.0 * len(self.minvalues) + sum(position * position - 10.0 * numpy.cos(2 * numpy.pi * position))
        penalty = self._getPenalty(position, 10000.0)

        return function + penalty
