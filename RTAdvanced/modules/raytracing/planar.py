import numpy as np

from .objects import Object3D
from .materials import Material


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
        self.sides = []
        self.setSides()

    def intersect(self, ray):
        """Find the intersection for the cube."""
        t = 1.0
        return self.positiveOnly(t)

    def __repr__(self):
        return str(self.getBaseColor()) + " Cube"
