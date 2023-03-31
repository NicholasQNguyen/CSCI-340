"""
Author: Liz Matthews Code modified from Developing Graphics Frameworks
with Python and OpenGL by Lee Stemkoski and
Michael Pascale.
"""
from .objects import Moving
from .objects import Object3D
from .utils.vector import vec, magnitude, normalize
from .utils.matrix import Matrix
from .utils.definitions import EPSILON
from pygame.locals import *
import pygame
import numpy as np


class MovementRig(Moving, Object3D):
    """A first-person perspective movement rig.
       WASD to move, ZX to ascend/descend, mouse
       movement to look around.
       WASD/ZX are oriented around the current look
       direction."""
    def __init__(self,
                 speed=15,
                 rotSpeed=np.radians(20)):
        super().__init__(speed, rotSpeed)
        Object3D.__init__(self)
        pygame.init()
        # Initialize attached Object3D
        self.lookAttachment = Object3D()
        self.children = [self.lookAttachment]
        self.lookAttachment.parent = self
        # Keep track of keys
        self.movement = {}
        for k in [K_w, K_a, K_s, K_d, K_q, K_e, K_z, K_x]:
            self.movement[k] = False
        self.velocityMap = {
            K_w: vec(0, 0, -1),
            K_s: vec(0, 0, 1),
            K_a: vec(-1, 0, 0),
            K_d: vec(1, 0, 0),
            K_z: vec(0, -1, 0),
            K_x: vec(0, 1, 0)
        }
        self.numbers = [K_1, K_2, K_3]

    # Override functions from Object3D class
    def add(self, child):
        self.lookAttachment.add(child)

    def remove(self, child):
        self.lookAttachment.remove(child)

    def update(self, deltaTime):
        self.velocity = np.zeros((3))
        # Use the movement dictionary and velocity map to
        # change the velocity
        for key, value in self.movement.items():
            if value:
                self.velocity += self.velocityMap[key] * self.speed * deltaTime
        if magnitude(self.velocity) > EPSILON:
            # Rotate velocity vector to match current rotation.
            # TODO finish this rotation stuff
            pass
        super().update(deltaTime)

    def handleOtherInput(self, event, deltaTime):
        # Set the movement dictionary based on the movement
        #  keys
        if event.type == KEYDOWN and \
           event.key in self.movement:
            self.movement[event.key] = True
        if event.type == KEYDOWN and \
           event.key in self.numbers:
            # TODO change between different materials
            pass
        if event.type == KEYUP and\
           event.key in self.movement:
            self.movement[event.key] = False
        # Set the rotation values based on mouse movement
        if event.type == MOUSEMOTION:
            x, y = pygame.mouse.get_rel()
            x /= 500
            y /= 500
            self.rotation += vec(-y, -x, 0)
