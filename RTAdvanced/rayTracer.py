""" Author: Liz Matthews, Geoff Matthews """
import numpy as np
import pygame as pg

from render import ProgressiveRenderer, ShowTypes
# from quilt import QuiltRenderer
from modules.raytracing.scene import Scene
from modules.raytracing.ray import Ray
from modules.raytracing.lights import PointLight
from modules.utils.vector import vec, normalize

SCREEN_MULTIPLIER = 1
WIDTH = 800
HEIGHT = 600


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

    def getDiffuse(self, vecToLight, normal):
        """Gets the diffuse. Expects normalized vectors"""
        # 03 Slides, Slide 32
        # https://www.cuemath.com/geometry/angle-between-vectors/
        return max(0, np.dot(normal, vecToLight))

    def getSpecularAngle(self, vecToLight, normal,
                         cameraRay, obj):
        # 07 Slides, slide 30
        halfwayVector = normalize(-vecToLight + cameraRay.direction)
        # 07 Slides, Slide 24 + Slide 27
        return np.dot(normal, halfwayVector) ** \
            obj.getShine() * \
            obj.getSpecularCoefficient()

    def getSpecularColor(self, specularAngle, objSpecularColor):
        # 07 Slides, Slide 20
        specularColor = specularAngle * objSpecularColor
        # Prevent black specular spots
        return specularColor if specularColor[0] > 0 else vec(0, 0, 0)

    def getColorR(self, ray):
        """Gets the color with diffuse and specualr attached.
           Expects a normalized ray."""
        nearestObj, minDist = self.scene.nearestObject(ray, None)
        # We hit nothing
        if nearestObj is None:
            return self.fog
        # Start with base color of object + ambient difference
        color = nearestObj.getBaseColor() - \
            nearestObj.getAmbient()  # 07 Slides, Slide 16
        surfaceHitPoint = ray.getPositionAt(minDist)
        normal = nearestObj.getNormal(surfaceHitPoint)
        for light in self.scene.lights:
            if type(light) == PointLight:
                vecToLight = light.getVectorToLight(surfaceHitPoint)
            # It's a directional light
            else:
                vecToLight = light.getVectorToLight()
            # Check if shadowed
            shadowedObj, _ = self.scene.nearestObject(Ray(
                                                          surfaceHitPoint,
                                                          vecToLight),
                                                      nearestObj)
            if shadowedObj is not None:
                return nearestObj.getAmbient()
            # 07 Slides, Slide 16
            color = color * \
                self.getDiffuse(vecToLight, normal) + \
                nearestObj.getAmbient() + \
                self.getSpecularColor(self.getSpecularAngle(  # Slide 23
                                          vecToLight,
                                          normal,
                                          ray,
                                          nearestObj),
                                      nearestObj.getSpecular())
        return color

    def getColor(self, x, y):
        return np.nan_to_num(  # Fixing any NaNs in numpy, clipping to 0, 1.
            np.clip(
                self.getColorR(  # Get the color based on the ray
                    self.scene.camera.getRay(x/self.width,
                                             y / self.height)),
                0, 1),
            0)


# Calls the 'main' function when this script is executed
if __name__ == '__main__':
    RayTracer.main("Ray Tracer Basics")
    pg.quit()
