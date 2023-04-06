"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from .mesh import Mesh
from ..utils.vector import vec, magnitude, normalize
from ..utils.definitions import EPSILON
from ..utils.matrix import Matrix
from pygame.locals import *
import numpy as np

class Moving(object):
    """An abstract class for inheritance. Updates its
       position and rotation based on velocities. Has
       two velocities, rotationalVelocity and velocity.
       Additionally, has two maximum speeds, one for
       each velocity."""
       
    def __init__(self, speed=1, rotSpeed=np.radians(20)):
        """Initializes maximum speed and velocities."""
        self.speed = speed
        self.rotationalSpeed = rotSpeed
        
        self.velocity = np.zeros((3))
        self.rotationalVelocity = np.zeros((3))        
        
    def setVelocity(self, velocity):
        """Sets the velocity to the given parameter."""
        self.velocity = vec(*velocity)
    
    def setRotVel(self, rotVel):
        """Sets the rotational velocity to the given
           parameter."""
        self.rotationalVelocity = vec(*rotVel)
        
    def update(self, deltaTime):
        """If either velocity has a magnitde greater than
           zero, calculates the distance or rotation achived
           in deltaTime and uses the velocity to add to the
           current values in rotation or position."""
        
        if magnitude(self.rotationalVelocity) > EPSILON:
            rv = normalize(self.rotationalVelocity) * self.rotationalSpeed * deltaTime
            self.rotation += rv
            
        if magnitude(self.velocity) > EPSILON:
            v = normalize(self.velocity) * self.speed * deltaTime
            self.position += v

            
class MovingMesh(Moving, Mesh):
    """Uses multiple inheritance to obtain the behaviors of
       both Moving and Mesh classes."""
       
    def __init__(self, geometry, material, speed=1, rotSpeed=np.radians(20)):
        super().__init__(speed, rotSpeed)
        Mesh.__init__(self, geometry, material)


class NoiseAnimatedMesh(Mesh):
    def __init__(self, geometry, material, speed=1, direction=np.array((0,1))):
        super().__init__(geometry, material)
        self.speed     = speed
        self.direction = direction
        self.start = np.array((0,0))
        
    def update(self, deltaTime):
        self.start += self.direction * self.speed * deltaTime
        
    