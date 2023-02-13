""" Author: Liz Matthews, Geoff Matthews """
import numpy as np
import pygame

from render import ProgressiveRenderer, ShowTypes

from modules.raytracing.scene import Scene
from modules.raytracing.ray import Ray
from modules.utils.vector import vec, normalize, magnitude


class RayTracer(ProgressiveRenderer):
    def __init__(self, width=800, height=600, show=ShowTypes.PerColumn):
        super().__init__(width, height, show=show)
        self.fog = vec(0.7, 0.9, 1.0)
        self.scene = Scene(aspect=width/height, fov=45)
        print("Camera Position:", self.scene.camera.getPosition())
        for obj in self.scene.objects:
            print(repr(obj) + " Position: " + str(obj.position))
        for light in self.scene.lights:
            print(repr(light) + " Position: " + str(light.position))

    def getColorR(self, ray):
        def getDiffuse(vecToLight, normal):
            vecFromLight = vecToLight * -1
            # Finding angle of incidence
            # 03 Slides, slide 32
            i = np.dot(vecFromLight, normal) * normal
            j = vecFromLight - i
            # r = -i + j
            # SOHCAHTOA
            angleOfIncidence = 90 - np.arctan(magnitude(i)/magnitude(j))
            # return np.dot(vecFromLight, r) / magnitude(vec(r))
            # 07 Slides, slide 10
            return np.cos(angleOfIncidence)

        def getSpecularAngle(vecToLight, normal, cameraRay):
            # 07 Slides, Slide 19
            reflectionVector = normalize(vecToLight -
                                         (vecToLight -
                                          (np.dot(normal,
                                           vecToLight) * normal)))
            return np.dot(reflectionVector, cameraRay.direction)

        # Start with zero color
        color = np.zeros((3))
        # Normalize the ray
        nRay = Ray(ray.position, normalize(ray.direction))
        # Find any objects it collides with and calculate color
        for obj in self.scene.objects:
            t = obj.intersect(nRay)
            # We hit nothing
            if t is None:
                return self.fog
            nearestObj, minDist = self.scene.nearestObject(
                                  Ray(nRay.position, nRay.direction * t))
            color = vec(0, 0, 1)
            # color = nearestObj.getAmbient()
            normal = nearestObj.getNormal()
            for light in self.scene.lights:
                # 03 Slides, Slide 32
                """
                |\ v2L r//\ 
                | \    / |
              i |  \  /  |-i
                \/  \/   |
                ----------
                  j    j
                """
                vecToLight = normalize(
                             light.getVectorToLight(
                                   ray.direction * minDist))
                diffuse = getDiffuse(vecToLight, normal)
                color = color * diffuse
                specularAngle = getSpecularAngle(vecToLight, normal, nRay)
                specularColor = specularAngle * nearestObj.getSpecular()
                # color = color + specularColor
                # color = color + obj.getAmbient()
            return color

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
