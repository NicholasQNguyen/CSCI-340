"""
Author: Liz Matthews, Geoff Matthews
"""
from abc import ABC, abstractmethod
import numpy as np
from .materials import Material
from ..utils.vector import normalize, vec


class Object3D(ABC):
    """Abstract base class for all objects in the raytraced scene.
       Has a position, material.
       Has getter methods for all material properties.
       Has abstract methods intersect and getNormal."""
    def __init__(self, pos, material):
        self.position = np.array(pos)
        self.material = material

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


class Sphere(Object3D):
    def __init__(self, radius, position, baseColor, ambient, diffuse,
                 specular, shininess, specCoeff):
        super().__init__(position, True)
        self.material = Material(baseColor,
                                 ambient,
                                 diffuse,
                                 specular,
                                 shininess)
        self.radius = radius

    def getRadius(self):
        return self.radius

    def intersect(self, ray):
        """Find the intersection for the sphere."""
        # 06 Slides, slide 43
        q = ray.position - self.position
        # 1 b/c normalized
        # a = 1
        b = 2 * np.dot(q, ray.direction)
        c = np.dot(q, q) - self.radius ** 2
        # https://www.csee.umbc.edu/~olano/class/435-02-8/ray-sphere.html
        # We miss if discriminent is negative
        discriminant = b ** 2 - 4 * c
        if discriminant < 0:
            return np.inf
        sqrtTerm = np.sqrt(discriminant)
        t1 = (-b + sqrtTerm) / 2
        t2 = (-b - sqrtTerm) / 2
        returnedT = min(t1, t2)
        return returnedT if returnedT > 0 else np.inf

    def getNormal(self, surfacePoint, intersection=None):
        """Find the unit normal for the sphere . Must override."""
        # https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-shading/shading-normals.html
        return normalize(surfacePoint - self.position)

    def __repr__(self):
        return str(self.getBaseColor()) + " Sphere"


class Plane(Object3D):
    def __init__(self, normal, position, color, ambient, diffuse, specular,
                 shininess, specCoeff):
        super().__init__(position, False)
        self.material = Material(color, ambient, diffuse, specular, shininess)
        self.normal = normal

    def intersect(self, ray):
        """Find the intersection for the plane."""
        # 10 Slides, slide 16
        denom = np.dot(ray.direction, self.normal)
        if denom == 0:
            return np.inf
        q = self.position - ray.position
        t = (np.dot(q, self.normal)) / denom
        return t if t > 0 else np.inf

    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        return self.normal

    def __repr__(self):
        return str(self.getBaseColor()) + " Plane"

class Cube(Object3D):
    def __init__(self, length, position, color, ambient, diffuse, specular,
                 shininess, specCoeff):
        super().__init__(position, False)
        self.material = Material(color, ambient, diffuse, specular, shininess)
        self.length = length

    def intersect(self, ray):
        """Find the intersection for the cube."""
        pass

    def __repr__(self):
        return str(self.getBaseColor()) + " Cube"

class Ellipsoid(Object3D):
    def __init__(self, a, b, c, position, color, ambient, diffuse, specular,
                 shininess, specCoeff):
        super().__init__(position, False)
        self.material = Material(color, ambient, diffuse, specular, shininess)
        self.a = a
        self.b = b
        self.c = c

    def intersect(self, ray):
        """Find the intersection for the ellipsoids."""
        # 10 Slides, Slide 22
        q = ray.position - self.position
        s = (self.a, self.b, self.c)
        vOverS = ray.direction / s
        qOverS = q / s
        a = np.dot(vOverS, vOverS)
        b = 2 * (np.dot(vOverS, qOverS))
        c = (np.dot(qOverS, qOverS)) - 1
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return np.inf
        sqrtTerm = np.sqrt(discriminant)
        t1 = (-b + sqrtTerm) / (2 * a)
        t2 = (-b - sqrtTerm) / (2 * a)
        returnedT = min(t1, t2)
        return returnedT if returnedT > 0 else np.inf

    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        # 10 Slides, Slide 26
        # TODO Fix this
        return normalize(vec(2 * intersection[0] / self.a ** 2,
                             2 * intersection[1] / self.b ** 2,
                             2 * intersection[2] / self.c ** 2))

    def __repr__(self):
        return str(self.getBaseColor()) + " Ellipsoid"
