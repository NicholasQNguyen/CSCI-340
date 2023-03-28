"""
Author: Liz Matthews
"""
import numpy as np
import random
from ..utils.vector import vec, lerp


def randomColor(u, v, uMaxIndex, vMaxIndex):
    return vec(random.random(), random.random(), random.random())


def rainbowGradient(u, v, uMaxIndex, vMaxIndex,
                    orientation="u", wrap=False):
    colors = [vec(1, 0, 0),
              vec(1, 1, 0),
              vec(0, 1, 0),
              vec(0, 1, 1),
              vec(0, 0, 1),
              vec(1, 0, 1)]
    if wrap:
        colors.append(colors[0])
    percentU = u / uMaxIndex
    percentV = v / vMaxIndex
    percentU *= len(colors) - 1
    percentV *= len(colors) - 1
    start = int(np.floor(percentU))
    end = min(u + 1, 5)
    if orientation == "u":
        return lerp(colors[start], colors[end], percentU - u)
    else:
        return lerp(colors[start], colors[end], percentU - v)
        
