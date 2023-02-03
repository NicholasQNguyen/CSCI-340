"""
Author: Liz Matthews, Geoff Matthews
"""
import numpy as np
import pygame

from render import ProgressiveRenderer, ShowTypes

from modules.raytracing.scene import Scene
from modules.utils.vector import vec, normalize

class RayTracer(ProgressiveRenderer):
    def __init__(self, width=800, height=600, show=ShowTypes.PerColumn):
        super().__init__(width, height, show=show)
        self.fog = vec(0.7,0.9,1.0)
        self.scene = Scene(aspect=width/height, fov=45)
        self.addObjects()

    def addObjects(self):
        self.scene.addSphere()
        self.scene.addPlane()

    def getColorR(self, ray):
        # Start with zero color
        color = np.zeros((3))

        # Normalize the ray
        nRay = normalize(ray)

        # Find any objects it collides with and calculate color
        for obj in self.scene.objects:
            pass

        # Return fog if doesn't hit anything
        return self.fog


    def getColor(self, x, y):
        # Calculate the percentages for x and y
        xPercent = x / self.width
        yPercent = y / self.height

        # Get the ray from the camera
        cameraRay = self.scene.camera.getRay(xPercent, yPercent)

        # Get the color based on the ray
        color = self.getColorR(cameraRay)

        # Fixing any NaNs in numpy, clipping to 0, 1.
        color = np.nan_to_num(np.clip(color, 0, 1), 0) 
            
        return color
    
# Calls the 'main' function when this script is executed
if __name__ == '__main__':
    RayTracer.main("Ray Tracer Basics")
    pygame.quit()
