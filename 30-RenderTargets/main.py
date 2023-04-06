"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from modules.oGL.base import Base
from modules.renderer import Renderer
from modules.objects import *
from modules.geometry import *
from modules.materials import *
from modules.movementRig import MovementRig
from modules.texture import Texture
from modules.utils.matrix import Matrix
from modules.utils.vector import vec

import pygame
import os
import numpy as np

class Main(Base):
    def handleOtherInput(self, event):
        self.rig.handleOtherInput(event, self.deltaTime)
        
    def initialize(self):        
        print("Initializing program...")
        
        
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        
        self.otherRenders = []
        
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=self.aspectRatio)
        
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 1, 4])
        self.scene.add(self.rig)
        
        geometry = BoxGeometry()
        material = LambertMaterial({"useVertexColors" : True})
        mesh = MovingMesh(geometry, material)
        mesh.setRotVel((0.3, 0.2, 0))
        mesh.setPosition([0,2,-1])
        self.scene.add(mesh)
        
    
        
        self.light = DirectionalLight(color=vec(1, 1, 1),
                                 direction=normalize(vec(-0.25,-0.5,-1)))
        self.scene.add(self.light)
        
        floor = PlaneGeometry(width=20, height=20,
                              widthSegments=20, heightSegments=20,
                              colorFunction=rainbowGradient)
        tex = Texture("rainbow.jpg")
        tex2 = Texture("bricks.png")
        mat = LambertMaterial({"useVertexColors" : True})
        imageMat = ImageMaterial(tex2)
        sphere = SphereGeometry()
        
        mesh = Mesh(floor, imageMat)
        mesh2 = Mesh(sphere, imageMat)
        mesh.setRotateX(-0.5 * np.pi)
        mesh.setPosition(vec(0,-0.2,0))
        mesh2.setPosition(vec(0,2,0))
        self.scene.add(mesh)
        self.scene.add(mesh2)
        
        
                
        print("Done initializing")
        
    def update(self):
        """Most of the work is in scene, rig, and renderer!"""
        
        self.scene.update(self.deltaTime)
        self.rig.update(self.deltaTime)     
        
        self.renderer.render(self.scene, self.camera)
        
        
if __name__ == '__main__':
    Main(fullScreen=False).run()
