""" Author: Liz Matthews, Geoff Matthews """
import numpy as np
import pygame

from render import ProgressiveRenderer, ShowTypes
from modules.raytracing.scene import Scene
from modules.raytracing.ray import Ray
from modules.raytracing.lights import PointLight
from modules.utils.vector import vec, normalize

TARGET_WIDTH = 800
TARGET_HEIGHT = 600
TEST_WIDTH = 400
TEST_HEIGHT = 300


class RayTracer(ProgressiveRenderer):
    def __init__(self,
                 width=TARGET_WIDTH,
                 height=TARGET_HEIGHT,
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
        return np.dot(normal, vecToLight)

    def getSpecularAngle(self, vecToLight, normal, cameraRay):
        # 07 Slides, slide 30
        vecFromLight = -1 * vecToLight
        halfwayVector = normalize(vecFromLight + cameraRay.direction)
        return np.dot(normal, halfwayVector)

    def getColorR(self, ray):
        # Start with zero color
        color = np.zeros((3))
        nRay = Ray(ray.position, normalize(ray.direction))
        nearestObj, minDist = self.scene.nearestObject(nRay)
        # We hit nothing
        if nearestObj is None:
            return self.fog
        shadowedObj, shadowMinDist = self.scene.shadowed(nRay, nearestObj)
        if shadowedObj is not None:
            pass
            # return vec(0, 1, 0)
            # return shadowedObj.getAmbient()
        # Base color
        color = nearestObj.getColor()
        # 07 Slides, Slide 16
        color = color - nearestObj.getAmbient()
        surfaceHitPoint = nRay.getPositionAt(minDist)
        normal = nearestObj.getNormal(surfaceHitPoint)
        for light in self.scene.lights:
            # 03 Slides, Slide 32
            if type(light) == PointLight:
                vecToLight = light.getVectorToLight(surfaceHitPoint)
            # It's a directional light
            else:
                vecToLight = light.getVectorToLight()
            diffuse = self.getDiffuse(vecToLight, normal)
            # diffuseColor = diffuse * nearestObj.getDiffuse()
            color = color * diffuse
            # color = color * diffuseColor
            specularAngle = self.getSpecularAngle(vecToLight, normal, nRay)
            # 07 Slides, Slide 24
            specularAngle **= nearestObj.getShine()
            # 07 Slides, Slide 27
            specularAngle *= nearestObj.getSpecularCoefficient()
            # 07 Slides, Slide 20
            specularColor = specularAngle * nearestObj.getSpecular()
            # print(str(nearestObj.getColor()) +\
            # " " + repr(nearestObj) +\
            # " SPEC COL " +\
            # str(specularColor))
            # Prevent black specular spots
            if not (specularColor[0] < 0):
                # print("SPEC COL", specularColor)
                color = color + specularColor
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
