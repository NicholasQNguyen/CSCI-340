"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""
import pygame
import numpy as np

from modules.oGL.base import Base
from modules.renderer import Renderer
from modules.objects import Scene, Camera, MovingMesh, AxesHelper, GridHelper
from modules.geometry import BoxGeometry, SphereGeometry, PyramidGeometry, RectangleGeometry
from modules.geometry.colorFuncs import randomColor, rainbowGradient, purple, blue
from modules.movementRig import MovementRig
from modules.materials import SurfaceMaterial
from modules.utils.vector import vec


class Main(Base):
    def handleOtherInput(self, event):
        self.rig.handleOtherInput(event, self.deltaTime)

    def initialize(self):
        print("Initializing program...")
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
        grid = GridHelper(size=20, gridColor=[1,1,1],
        centerColor=[1,1,0])
        grid.setRotateX(-np.pi/2)
        self.scene.add(grid)
        # geometry = BoxGeometry()
        # geometry = SphereGeometry(colorFunction=rainbowGradient)
        # Purple Pyramid
        material = SurfaceMaterial({"useVertexColors" : True})
        geometry = PyramidGeometry(colorFunction=purple)
        mesh = MovingMesh(geometry, material)
        mesh.setRotVel(vec(0.0337, 0.0514, 0))
        mesh.setRotationalSpeed(2)
        mesh.setPosition([0,1, -4])
        self.scene.add(mesh)
        # Floor
        floorMaterial = SurfaceMaterial({"useVertexColors" : True})
        floorGeometry = RectangleGeometry(width=30, height=30)
        floorMesh = MovingMesh(floorGeometry, floorMaterial)
        floorMesh.setRotate(3 * np.pi / 2, 0, 0)
        floorMesh.setRotationalSpeed(0)
        self.scene.add(floorMesh)
        # Bowl
        sphereMaterial = SurfaceMaterial({"useVertexColors" : True}, doubleSide=True)
        sphereGeometry = SphereGeometry(radius=.5,
                                        uStart=0, uEnd=np.pi,
                                        vStart=-np.pi/2, vEnd=np.pi/2,
                                        colorFunction=randomColor)
        sphereMesh = MovingMesh(sphereGeometry, sphereMaterial)
        sphereMesh.setRotVel(vec(0.0337, 0.0514, 0))
        sphereMesh.setRotationalSpeed(5)
        sphereMesh.setPosition([4,1, -4])
        sphereMesh.setRotate(0, 0, 3*np.pi/2)
        self.scene.add(sphereMesh)

    def update(self):
        """Most of the work is in scene, rig, and renderer!"""
        self.scene.update(self.deltaTime)
        self.rig.update(self.deltaTime)
        self.renderer.render(self.scene, self.camera)


if __name__ == '__main__':
    Main(fullScreen=False).run()
