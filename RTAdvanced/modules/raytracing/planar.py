import sys
import numpy as np
from enum import Enum

from .objects import Object3D
from ..utils.vector import vec


class Side(Enum):
    """Each side of the cube."""
    Top = 0
    Bottom = 1
    Left = 2
    Right = 3
    Front = 4
    Back = 5


class Planar(Object3D):
    def signedIntersect(self, ray):
        # 10 Slides, slide 16
        return np.inf if \
            (denom := np.dot(ray.direction, self.normal)) == 0 else \
            np.dot(self.position - ray.position, self.normal) / denom


class Plane(Planar):
    def __init__(self, normal, position, baseColor,
                 ambient, diffuse, specular,
                 shininess, specCoeff, reflective,
                 image):
        super().__init__(position, baseColor, ambient,
                         diffuse, specular, shininess,
                         specCoeff, reflective, image)
        self.normal = normal

    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        return self.normal

    def intersect(self, ray):
        """Find the intersection for the plane.
           Returns a t only if it's positive."""
        return self.positiveOnly(self.signedIntersect(ray))

    def __repr__(self):
        return str(self.getBaseColor()) + " Plane"


class Cube(Planar):
    def __init__(self, length, position, baseColor, ambient,
                 diffuse, specular, shininess, specCoeff,
                 reflective, image):
        super().__init__(position, baseColor, ambient,
                         diffuse, specular, shininess,
                         specCoeff, reflective, image)
        self.length = length
        self.sides = []
        self.setSides()

    def setSides(self):
        for side in [Side.Top, Side.Bottom, Side.Left,
                     Side.Right, Side.Front, Side.Bottom]:
            self.sides.append(self.generateSide(side))

    def generateSide(self, side):
        distance = self.length / 2
        match side:
            case Side.Top:
                normal = vec(0, 1, 0)
                position = self.position + vec(0,
                                               distance,
                                               0)
            case Side.Bottom:
                normal = vec(0, -1, 0)
                position = self.position - vec(0,
                                               distance,
                                               0)
            case Side.Left:
                normal = vec(-1, 0, 0)
                position = self.position - vec(distance,
                                               0,
                                               0)
            case Side.Right:
                normal = vec(1, 0, 0)
                position = self.position + vec(distance,
                                               0,
                                               0)
            case Side.Front:
                normal = vec(0, 0, 1)
                position = self.position + vec(0,
                                               0,
                                               distance)
            case Side.Back:
                normal = vec(0, 0, -1)
                position = self.position - vec(0,
                                               0,
                                               distance)
            case _:
                print("OH GOD")
                sys.exit(1)

        return Plane(normal=normal,
                     position=position,
                     color=self.getBaseColor(),
                     ambient=self.getAmbient(),
                     diffuse=self.getDiffuse(),
                     specular=self.getSpecular(),
                     shininess=self.getShine(),
                     specCoeff=self.getSpecularCoefficient())

    # TODO get this working
    def intersect(self, ray):
        """Find the intersection for the cube."""
        return min([side.signedIntersect(ray) for side in self.sides])

    # TODO actually get this working
    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        return self.normal

    def __repr__(self):
        return str(self.getBaseColor()) + " Cube"
