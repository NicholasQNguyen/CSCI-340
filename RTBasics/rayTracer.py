""" Author: Liz Matthews, Geoff Matthews """
# TODO Fix nearest object (in scene), ifx diffuse, fix specular
import numpy as np
import pygame

from render import ProgressiveRenderer, ShowTypes

from modules.raytracing.scene import Scene
from modules.raytracing.ray import Ray
from modules.raytracing.lights import PointLight, DirectionalLight
from modules.utils.vector import vec, normalize, magnitude

TARGET_WIDTH = 800
TARGET_HEIGHT = 600
TEST_WIDTH = 400
TEST_HEIGHT = 300


class RayTracer(ProgressiveRenderer):
    def __init__(self, width=TARGET_WIDTH, height=TARGET_HEIGHT, show=ShowTypes.PerColumn):
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
        # 07 Slides, Slide 19
        """
        reflectionVector = normalize(vecToLight -
                                     (vecToLight -
                                      np.dot(normal,
                                       vecToLight) * normal))
        return np.dot(reflectionVector, cameraRay.direction)
        """
        # 07 Slides, slide 30
        halfwayVector = normalize(vecToLight + cameraRay.direction)
        return np.dot(normal, halfwayVector)

    def getColorR(self, ray):
        # Start with zero color
        color = np.zeros((3))
        # Normalize the ray
        nRay = Ray(ray.position, normalize(ray.direction))
        # Find any objects it collides with and calculate color
        nearestObj, minDist = self.scene.nearestObject(
                              Ray(nRay.position, nRay.direction))
        # We hit nothing
        if nearestObj is None:
            return self.fog
        color = vec(0, 0, 1)
        # color = nearestObj.getAmbient()
        surfaceHitPoint =  nRay.getPositionAt(minDist)
        print("SURFACE HIT", surfaceHitPoint)
        print("--------------------------------------------------------")
        # normal = Ray(surfaceHitPoint, nearestObj.getNormal())
        normal = nearestObj.getNormal(surfaceHitPoint)
        for light in self.scene.lights:
            print("NORMAL", normal)
            # 03 Slides, Slide 32
            """
            |\ v2L r//\ 
            | \    / |
          i |  \  /  |-i
            \/  \/   |
            ----------
              j    j
            """
            if type(light) == PointLight:
                vecToLight = light.getVectorToLight(surfaceHitPoint)
                print("VEC 2 LIGHT", vecToLight)
                print("--------------------------------------------------------")
            # It's a directional light
            else:
                vecToLight = Ray(surfaceHitPoint, light.getVectorToLight())
            diffuse = self.getDiffuse(vecToLight, normal)
            print("DIFFUSE", diffuse)
            print("-----------------------------------------------------------------------")
            color = color * diffuse
            specularAngle = self.getSpecularAngle(vecToLight, normal, nRay)
            specularColor = specularAngle * nearestObj.getSpecular()
            # color = color + specularColor
            color = color + nearestObj.getAmbient()
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
    # TODO figure out if this stuff down here is any good
    """
    # Finding angle of incidence
    # 03 Slides, slide 32
    # vecFromLight = -vecToLight
    # i = normalize(np.dot(vecFromLight, normal) * normal)
    # j = normalize(vecFromLight - i)
    # r = normalize(-i + j)
    # SOHCAHTOA
    # angleOfIncidence = 90 - np.arctan(magnitude(i)/magnitude(j))
    # angleOfIncidence = np.dot(vecToLight, normal)
    # angleOfIncidence = np.arccos(angleOfIncidence)
    # 07 Slides, slide 10
    # return np.cos(angleOfIncidence)
    """
