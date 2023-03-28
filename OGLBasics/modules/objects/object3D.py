"""
Author: Liz Matthews
Code modified from
https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""
from ..oGL.attribute import Attribute
from ..oGL.uniform import Uniform
from ..utils.vector import vec
from ..utils.matrix import Matrix

import numpy as np
from OpenGL.GL import *

x = 0
y = 1
z = 2


class Object3D(object):        
    """As described in Developing Graphics Frameworks
       with Python and OpenGL by Lee Stemkoski and
       Michael Pascal.
       
       Edits include change to use absolute transformation
       values instead of accumulative values."""
    def __init__(self):
        self.parent   = None
        self.children = []
        self.rotation = vec(0,0,0)
        self.position = vec(0,0,0)
        self.scale    = vec(1,1,1)
    
    def update(self, deltaTime=0):
        """Stub method so that all objects can be called
           to update even if they do not need to update."""
        pass
        
    def add(self, child):
        self.children.append(child)
        child.parent = self
    
    def remove(self, child):
        self.children.remove(child)
        child.parent = None
    
    def getDescendantList(self):
        """Depth-first traversal to obtain a list of descendants."""
        descendants = []
        nodesToProcess = [self]
        while len(nodesToProcess) > 0:
            node = nodesToProcess.pop(0)
            descendants.append(node)
            nodesToProcess = node.children + nodesToProcess
            
        return descendants
    
    ## Absolute transformation calculation ##
    def getWorldMatrix(self):
        """Obtain the final transformation matrix based on all
           transforms in parent chain."""
        t = Matrix.makeIdentity()
        if self.parent == None:
            return t
        else:
            t = Matrix.translate(t,
                             self.position[x],
                             self.position[y],
                             self.position[z])
            t = Matrix.rotate(t,
                          self.rotation[x],
                          self.rotation[y],
                          self.rotation[z])
            return self.parent.getWorldMatrix() @ t
    
    ## Mutator methods to adjust absolute values for translations ##
    def setPosition(self, newPosition):
        self.position = newPosition

    def setRotateX(self, angle):
        self.rotation[x] = angle

    def setRotateY(self, angle):
        self.rotation[y] = angle

    def setRotateZ(self, angle):
        self.rotation[z] = angle

    def setRotate(self, xAngle, yAngle, zAngle):
        self.setRotateX(xAngle)
        self.setRotateY(YAngle)
        self.setRotateZ(ZAngle)

    def setScale(self, scale):
        self.scale = scale

    def setScaleAsymmetric(self, xScale, yScale, zScale):
        self.scale[x] = xScale
        self.scale[y] = yScale
        self.scale[z] = zScale
