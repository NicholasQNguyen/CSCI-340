from render import ProgressiveRenderer, ShowTypes
from modules.utils.noise import NoisePatterns
from modules.utils.vector import lerp, smerp
import numpy as np
import pygame
import random


class RandomRenderer(ProgressiveRenderer):
    def __init__(self, width=640, height=480,
                 showTime=True,
                 show=ShowTypes.PerColumn,
                 minimumPixel=0,
                 startPixelSize=256):
        """An unnecessary override but provided to show how
        to override the __init__ in future inheritance classes."""
        super().__init__(width, height,
                         showTime,
                         show,
                         minimumPixel,
                         startPixelSize)

    def getColor(self, x, y):
        """Gives a random color per pixel."""
        return np.array((random.random(),
                         random.random(),
                         random.random()))

    def handleOtherInput(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            type(self).restart()


class RainbowRenderer(ProgressiveRenderer):
    def __init__(self, width=640, height=480,
                 showTime=True,
                 show=ShowTypes.PerColumn,
                 minimumPixel=0,
                 startPixelSize=256):
        """An unnecessary override but provided to show how
        to override the __init__ in future inheritance classes."""
        super().__init__(width, height,
                         showTime,
                         show,
                         minimumPixel,
                         startPixelSize)
        self.functionsList = [self.hPercent,
                              self.vPercent,
                              self.hundredMinusHPercent,
                              self.hundredMinusVPercent]
        self.rFunc = 0
        self.gFunc = 1
        self.bFunc = 2

    def hPercent(self, x):
        return x / self.width

    def vPercent(self, y):
        return y / self.height

    def hundredMinusHPercent(self, x):
        return 1.0 - self.hPercent(x)

    def hundredMinusVPercent(self, y):
        return 1.0 - self.vPercent(y)

    def callFunc(self, index, x, y):
        # If hori func, then use x
        if index % 2 == 0:
            return self.functionsList[index % 4](x)
        else:
            return self.functionsList[index % 4](y)

    def getColor(self, x, y):
        """Gives a random color per pixel."""
        return np.array((self.callFunc(self.rFunc, x, y),
                         self.callFunc(self.gFunc, x, y),
                         self.callFunc(self.bFunc, x, y)))

    def handleOtherInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.rFunc += 1
            elif event.key == pygame.K_2:
                self.gFunc += 1
            elif event.key == pygame.K_3:
                self.bFunc += 1
            else:
                return None
            # Reset only if one of 1, 2, or 3 was hit
            type(self).restart()


# Calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        RainbowRenderer.main()
    finally:
        pygame.quit()
