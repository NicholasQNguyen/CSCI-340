""" Author: Liz Matthews, Geoff Matthews """
import numpy as np
import pygame

from render import ProgressiveRenderer, ShowTypes

from modules.raytracing.scene import Scene
from modules.raytracing.ray import Ray
from modules.raytracing.objects import Sphere, Plane
from modules.utils.vector import vec, normalize, magnitude


class RayTracer(ProgressiveRenderer):
    def __init__(self, width=800, height=600, show=ShowTypes.PerColumn):
        super().__init__(width, height, show=show)
        self.fog = vec(0.7, 0.9, 1.0)
        self.scene = Scene(aspect=width/height, fov=45)
        print("CAM POS:", self.scene.camera.getPosition())
        for obj in self.scene.objects:
            print(repr(obj) + " POS: " + str(obj.position))
        for light in self.scene.lights:
            print(repr(light) + " POS: " + str(light.position))

    def getColorR(self, ray):
        # Start with zero color
        color = np.zeros((3))

        # Normalize the ray
        nRay = Ray(ray.position, normalize(ray.direction))

        # Find any objects it collides with and calculate color
        for obj in self.scene.objects:
            if type(obj) == Sphere:
                t = obj.intersect(nRay)
                if t is None:
                    return self.fog
                nearestObj, minDist = self.scene.nearestObject(Ray(nRay.position, nRay.direction * t))
                color = nearestObj.getAmbient()
                normal = nearestObj.getNormal()
                if nearestObj is not None:
                    for light in self.scene.lights: 
                        """
                        |\vFL  r//\
                        | \    / |
                      i |  \  /  |-i
                        \/  \/   |
                        ----------
                          j    j
                        """
                        vecToLight = normalize(light.getVectorToLight(ray.direction * minDist))
                        vecFromLight = -vecToLight
                        # Finding angle of incidence
                        i = np.dot(vecFromLight, normal) * normal
                        j = vecFromLight - i
                        r = -i + j
                        angleOfIncidence = np.arccos(np.dot(vecFromLight, r) / magnitude(vec(r)))
                        diffuse = np.cos(angleOfIncidence)
                        color = color + diffuse
                        # 07 Slides, Slide 19
                        reflectionVector = vecToLight - (vecToLight - (np.dot(normal, vecToLight) * normal))
                        return color
            elif type(obj) == Plane:
                intersection = obj.intersect(nRay)
                # return vec(0, 1, 0)

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
