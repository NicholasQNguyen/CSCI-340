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
from modules.objects import Scene, Camera, Mesh
from modules.geometry import BoxGeometry, CylinderGeometry, PolygonGeometry
from modules.materials import SurfaceMaterial
from modules.utils.vector import vec


class Main(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=self.aspectRatio)
        self.camera.position = vec(0, 0, 4)
        self.scene.add(self.camera)
        geometry = CylinderGeometry()
        material = SurfaceMaterial({"useVertexColors": True})
        mesh = Mesh(geometry, material)
        mesh.rotation[0] = 0.25 * np.pi
        mesh.rotation[1] = 0.2 * np.pi
        mesh.position = vec(0, 1, -4)
        self.scene.add(mesh)

    def update(self):
        """Most of the work is in scene, rig, and renderer!"""
        self.scene.update(self.deltaTime)
        self.renderer.render(self.scene, self.camera)


if __name__ == '__main__':
    Main(fullScreen=False).run()
