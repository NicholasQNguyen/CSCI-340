import sys
import numpy as np
from enum import Enum

from .objects import Object3D
from .materials import Material

class Side(Enum):
    """Each side of the cube."""
    Top = 0
    Botton = 1
    Left = 2
    Right = 3
    Front = 4
    Bottom = 5


class Planar(Object3D):
    pass


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
        """Find the intersection for the plane."""
        # 10 Slides, slide 16
        denom = np.dot(ray.direction, self.normal)
        if denom == 0:
            return np.inf
        q = self.position - ray.position
        t = (np.dot(q, self.normal)) / denom
        return self.positiveOnly(t)

    def __repr__(self):
        return str(self.getBaseColor()) + " Plane"


class Cube(Planar):
    def __init__(self, length, position, color, ambient,
                 diffuse, specular, shininess, specCoeff):
        super().__init__(position, False)
        self.material = Material(color, ambient, diffuse, specular, shininess)
        self.length = length
        self.sides = []
        self.setSides()

    def setSides(self): 
        addSide(Side.Top)
        addSide(Side.Bottom)
        addSide(Side.Left)
        addSide(Side.Right)
        addSide(Side.Front)
        addSide(Side.Back)

    def intersect(self, ray):
        """Find the intersection for the cube."""
        ts = [side.intersect(ray) for side in self.sides]
        filteredTs = [t for t in ts if t is not np.inf]
        return self.positiveOnly(t)

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

        self.sides.append(normal=normal,
                          position=position,
                          color=self.color,
                          ambient=self.ambient,
                          diffuse=self.diffuse,
                          specular=self.specular,
                          shininess=self.shininess,
                          specCoeff=self.specularCoefficient)
        

    def __repr__(self):
        return str(self.getBaseColor()) + " Cube"
