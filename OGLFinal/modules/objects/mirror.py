import numpy as np
from OpenGL.GL import *

from ..geometry.primitives import RectangleGeometry
from ..materials.imageMaterial import ImageMaterial
from .mesh import Mesh
from . import Camera
from ..utils.vector import vec, normalize, magnitude
from ..utils.matrix import Matrix
from ..utils.definitions import EPSILON
from ..renderTarget import RenderTarget


class Mirror(Mesh):
    def __init__(self, position, direction, viewPosition, viewDirection,
                 resolution=[512,512], size = [1,1]):
        self.normal = viewDirection
        # TODO make not a hard coded value
        self.rt = vec(1, 0, 0)
        self.up = vec(0, 1, 0)
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
        left = -1
        right = 1
        bottom = -1
        top = 1
        viewPosition = movementRig.position
        viewDir = self.position - viewPosition
        fwdPart = np.dot(viewDir, self.normal) * self.normal
        mirroredViewPos = movementRig.position + fwdPart * 2
        self.camera.setPosition(mirroredViewPos)
        focal = normalize(viewDir) * magnitude(fwdPart)
        self.lookAt(focal)
        if magnitude(fwdPart) < EPSILON:
            return
        ldist = np.dot((left - focal), self.rt)
        rdist = np.dot((right - focal), self.rt)
        tdist = np.dot((top - focal), self.up)
        bdist = np.dot((bottom - focal), self.up)
        self.camera.projectionMatrix = Matrix.makePerspectiveAsymmetric(left=ldist, right=rdist, bottom=bdist, top=tdist, near=magnitude(fwdPart))
        self.camera.updateViewMatrix()
