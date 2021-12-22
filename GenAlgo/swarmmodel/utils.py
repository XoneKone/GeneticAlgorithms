#!/usr/bin/python
# -*- coding: UTF-8 -*-

def printResult(swarm, iteration):
    template = u"""Iteration: {iter}

Best Position: {bestpos}
Best Final Func: {finalfunc}
----------------------------
"""

    result = template.format(iter=iteration,
                             bestpos=swarm.globalBestPosition,
                             finalfunc=swarm.globalBestFinalFunc)


    return result
