import sys
import numpy as np
from enum import Enum

from .objects import Object3D
from .materials import Material
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
    def intersectPart1(self, ray):
        # 10 Slides, slide 16
        denom = np.dot(ray.direction, self.normal)
        if denom == 0:
            return np.inf
        q = self.position - ray.position
        return (np.dot(q, self.normal)) / denom


class Plane(Planar):
    def __init__(self, normal, position, color, ambient, diffuse, specular,
                 shininess, specCoeff):
        super().__init__(position)
        self.material = Material(color, ambient, diffuse, specular, shininess)
        self.normal = normal

    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        return self.normal

    def intersect(self, ray):
        """Find the intersection for the plane.
           Returns a t only if it's positive."""
        return self.positiveOnly(self.intersectPart1(ray))

    def signedIntersect(self, ray):
        """Find the intersection for the plane.
           Returns a signed t."""
        return self.intersectPart1(ray)

    def __repr__(self):
        return str(self.getBaseColor()) + " Plane"


class Cube(Planar):
    def __init__(self, length, position, color, ambient,
                 diffuse, specular, shininess, specCoeff):
        super().__init__(position)
        self.material = Material(color, ambient, diffuse, specular, shininess)
        self.length = length
        self.sides = []
        self.setSides()

    def setSides(self):
        self.addSide(Side.Top)
        self.addSide(Side.Bottom)
        self.addSide(Side.Left)
        self.addSide(Side.Right)
        self.addSide(Side.Front)
        self.addSide(Side.Back)

    def addSide(self, side):
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

        self.sides.append(Plane(normal=normal,
                                position=position,
                                color=self.getBaseColor(),
                                ambient=self.getAmbient(),
                                diffuse=self.getDiffuse(),
                                specular=self.getSpecular(),
                                shininess=self.getShine(),
                                specCoeff=self.getSpecularCoefficient()))

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
