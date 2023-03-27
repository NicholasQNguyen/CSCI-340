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
    colors = [(1, 0, 0),
              (1, 1, 0),
              (0, 1, 0),
              (0, 1, 1),
              (0, 0, 1),
              (1, 0, 1)]
    percentU = u / uMaxIndex
    percentV = v / vMaxIndex
    percentU *= len(colors) - 1
    percentV *= len(colors) - 1
    if orientation == "u":
        return lerp(np.floor(percentU), u + 1, percentU - u)
    else:
        return lerp(np.floor(percentU), v + 1, percentU - v)
        
