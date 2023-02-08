"""
Author: Liz Matthews, Geoff Matthews
"""
from abc import ABC, abstractmethod
import numpy as np
from .materials import Material
from ..utils.vector import normalize


class Object3D(ABC):
    """Abstract base class for all objects in the raytraced scene.
       Has a position, material.
       Has getter methods for all material properties.
       Has abstract methods intersect and getNormal."""
    def __init__(self, pos, material):
        self.position = np.array(pos)
        self.material = material

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

    @abstractmethod
    def intersect(self, ray):
        """Find the intersection for the given object. Must override."""
        pass

    @abstractmethod
    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        pass


class Sphere(Object3D):
    def __init__(self, radius, position, ambient, diffuse,
                 specular, shininess, specCoeff):
        super().__init__(position, True)
        self.material = Material(ambient, diffuse, specular, shininess)
        self.radius = radius

    def getRadius(self):
        return self.radius

    def intersect(self, ray):
        """Find the intersection for the sphere."""
        q = ray.position - self.position
        a = 1
        b = 2 * np.dot(q, ray.direction)
        c = np.dot(q, q) - self.radius ** 2
        # https://www.csee.umbc.edu/~olano/class/435-02-8/ray-sphere.html
        # We miss if discriminent is negative
        discriminent = b ** 2 - 4 * c
        if discriminent < 0:
            return None
        # 1 b/c normalized
        t1 = (-b + np.sqrt(discriminent)) / 2
        t2 = (-b - np.sqrt(discriminent)) / 2
        return min(t1, t2)

    def getNormal(self, intersection=None):
        """Find the normal for the given object. Must override."""
        return normalize(2 * self.position)

    def __repr__(self):
        return "Sphere"


class Plane(Object3D):
    def __init__(self, normal, position, ambient, diffuse, specular,
                 shininess, specCoeff):
        super().__init__(position, False)
        self.material = Material(ambient, diffuse, specular, shininess)
        self.normal = normal

    def intersect(self, ray):
        """Find the intersection for the plane."""
        denom = np.dot(ray.direction, self.normal)
        if denom != 0:
            t = np.dot((self.position - ray.position), self.normal) / denom
            return ray.position + ray.direction * t
        else:
            return np.inf

    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        return self.normal

    def __repr__(self):
        return "Plane"
