""" Author: Liz Matthews, Geoff Matthews """
import numpy as np
import pygame as pg

from render import ProgressiveRenderer, ShowTypes
# from quilt import QuiltRenderer
from modules.raytracing.scene import Scene
from modules.raytracing.ray import Ray
from modules.raytracing.lights import PointLight
from modules.raytracing.spherical import Ellipsoid
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
        # https://www.cuemath.com/geometry/angle-between-vectors/
        return max(0, np.dot(normal, vecToLight))

    def getSpecularAngle(self, vecToLight, normal,
                         cameraRay, obj):
        # 07 Slides, slide 30
        vecFromLight = vecToLight * (-1)
        halfwayVector = normalize(vecFromLight + cameraRay.direction)
        specularAngle = np.dot(normal, halfwayVector)
        # 07 Slides, Slide 24
        specularAngle **= obj.getShine()
        # 07 Slides, Slide 27
        specularAngle *= obj.getSpecularCoefficient()
        return specularAngle

    def getSpecularColor(self, specularAngle, objSpecularColor):
        # 07 Slides, Slide 20
        specularColor = specularAngle * objSpecularColor
        # Prevent black specular spots
        return specularColor if specularColor[0] > 0 else vec(0, 0, 0)

    def getColorR(self, ray):
        normalizedRay = Ray(ray.position, normalize(ray.direction))
        nearestObj, minDist = self.scene.nearestObject(normalizedRay)
        # We hit nothing
        if nearestObj is None:
            return self.fog
        # Start with base color of object
        color = nearestObj.getBaseColor()
        # 07 Slides, Slide 16
        color = color - nearestObj.getAmbient()
        surfaceHitPoint = normalizedRay.getPositionAt(minDist)
        normal = nearestObj.getNormal(surfaceHitPoint)
        # TODO remove this testing only
        if type(nearestObj) is Ellipsoid:
            print("NORMAL", normal)
        for light in self.scene.lights:
            # 03 Slides, Slide 32
            if type(light) == PointLight:
                vecToLight = light.getVectorToLight(surfaceHitPoint)
            # It's a directional light
            else:
                vecToLight = light.getVectorToLight()
            # Check if shadowed
            rayFromSurfaceToLight = Ray(surfaceHitPoint, vecToLight)
            shadowedObj, _ = self.scene.shadowed(rayFromSurfaceToLight, nearestObj)
            if shadowedObj is not None:
                return nearestObj.getAmbient()
            diffuse = self.getDiffuse(vecToLight, normal)
            # TODO remove this testing only
            if type(nearestObj) is Ellipsoid:
                print("DIFFUSE", diffuse)
            # 07 Slides, Slide 16
            color = color * diffuse
            # 07 Slides, Slide 16
            color = color + nearestObj.getAmbient()
            specularAngle = self.getSpecularAngle(vecToLight, normal,
                                                  normalizedRay, nearestObj)
            specularColor = self.getSpecularColor(specularAngle,
                                                  nearestObj.getSpecular())
            # 07 Slides, Slide 23
            color = color + specularColor
        return color

    def getColor(self, x, y):
        xPercent = x / self.width
        yPercent = y / self.height
        cameraRay = self.scene.camera.getRay(xPercent, yPercent)
        # Get the color based on the ray
        color = self.getColorR(cameraRay)
        # Fixing any NaNs in numpy, clipping to 0, 1.
        color = np.nan_to_num(np.clip(color, 0, 1), 0)
        return color


# Calls the 'main' function when this script is executed
if __name__ == '__main__':
    RayTracer.main("Ray Tracer Basics")
    pg.quit()
