import pygame as pg
import numpy as np

EPSILON = 1e-11
SHIFT_EPSILON = EPSILON * 100000


def makeColor(name):
    pyColor = pg.Color(name)
    # Convert from 255 to 1.0 colors
    return np.array(pyColor[:-1]) / 255


def safeMultiply(self, vector, multiplier):
    newVector = vector * multiplier
    for index in range(len(newVector)):
        self[index] = max(0, min(1.0, newVector[index]))
    return newVector


COLORS = {
    "blue": makeColor("blue"),
    "white": makeColor("white"),
    "black": makeColor("black"),
    "red": makeColor("red"),
    "yellow": makeColor("yellow"),
    "marble1": makeColor("seagreen1"),
    "marble2": makeColor("seagreen4"),
    "wood1": makeColor("sienna1"),
    "wood2": makeColor("sienna4"),
    "gray": makeColor("gray")
}
