"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from .basic import BasicMaterial 
from OpenGL.GL import *

class LineMaterial(BasicMaterial):
    def __init__(self, properties={}, doubleSide=False):
        super().__init__()
        
        # Render vertices as continuous line by default
        self.settings["drawStyle"] = GL_LINE_STRIP
        
        # Render both sides? default: front side only
        # Vertices ordered counterclockwise
        self.settings["doubleSide"] = doubleSide

        # Line thickness
        self.settings["lineWidth"] = 1
        
        # Line type: "connected" | "loop" | "segments"
        self.settings["lineType"] = "connected"
        
        self.setProperties(properties)
        
    def updateRenderSettings(self):
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
        glLineWidth(self.settings["lineWidth"])
        if self.settings["lineType"] == "connected":
            self.settings["drawStyle"] = GL_LINE_STRIP
        elif self.settings["lineType"] == "loop":
            self.settings["drawStyle"] = GL_LINE_LOOP
        elif self.settings["lineType"] == "segments":
            self.settings["drawStyle"] = GL_LINES
        else:
            raise Exception(f"Unknown LineMaterial draw style {self.settings['lineType']}.")
        
