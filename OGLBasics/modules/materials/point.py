"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from .basic import BasicMaterial 
from OpenGL.GL import *

class PointMaterial(BasicMaterial):
    def __init__(self, properties={}, doubleSide=False):
        super().__init__()
        
        # Render vertices as points
        self.settings["drawStyle"] = GL_POINTS
        
        # Render both sides? default: front side only
        # Vertices ordered counterclockwise
        self.settings["doubleSide"] = doubleSide

        # Width and height of points, in pixels
        self.settings["pointSize"] = 8
        
        # Draw points as rounded
        self.settings["roundedPoints"] = False
        self.setProperties(properties)
        
    def updateRenderSettings(self):
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        glPointSize(self.settings["pointSize"])
        if self.settings["roundedPoints"]:
            glEnable(GL_POINT_SMOOTH)
        else:
            glDisable(GL_POINT_SMOOTH)
            
