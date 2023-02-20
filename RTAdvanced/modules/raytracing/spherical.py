import numpy as np

from .objects import Object3D
from .materials import Material
from ..utils.vector import normalize


class Spherical(Object3D):
    def quadraticFormula(self, a, b, c):
        """Calulates the quadratic formula.
           Returns a tuple with -b plus and minus
           in the 0th and 1st index respectively."""
        plusB = (-b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        minusB = (-b - np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        return (plusB, minusB)

    def getDiscriminant(self, a, b, c):
        """Calulates the discriminent (term under the
           sqrt in the quadratic formula).
           Returns a float."""
        return b ** 2 - 4 * a * c

    def getNormal(self, surfacePoint, intersection=None):
        """Find the unit normal."""
        # https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-shading/shading-normals.html
        return normalize(surfacePoint - self.position)


class Sphere(Spherical):
    def __init__(self, radius, position, baseColor, ambient,
                 diffuse, specular, shininess, specCoeff):
        super().__init__(position)
        self.material = Material(baseColor,
                                 ambient,
                                 diffuse,
                                 specular,
                                 shininess)
        self.radius = radius

    def getRadius(self):
        """Returns the radius of the circle."""
        return self.radius

    def intersect(self, ray):
        """Find the intersection for the sphere.
           Returns either a float representing the distance
           to the sphere (t) or infinity if it misses"""
        # 06 Slides, slide 43
        q = ray.position - self.position
        # 1 b/c normalized
        a = 1
        b = 2 * np.dot(q, ray.direction)
        c = np.dot(q, q) - self.radius ** 2
        # https://www.csee.umbc.edu/~olano/class/435-02-8/ray-sphere.html
        # We miss if discriminent is negative
        if self.getDiscriminant(a, b, c) < 0:
            return np.inf
        return self.positiveOnly(min(self.quadraticFormula(a, b, c)))

    def __repr__(self):
        return str(self.getBaseColor()) + " Sphere"


class Ellipsoid(Spherical):
    def __init__(self, a, b, c, position, color, ambient,
                 diffuse, specular, shininess, specCoeff):
        super().__init__(position)
        self.material = Material(color, ambient, diffuse, specular, shininess)
        self.a = a
        self.b = b
        self.c = c

    def intersect(self, ray):
        """Find the intersection for the ellipsoid.
           Returns either a float representing the distance
           to the ellipsoid (t) or infinity if it misses"""
        # 10 Slides, Slide 22
        q = ray.position - self.position
        s = (self.a, self.b, self.c)
        vOverS = ray.direction / s
        qOverS = q / s
        a = np.dot(vOverS, vOverS)
        b = np.dot(vOverS, qOverS) * 2
        c = np.dot(qOverS, qOverS) - 1
        if self.getDiscriminant(a, b, c) < 0:
            return np.inf
        return self.positiveOnly(min(self.quadraticFormula(a, b, c)))

    def __repr__(self):
        return str(self.getBaseColor()) + " Ellipsoid"
