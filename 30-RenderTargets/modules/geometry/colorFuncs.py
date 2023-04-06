"""
Author: Liz Matthews
"""

from ..utils.vector import vec, lerp, smerp
from ..utils.definitions import makeColor
import numpy as np
import random


def randomColor(u, v, uMaxIndex, vMaxIndex):
    return vec(random.random(), random.random(), random.random())


def rainbowGradient(uIndex, vIndex, uMaxIndex=1, vMaxIndex=1, orientation="v", wrap=True):
    colors = [vec(1,0,0), vec(1,1,0), vec(0,1,0),
              vec(0,1,1), vec(0,0,1), vec(1,0,1)]
    
    if wrap:
        colors.append(colors[0])
    
    if orientation == "u":
        percent = uIndex / uMaxIndex
    else:
        percent = vIndex / vMaxIndex
    
    scaledI = percent * (len(colors) - 1)
    frac  = float(scaledI - np.floor(scaledI))
    start = int(np.floor(scaledI))
    end   = start + 1
    
    return lerp(colors[start], colors[end], frac)
  