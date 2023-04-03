"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from modules.oGL.base import Base
from modules.renderer import Renderer
from modules.objects import Scene, Camera, Mesh, DirectionalLight
from modules.geometry import *
from modules.materials import LambertMaterial, PhongMaterial
from modules.utils.matrix import Matrix
from modules.utils.vector import vec

import pygame
import os
import numpy as np

class Main(Base):
        
    def initialize(self):        
        print("Initializing program...")
                
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=self.aspectRatio)
        
        self.camera.position =[0, 1, 4]
        self.scene.add(self.camera)
        
        
        geometry = SphereGeometry()
        material = PhongMaterial({"useVertexColors" : False,
                                  "useFaceNormals" : True})
        self.mesh = Mesh(geometry, material)
        self.mesh.position =[0,0.5,-1]
        self.scene.add(self.mesh)
        
        
        self.light = DirectionalLight(color=vec(1, 1, 1),
                                 direction=vec(0,-1,0))
        self.scene.add(self.light)

        
    def update(self):
        """Most of the work is in scene, rig, and renderer!"""
        
        self.mesh.rotation += vec(0.3, 0.2, 0) * self.deltaTime
        
        self.scene.update(self.deltaTime)
        self.renderer.render(self.scene, self.camera)
        
        
if __name__ == '__main__':
    Main(fullScreen=False).run()
