# textures on planes,
""" Author: Liz Matthews, Geoff Matthews """
import numpy as np
import pygame as pg

from render import ProgressiveRenderer, ShowTypes
# from quilt import QuiltRenderer
from modules.raytracing.scene import Scene
from modules.raytracing.spherical import Sphere, Ellipsoid
from modules.raytracing.planar import Plane
from modules.raytracing.ray import Ray
from modules.utils.vector import vec, normalize
from modules.utils.definitions import twoFiftyFiveToOnePointO

SCREEN_MULTIPLIER = 1
WIDTH = 800
HEIGHT = 600
MAX_RECURSION_DEPTH = 3
X = 0
Y = 1
Z = 2


class RayTracer(ProgressiveRenderer):
    def __init__(self,
                 width=WIDTH * SCREEN_MULTIPLIER,
                 height=HEIGHT * SCREEN_MULTIPLIER,
                 show=ShowTypes.PerColumn,
                 samplePerPixel=1,
                 file=None):
        super().__init__(width, height, show=show,
                         samplePerPixel=samplePerPixel,
                         file=file)
        self.fog = vec(0.7, 0.9, 1.0)
        self.scene = Scene(aspect=width/height, fov=45)
        print("Camera Position:", self.scene.camera.getPosition())
        for obj in self.scene.objects:
            print(repr(obj) + " Position: " + str(obj.position))
        for light in self.scene.lights:
            print(repr(light) + " Position: " + str(light.position))

    def getReflectionAngle(self, vector1, vector2):
        """Returns an angle that is
           between vector1 and vector2.
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
        return -(i := (np.dot(vector, normal) * normal)) + (vector - i)

    def returnImage(self, obj, surfaceHitPoint):
        """Returns the color of the image we hit."""
        # 11 Slides, Slide 20
        if type(obj) is Sphere or \
           type(obj) is Ellipsoid:
            # 11 Slides, Slide 49
            d = obj.getPosition() - surfaceHitPoint
            u = 0.5 + (np.arctan2(d[Z], d[X]) / (2 * np.pi))
            v = np.arccos(d[Y]) / np.pi
            # 11 Slides, Slide 21
            px = int(u * obj.getImage().get_width()) % \
                obj.getImage().get_width()
            py = int(v * obj.getImage().get_height()) % \
                obj.getImage().get_height()
            return twoFiftyFiveToOnePointO(obj.getImage().get_at((px, py)))
        # TODO get working for cubes
        elif type(obj) is Plane:
            normal = obj.getNormal()
            forward = self.scene.camera.getForward()
            u = np.cross(normal, forward)
            v = np.cross(normal, u)
            # 11 Slides, Slide 24
            p = normalize(surfaceHitPoint - obj.getPosition())
            coordinateU = int(np.dot(u, p)) % obj.getImage().get_width()
            coordinateV = int(np.dot(v, p)) % obj.getImage().get_height()
            return twoFiftyFiveToOnePointO(obj.getImage().get_at(
                (coordinateU, coordinateV)))

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
            (specularColor := specularAngle * objectSpecularColor)[X] > 0 \
            else vec(0, 0, 0)  # Prevent black specular spots

    def getColorR(self, ray, recursionCount=0):
        """Returns color with diffuse and specualr attached.
           Expects a normalized ray."""
        nearestObject, minDist = self.scene.nearestObject(ray)
        # We hit nothing
        if nearestObject is None:
            return self.fog
        surfaceHitPoint = ray.getPositionAt(minDist)
        normal = nearestObject.getNormal(surfaceHitPoint)
        # Reflect if it's reflective
        if nearestObject.isReflective():
            return self.getColorR(Ray(surfaceHitPoint,
                                      self.getReflectionVector(ray.direction,
                                                               normal)),
                                  recursionCount + 1)
        if nearestObject.getImage() is not None:
            color = self.returnImage(nearestObject, surfaceHitPoint)
        else:
            # Start with base color of object + ambient difference
            color = nearestObject.getBaseColor() - \
                nearestObject.getAmbient()  # 07 Slides, Slide 16
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

    def getColor(self, x, y, samplePerPixel=1):
        totalColor = np.zeros(3)
        for i in range(samplePerPixel ** 2):
            # Hit the center of the pixel
            shift = 1 / ((samplePerPixel + 1) * (i + 1))
            # Get the color based on the ray
            cameraRay = self.scene.camera.getRay(
                                                    (x + shift) / self.width,
                                                    (y + shift) / self.height
                                                )
            # Fixing any NaNs in numpy, clipping to 0, 1.
            totalColor = totalColor + np.nan_to_num(np.clip(
                self.getColorR(cameraRay, 0), 0, 1), 0)
        return totalColor / (samplePerPixel ** 2)


# Calls the 'main' function when this script is executed
if __name__ == '__main__':
    RayTracer.main("Ray Tracer Basics")
    pg.quit()
