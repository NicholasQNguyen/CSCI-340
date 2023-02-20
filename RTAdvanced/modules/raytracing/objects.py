"""
Author: Liz Matthews, Geoff Matthews
"""
from abc import ABC, abstractmethod
import numpy as np
from .materials import Material


class Object3D(ABC):
    """Abstract base class for all objects in the raytraced scene.
       Has a position, material.
       Has getter methods for all material properties.
       Has abstract methods intersect and getNormal."""
    def __init__(self, pos):
        self.position = np.array(pos)

    def getPosition(self):
        return self.position

    def getAmbient(self, intersection=None):
        """Getter method for the material's ambient color.
           Intersection parameter is unused for Ray Tracing Basics."""
        return self.material.getAmbient()

    def getDiffuse(self, intersection=None):
        """Getter method for the material's diffuse color.
           Intersection parameter is unused for Ray Tracing Basics."""
        return self.material.getDiffuse()

    def getSpecular(self, intersection=None):
        """Getter method for the material's specular color.
           Intersection parameter is unused for Ray Tracing Basics."""
        return self.material.getSpecular()

    def getShine(self):
        """Getter method for the material's shininess factor."""
        return self.material.getShine()

    def getSpecularCoefficient(self, intersection=None):
        """Getter method for the material's specular coefficient.
           Intersection parameter is unused for Ray Tracing Basics."""
        return self.material.getSpecularCoefficient()

    def getBaseColor(self):
        """Getter method for the material's color."""
        return self.material.getBaseColor()

    @abstractmethod
    def intersect(self, ray):
        """Find the intersection for the given object. Must override."""
        pass

    @abstractmethod
    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        pass

    def positiveOnly(self, t):
        """Returns t or infinity if t is negative."""
        return t if t > 0 else np.inf


class Planar(Object3D):
    def intersect(self, ray):
        """Find the intersection for the plane."""
        # 10 Slides, slide 16
        denom = np.dot(ray.direction, self.normal)
        if denom == 0:
            return np.inf
        q = self.position - ray.position
        t = (np.dot(q, self.normal)) / denom
        return self.positiveOnly(t)


class Plane(Planar):
    def __init__(self, normal, position, color, ambient, diffuse, specular,
                 shininess, specCoeff):
        super().__init__(position)
        self.material = Material(color, ambient, diffuse, specular, shininess)
        self.normal = normal

    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        return self.normal

    def __repr__(self):
        return str(self.getBaseColor()) + " Plane"


class Cube(Planar):
    def __init__(self, length, position, color, ambient,
                 diffuse, specular, shininess, specCoeff):
        super().__init__(position, False)
        self.material = Material(color, ambient, diffuse, specular, shininess)
        self.length = length

    def intersect(self, ray):
        """Find the intersection for the cube."""
        t = 1.0;
        return self.positiveOnly(t)

    def __repr__(self):
        return str(self.getBaseColor()) + " Cube"
