"""
Author: Liz Matthews, Geoff Matthews
"""
import numpy as np
from ..raytracing.objects import Sphere, Plane
from ..raytracing.lights import DirectionalLight, PointLight
from .camera import Camera
from ..utils.vector import vec
from ..utils.definitions import COLORS

POSITION = vec(1, 3, 0)


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
        """
        self.addPointLight(color=vec(1, 1, 1), position=POSITION)
        # Blue Sphere
        self.addSphere(radius=0.7,
                       position=vec(0, 1, -3),
                       color=vec(0, 0, 1),
                       ambient=vec(0.2, 0.2, 0.4),
                       diffuse=vec(0.2, 0.2, 0.4),
                       specular=vec(0.8, 0.8, 1),
                       shininess=5,
                       specCoeff=0.1)
        # Green Sphere
        self.addSphere(radius=.7,
                       position=vec(-1, -0.2, -4),
                       color=vec(0, 1, 0),
                       ambient=vec(0.2, 0.4, 0.2),
                       diffuse=vec(0.2, 1, 0.2),
                       specular=vec(0.8, 0.8, 1),
                       shininess=100,
                       specCoeff=1)
        # Red Sphere
        self.addSphere(radius=.7,
                       position=vec(1, 0, -2.3),
                       color=vec(1, 0, 0),
                       ambient=vec(0.4, 0.2, 0.2),
                       diffuse=vec(1, 0.2, 0.2),
                       specular=vec(1, 0.8, 0.8),
                       shininess=100,
                       specCoeff=1)
        # Gray Plane
        self.addPlane(normal=vec(0, 1, 0),
                      position=vec(0, -1, 0),
                      color=COLORS["gray"],
                      ambient=vec(0.3, 0.3, 0.3),
                      diffuse=vec(0.7, 0.7, 0.7),
                      specular=vec(1, 1, 1),
                      shininess=5,
                      specCoeff=0.1)
        """
        self.addPointLight(color=vec(1, 1, 1), position=vec(1, 5, 2))
        self.addDirectionalLight(color=vec(1, 1, 1), lightVector=vec(1, 1, 1))
        # Big Purple Sphere
        self.addSphere(radius=0.9,
                       position=vec(-1.5, 0.3, -0.3),
                       color=vec(1, 0, 1),
                       ambient=vec(0.4, 0.2, 0.4),
                       diffuse=vec(1, 0.2, 1),
                       specular=vec(1, 0.8, 1),
                       shininess=10,
                       specCoeff=.5)
        # Medium Cyan Sphere
        self.addSphere(radius=0.45,
                       position=vec(0, 0, 0),
                       color=vec(0, 1, 1),
                       ambient=vec(0.2, 0.4, 0.4),
                       diffuse=vec(0.2, 1, 1),
                       specular=vec(0.8, 1, 1),
                       shininess=1000,
                       specCoeff=.1)
        # Small Yellow Sphere
        self.addSphere(radius=0.2,
                       position=vec(1, .2, -1.3),
                       color=vec(1, 1, 0),
                       ambient=vec(0.4, 0.4, 0.2),
                       diffuse=vec(1, 1, 0.2),
                       specular=vec(1, 1, 0.8),
                       shininess=100,
                       specCoeff=1)
        # Medium Red Sphere
        self.addSphere(radius=0.7,
                       position=vec(1.5, .2, -2.5),
                       color=vec(1, 0, 0),
                       ambient=vec(0.4, 0.2, 0.2),
                       diffuse=vec(1, 0.2, 0.2),
                       specular=vec(1, 0.8, 0.8),
                       shininess=150,
                       specCoeff=.75)
        # Green Plane
        self.addPlane(normal=vec(0, 1, 0),
                      position=vec(0, -1, 0),
                      color=vec(0, 1, 0),
                      ambient=vec(0.0, 0.3, 0.0),
                      diffuse=vec(0.2, 0.7, 0.2),
                      specular=vec(1, 1, 1),
                      shininess=5,
                      specCoeff=0.1)

    def nearestObject(self, ray):
        """Returns the nearest collision object
           and the distance to the object."""
        distances = [o.intersect(ray) for o in self.objects]
        nearestObj = None
        minDistance = np.inf
        for i in range(len(distances)):
            if distances[i] < minDistance:
                minDistance = distances[i]
                nearestObj = self.objects[i]
        return nearestObj, minDistance

    def shadowed(self, ray, obj):
        """Returns the nearest collision object and the distance to the object,
           excluding obj."""
        distances = [o.intersect(ray) for o in self.objects if o is not obj]
        colObj = None
        distanceToObj = np.inf
        for i in range(len(distances)):
            if distances[i] < distanceToObj and self.objects[i] is not obj:
                distanceToObj = distances[i]
                colObj = self.objects[i]
        return colObj, distanceToObj

    def addSphere(self, radius=0.5,
                  position=vec(0, 0, 0), color=COLORS["blue"],
                  ambient=COLORS["blue"],
                  diffuse=COLORS["black"], specular=COLORS["white"],
                  shininess=0, specCoeff=100):
        self.objects.append(Sphere(radius, position, color,
                                   ambient, diffuse,
                                   specular, shininess, specCoeff))

    def addPlane(self, normal=vec(0, 1, 0),
                 position=vec(0, 0, 0), color=COLORS["gray"],
                 ambient=COLORS["blue"],
                 diffuse=COLORS["black"], specular=COLORS["white"],
                 shininess=0, specCoeff=100):
        self.objects.append(Plane(normal, position, color,
                                  ambient, diffuse,
                                  specular, shininess, specCoeff))

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
