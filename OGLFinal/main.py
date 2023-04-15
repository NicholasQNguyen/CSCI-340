"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""
import pygame
from pygame.locals import *
import numpy as np
import os

from modules.oGL.base import Base
from modules.renderer import Renderer
from modules.objects import Scene, Camera, MovingMesh, AxesHelper, GridHelper, Group
from modules.objects.lights import DirectionalLight
from modules.geometry import (BoxGeometry,
                              SphereGeometry,
                              PyramidGeometry,
                              RectangleGeometry,
                              PolygonGeometry,
                              WobblyGeometry,
                              CylinderGeometry,
                              NoisePlaneGeometry)
from modules.geometry.objectFile import ObjectFileGeometry
from modules.geometry.colorFuncs import (randomColor, rainbowGradient,
                                         purple, blue)
from modules.objects.viewscreen import Viewscreen
from modules.objects.mirror import Mirror 
from modules.movementRig import MovementRig
from modules.materials import SurfaceMaterial, PointMaterial, LineMaterial
from modules.materials.lambert import LambertMaterial
from modules.materials.phong import PhongMaterial
from modules.materials.mountainMaterial import MountainMaterial
from modules.materials.imageMaterial import ImageMaterial
from modules.utils.vector import vec
from modules.texture import Texture

IMAGE_FOLDER = os.path.join("resources", "images")
OBJ_FOLDER = os.path.join("resources", "models")
BRICKS_PATH = os.path.join(IMAGE_FOLDER, "bricks.png")
CIRCLES_PATH = os.path.join(IMAGE_FOLDER, "circles.png")
JEWELS_PATH = os.path.join(IMAGE_FOLDER, "jewels.png")
BRICKS = Texture(BRICKS_PATH)
CIRCLES = Texture(CIRCLES_PATH)
JEWELS = Texture(JEWELS_PATH)
ICE_CREAM = os.path.join(OBJ_FOLDER, "icecream.obj")


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
        self.rig.setPosition([1, 6, 4])
        self.scene.add(self.rig)
        axes = AxesHelper(axisLength=2)
        self.scene.add(axes)
        grid = GridHelper(size=20, gridColor=[1, 1, 1],
                          centerColor=[1, 1, 0])
        grid.setRotateX(-np.pi/2)
        self.scene.add(grid)
        # Floor
        #  """
        floorMaterial = MountainMaterial({"useVertexColors" : True})
        floorGeometry = NoisePlaneGeometry(width=30, height=30)
        floorMesh = MovingMesh(floorGeometry, floorMaterial)
        floorMesh.setRotate(3 * np.pi / 2, 0, 0)
        floorMesh.setRotationalSpeed(0)
        self.scene.add(floorMesh)
        # """
        # Box
        material = PhongMaterial({"useVertexColors": False})
        geometry = BoxGeometry(width=3, height=3, depth=3)
        mesh = MovingMesh(geometry, material)
        mesh.setRotVel(vec(1, 0, 0))
        mesh.setRotationalSpeed(2)
        mesh.setPosition([6, 3, 0])
        self.scene.add(mesh)
        # Sphere
        geometry = SphereGeometry()
        material = PhongMaterial({"useVertexColors" : False,
                                  "useFaceNormals" : True})
        self.mesh = MovingMesh(geometry, material)
        self.mesh.setRotVel(vec(1, 0, 0))
        self.mesh.setRotationalSpeed(2)
        self.mesh.position =[0,3,0]
        self.scene.add(self.mesh)
        # Image box
        geometry = BoxGeometry()
        material = ImageMaterial(BRICKS)
        self.mesh = MovingMesh(geometry, material)
        self.mesh.setRotVel(vec(1, 1, 0))
        self.mesh.setRotationalSpeed(1)
        self.mesh.position =[4, 3, 0]
        self.scene.add(self.mesh)
        # Wobbly thing
        geometry = WobblyGeometry()
        material = PhongMaterial({"useVertexColors" : False,
                                  "useFaceNormals" : True})
        self.mesh = MovingMesh(geometry, material)
        self.mesh.setRotVel(vec(1, 0, 1))
        self.mesh.setRotationalSpeed(2)
        self.mesh.position =[0,3,5]
        self.scene.add(self.mesh)
        # Viewport thing
        self.mirror = Mirror(vec(0, 5, 0), vec(0, 0, -1),
                               vec(0, 0, -1), vec(0, 0, -1))
        self.scene.add(self.mirror)
        # Obj test
        """
        geometry = ObjectFileGeometry(ICE_CREAM)
        material = PhongMaterial({"useVertexColors" : False,
                                  "useFaceNormals" : True})
        self.mesh = MovingMesh(geometry, material)
        self.mesh.position =[2,3,0]
        self.scene.add(self.mesh)
        """
        # Lights
        self.scene.add(DirectionalLight(direction = vec(1, 0, 0)))

    def update(self):
        """Most of the work is in scene, rig, and renderer!"""
        self.scene.update(self.deltaTime)
        self.rig.update(self.deltaTime)
        self.renderer.render(self.scene, self.mirror.camera,
                             self.mirror.renderTarget)
        self.mirror.updateView(self.rig)
        self.renderer.render(self.scene, self.camera)


if __name__ == '__main__':
    Main(fullScreen=False).run()
