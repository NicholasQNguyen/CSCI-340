"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""
import pygame
from pygame.locals import *
import numpy as np

from modules.oGL.base import Base
from modules.renderer import Renderer
from modules.objects import Scene, Camera, MovingMesh, AxesHelper, GridHelper, Group
from modules.objects.lights import DirectionalLight
from modules.geometry import (BoxGeometry,
                              SphereGeometry,
                              PyramidGeometry,
                              RectangleGeometry,
                              PolygonGeometry,
                              CylinderGeometry)
from modules.geometry.colorFuncs import (randomColor, rainbowGradient,
                                         purple, blue)
from modules.movementRig import MovementRig
from modules.materials import SurfaceMaterial, PointMaterial, LineMaterial
from modules.materials.lambert import LambertMaterial
from modules.materials.phong import PhongMaterial
from modules.utils.vector import vec


class Main(Base):
    def handleOtherInput(self, event):
        self.rig.handleOtherInput(event, self.deltaTime)
        if event.type == KEYDOWN and \
           event.key in self.numbers:
            if event.key == K_1:
                self.materialType = "point"
            elif event.key == K_2:
                self.materialType = "line"
            elif event.key == K_3:
                self.materialType = "surface"
            self.initialize()

    def initialize(self):
        print("Initializing program...")
        self.numbers = [K_1, K_2, K_3]
        if self.materialType is None:   
            self.materialType = "surface"
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=self.aspectRatio)
        self.rig = MovementRig()
        self.rig.add(self.camera)

        # The following does not work until part 2 is completed
        self.rig.setPosition([1, 1, 4])
        self.scene.add(self.rig)
        axes = AxesHelper(axisLength=2)
        self.scene.add(axes)
        grid = GridHelper(size=20, gridColor=[1, 1, 1],
                          centerColor=[1, 1, 0])
        grid.setRotateX(-np.pi/2)
        self.scene.add(grid)
        # Floor
        if self.materialType == "point":
            floorMaterial = PointMaterial({"useVertexColors": True})
        elif self.materialType == "line":
            floorMaterial = LineMaterial({"useVertexColors": True})
        else:
            floorMaterial = SurfaceMaterial({"useVertexColors": True})
        floorGeometry = RectangleGeometry(width=30, height=30)
        floorMesh = MovingMesh(floorGeometry, floorMaterial)
        floorMesh.setRotate(3 * np.pi / 2, 0, 0)
        floorMesh.setRotationalSpeed(0)
        self.scene.add(floorMesh)
        # Purple Pyramid
        if self.materialType == "point":
            material = LambertMaterial({"useVertexColors": True})
        elif self.materialType == "line":
            material = LineMaterial({"useVertexColors": True})
        else:
            material = LambertMaterial({"useVertexColors": True})
        geometry = PyramidGeometry(colorFunction=purple)
        mesh = MovingMesh(geometry, material)
        mesh.setRotVel(vec(0.0337, 0.0514, 0))
        mesh.setRotationalSpeed(2)
        mesh.setPosition([0, 1, -4])
        self.scene.add(mesh)
        # Box
        if self.materialType == "point":
            material = PhongMaterial({"useVertexColors": True})
        elif self.materialType == "line":
            material = LineMaterial({"useVertexColors": True})
        else:
            material = LambertMaterial({"useVertexColors": True})
        geometry = BoxGeometry(width=3, height=3, depth=3)
        mesh = MovingMesh(geometry, material)
        mesh.setRotVel(vec(0, 1, 0))
        mesh.setRotationalSpeed(4)
        mesh.setPosition([0, 0, 0])
        self.scene.add(mesh)
        # Lights
        self.scene.add(DirectionalLight(direction = vec(0, -1, 0)))

    def update(self):
        """Most of the work is in scene, rig, and renderer!"""
        self.scene.update(self.deltaTime)
        self.rig.update(self.deltaTime)
        self.renderer.render(self.scene, self.camera)


if __name__ == '__main__':
    Main(fullScreen=False).run()
