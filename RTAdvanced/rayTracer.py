# TODO ask about cubes, and updating the machines to python3 3.10
""" Author: Liz Matthews, Geoff Matthews """
import numpy as np
import pygame as pg

from render import ProgressiveRenderer, ShowTypes
# from quilt import QuiltRenderer
from modules.raytracing.scene import Scene
from modules.raytracing.planar import Cube
from modules.raytracing.ray import Ray
from modules.utils.vector import vec, normalize

SCREEN_MULTIPLIER = 1
WIDTH = 800
HEIGHT = 600
MAX_RECURSION_DEPTH = 3


class RayTracer(ProgressiveRenderer):
    def __init__(self,
                 width=WIDTH * SCREEN_MULTIPLIER,
                 height=HEIGHT * SCREEN_MULTIPLIER,
                 show=ShowTypes.PerColumn):
        super().__init__(width, height, show=show)
        self.fog = vec(0.7, 0.9, 1.0)
        self.scene = Scene(aspect=width/height, fov=45)
        print("Camera Position:", self.scene.camera.getPosition())
        for obj in self.scene.objects:
            print(repr(obj) + " Position: " + str(obj.position))
        for light in self.scene.lights:
            print(repr(light) + " Position: " + str(light.position))

    def getReflectionAngle(self, vector1, vector2):
        """Returns an angle that is the product of the
           reflection of vector1 and vector2.
           Expects normalized vectors."""
        # 03 Slides, Slide 32
        # https://www.cuemath.com/geometry/angle-between-vectors/
        return np.dot(vector1, vector2)

    def getReflectionVector(self, vector, normal):
        """Returns the vector that is the reflection
           of the vector off of a surface.
           Expects normalized vectors."""
        # 03 Slides, Slide 32
        # https://www.cuemath.com/geometry/angle-between-vectors/
        i = np.dot(vector, normal)
        j = vector - i
        return -i + j

    def getDiffuse(self, vectorToLight, normal):
        """Gets the diffuse. Expects normalized vectors"""
        return max(0, self.getReflectionAngle(vectorToLight, normal))

    def getSpecularAngle(self, vectorToLight, normal,
                         cameraRay, obj):
        # 07 Slides, slide 30
        halfwayVector = normalize(-vectorToLight + cameraRay.direction)
        # 07 Slides, Slide 24 + Slide 27
        return self.getReflectionAngle(normal, halfwayVector) ** \
            obj.getShine() * \
            obj.getSpecularCoefficient()

    def getSpecularColor(self, specularAngle, objectSpecularColor):
        # 07 Slides, Slide 20
        return specularColor if \
            (specularColor := specularAngle * objectSpecularColor)[0] > 0 \
            else vec(0, 0, 0)  # Prevent black specular spots

    def getColorR(self, ray, recursionCount):
        """Returns color with diffuse and specualr attached.
           Expects a normalized ray."""
        nearestObject, minDist = self.scene.nearestObject(ray, None)
        # We hit nothing
        if nearestObject is None:
            return self.fog
        if type(nearestObject) is Cube:
            return vec(0, 1, 0)
        # Start with base color of object + ambient difference
        color = nearestObject.getBaseColor() - \
            nearestObject.getAmbient()  # 07 Slides, Slide 16
        surfaceHitPoint = ray.getPositionAt(minDist)
        normal = nearestObject.getNormal(surfaceHitPoint)
        # TODO fix this
        # Reflect if it's reflective
        if nearestObject.getReflective() and \
           recursionCount < MAX_RECURSION_DEPTH:
            return color + \
                self.getColorR(Ray(surfaceHitPoint,
                                   self.getReflectionVector(ray.direction,
                                                            normal)),
                               recursionCount + 1)
        for light in self.scene.lights:
            vectorToLight = light.getVectorToLight(surfaceHitPoint)
            # Check if shadowed
            shadowedObject, _ = self.scene.nearestObject(Ray(
                                                             surfaceHitPoint,
                                                             vectorToLight),
                                                         nearestObject)
            if shadowedObject is not None:
                return nearestObject.getAmbient()
            # 07 Slides, Slide 16
            color = color * \
                self.getDiffuse(vectorToLight, normal) + \
                nearestObject.getAmbient() + \
                self.getSpecularColor(self.getSpecularAngle(  # Slide 23
                                          vectorToLight,
                                          normal,
                                          ray,
                                          nearestObject),
                                      nearestObject.getSpecular())
        return color

    def getColor(self, x, y):
        return np.nan_to_num(  # Fixing any NaNs in numpy, clipping to 0, 1.
            np.clip(
                self.getColorR(  # Get the color based on the ray
                    self.scene.camera.getRay(x / self.width,
                                             y / self.height),
                    0),
                0, 1),
            0)


# Calls the 'main' function when this script is executed
if __name__ == '__main__':
    RayTracer.main("Ray Tracer Basics")
    pg.quit()
