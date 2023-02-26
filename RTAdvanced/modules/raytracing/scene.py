"""
Author: Liz Matthews, Geoff Matthews
"""
import numpy as np

from ..raytracing.planar import Plane, Cube
from ..raytracing.spherical import Sphere, Ellipsoid
from ..raytracing.lights import DirectionalLight, PointLight
from .camera import Camera
from ..utils.vector import vec
from ..utils.definitions import COLORS

LIGHT_POSITION = vec(-1, 2, 2)


class Scene(object):
    """A class to contain all items in a scene.
       Contains a camera.
       Contains a list of lights.
       Contains a list of objects."""
    def __init__(self,
                 focus=vec(0, 0.2, 0),
                 direction=vec(0, 0, -1),
                 up=vec(0, 1, 0),
                 fov=45.0,
                 distance=2.5,
                 aspect=4/3):
        self.lights = []
        self.objects = []
        self.camera = Camera(focus, direction, up, fov, distance, aspect)
        # Set up lights, spheres,  and planes here
        self.setup()

    def setup(self):
        # Example setup
        self.addPointLight(color=vec(1, 1, 1), position=LIGHT_POSITION)
        # Blue Sphere
        self.addSphere(radius=0.5,
                       position=vec(1, 0, 0),
                       color=vec(0, 0, 1),
                       ambient=vec(0.2, 0.2, 0.4),
                       diffuse=vec(0.2, 0.2, 0.4),
                       specular=vec(0.8, 0.8, 1),
                       shininess=50,
                       specCoeff=.6,
                       reflective=False)
        """
        # Reflective Purple Sphere
        self.addSphere(radius=0.5,
                       position=vec(0, 0, 0),
                       color=vec(1, 0, 1),
                       ambient=vec(0.4, 0.2, 0.4),
                       diffuse=vec(0.4, 0.2, 0.4),
                       specular=vec(1, 0.8, 1),
                       shininess=25,
                       specCoeff=.8,
                       reflective=True)
        """
        # Red Ellipsoid
        self.addEllipsoid(a=1.5,
                          b=0.7,
                          c=0.5,
                          position=vec(0, 1, -2.3),
                          color=vec(1, 0, 0),
                          ambient=vec(0.4, 0.2, 0.2),
                          diffuse=vec(1, 0.2, 0.2),
                          specular=vec(1, 0.8, 0.8),
                          shininess=100,
                          specCoeff=1,
                          reflective=False)
        # Gray Plane
        self.addPlane(normal=vec(0, 1, 0),
                      position=vec(0, -1, 0),
                      color=COLORS["gray"],
                      ambient=vec(0.3, 0.3, 0.3),
                      diffuse=vec(0.7, 0.7, 0.7),
                      specular=vec(1, 1, 1),
                      shininess=5,
                      specCoeff=0.1,
                      reflective=False)
        """
        # Blue Cube
        self.addCube(length=1,
                     position=vec(0, 0, 0),
                     color=COLORS["blue"],
                     ambient=vec(0.3, 0.3, 0.7),
                     diffuse=vec(0.3, 0.3, 0.7),
                     specular=COLORS["white"],
                     shininess=0,
                     specCoeff=100)
        """

    def nearestObject(self, ray, obj=None):
        """Returns the nearest collision object
           and the distance to the object, excluding obj."""
        distances = [o.intersect(ray) for o in self.objects if o is not obj]
        colObj = None
        distanceToObj = np.inf
        for i, distance in enumerate(distances):
            if distance < distanceToObj and self.objects[i] is not obj:
                distanceToObj = distance
                colObj = self.objects[i]
        return colObj, distanceToObj

    def addSphere(self, radius=0.5,
                  position=vec(0, 0, 0), color=COLORS["blue"],
                  ambient=COLORS["blue"],
                  diffuse=COLORS["black"], specular=COLORS["white"],
                  shininess=0, specCoeff=100, reflective=False,
                  image=None):
        self.objects.append(Sphere(radius, position, color,
                                   ambient, diffuse,
                                   specular, shininess,
                                   specCoeff, reflective,
                                   image))

    def addEllipsoid(self, a=1, b=1, c=1,
                     position=vec(0, 0, 0), color=COLORS["red"],
                     ambient=COLORS["red"],
                     diffuse=COLORS["black"], specular=COLORS["white"],
                     shininess=0, specCoeff=100, reflective=False,
                     image=None):
        self.objects.append(Ellipsoid(a, b, c, position, color,
                                      ambient, diffuse,
                                      specular, shininess,
                                      specCoeff, reflective,
                                      image))

    def addPlane(self, normal=vec(0, 1, 0),
                 position=vec(0, 0, 0), color=COLORS["gray"],
                 ambient=COLORS["blue"],
                 diffuse=COLORS["black"], specular=COLORS["white"],
                 shininess=0, specCoeff=100, reflective=False,
                 image=None):
        self.objects.append(Plane(normal, position, color,
                                  ambient, diffuse,
                                  specular, shininess,
                                  specCoeff, reflective,
                                  image))

    def addCube(self, length=1,
                position=vec(0, 0, 0), color=COLORS["gray"],
                ambient=COLORS["blue"],
                diffuse=COLORS["black"], specular=COLORS["white"],
                shininess=0, specCoeff=100, reflective=False,
                image=None):
        self.objects.append(Cube(length, position, color,
                                 ambient, diffuse,
                                 specular, shininess,
                                 specCoeff, reflective,
                                 image))

    def addDirectionalLight(self,
                            color=COLORS["white"],
                            position=vec(0, 0, 0),
                            lightVector=vec(0, 0, 0)):
        self.lights.append(DirectionalLight(color=color,
                                            position=position,
                                            lightVector=lightVector))

    def addPointLight(self,
                      color=COLORS["white"],
                      position=vec(0, 0, 0)):
        self.lights.append(PointLight(color, position))
