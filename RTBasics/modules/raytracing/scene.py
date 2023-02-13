"""
Author: Liz Matthews, Geoff Matthews
"""
import numpy as np
from ..raytracing.objects import Sphere, Plane
from ..raytracing.lights import DirectionalLight, PointLight
from .camera import Camera
from ..utils.vector import vec
from ..utils.definitions import COLORS

POSITION = vec(1, 3, -5)

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
        self.addSphere()
        self.addPointLight(color=vec(1, 1, 1), position=POSITION)
        # self.addSphere(ambient=vec(.2, 0, 0),
        #                radius=.7,
        #                position=vec(0, 1, -3))
        """
        self.addSphere(ambient=vec(0.2, 0.2, 0.4),
                       diffuse=vec(0.2, 1, 0.2),
                       specular=vec(0.8, 0.8, 1),
                       shininess=5,
                       specCoeff=0.2,
                       radius=.7,
                       position=vec(-1, -0.2, -4))
        """
        # self.addPlane(position=vec(0, -1, 0))
        # self.addPlane(position=vec(0, 0, 0))
        # self.addPointLight(position=vec(1, 0, 0))

    def nearestObject(self, ray):
        """Returns the nearest collision object
           and the distance to the object."""
        distances = [o.intersect(ray) for o in self.objects]
        filteredDistances = [dist for dist in distances if dist is not None]
        # Sort so we can get the shortest distance
        filteredDistances.sort()
        # TODO make this actually something
        nearestObj = self.objects[0]
        minDistance = filteredDistances[0]
        return nearestObj, minDistance

    def shadowed(self, obj, ray):
        """Returns the nearest collision object and the distance to the object,
           excluding obj."""
        distances = [o.intersect(ray) for o in self.objects if o is not obj]
        filteredDistances = [dist for dist in distances if dist is not None]
        filteredDistances.sort()
        minDistance = filteredDistances[0]
        colObj = self.objects[0]
        if colObj is obj:
            colObj = None
        return colObj, minDistance

    def addSphere(self, radius=0.5,
                  position=vec(0, 0, 0), ambient=COLORS["blue"],
                  diffuse=COLORS["black"], specular=COLORS["white"],
                  shininess=0, specCoeff=100):
        self.objects.append(Sphere(radius, position,
                                   ambient, diffuse,
                                   specular, shininess, specCoeff))

    def addPlane(self, normal=vec(0, 1, 0),
                 position=vec(0, 0, 0), ambient=COLORS["blue"],
                 diffuse=COLORS["black"], specular=COLORS["white"],
                 shininess=0, specCoeff=100):
        self.objects.append(Plane(normal, position,
                                  ambient, diffuse,
                                  specular, shininess, specCoeff))

    def addDirectionalLight(self,
                            color=COLORS["white"],
                            position=vec(0, 0, 0)):
        self.lights.append(DirectionalLight(color, position))

    def addPointLight(self,
                      color=COLORS["white"],
                      position=vec(0, 0, 0)):
        self.lights.append(PointLight(color, position))
