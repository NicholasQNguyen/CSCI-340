import numpy as np
from OpenGL.GL import *

from ..geometry.primitives import RectangleGeometry
from ..materials.imageMaterial import ImageMaterial
from .mesh import Mesh
from . import Camera
from ..utils.vector import vec, normalize, magnitude
from ..renderTarget import RenderTarget


class Mirror(Mesh):
    def __init__(self, position, direction, viewPosition, viewDirection,
                 resolution=[512,512], size = [1,1]):

        self.camera = Camera(aspectRatio=resolution[0]/resolution[1])
        self.camera.setPosition(viewPosition)
        self.camera.setDirection(viewDirection)
        self.setScaleAsymmetric(-1, 0, 0)
        self.camera.updateViewMatrix()
        self.size = np.array(size)
        self.renderTarget = RenderTarget(resolution,
                            properties={"wrap": GL_CLAMP_TO_BORDER})
        geom = RectangleGeometry(width=self.size[0], height=self.size[1])
        mat = ImageMaterial(self.renderTarget.texture)
        """
                {"useUVColors" : True,
                 "shaded" : False,
                 "doubleSide" : True})
        """
        super().__init__(geom, mat)
        self.setPosition(position)
        self.setDirection(direction)

    def updateView(self, movementRig):
        viewPosition = movementRig.position
        viewDir = self.position - viewPosition
        fwdPart = np.dot(viewDir, self.normal) * self.normal
        mirroredViewPos = movementRig.position + fwdPart * 2
        self.camera.setPosition(mirroredViewPos)
        focal = normalize(viewDir) * fwdPart
        mirror.lookAt(focal)
        if fwdPart < EPSILON:
            return
