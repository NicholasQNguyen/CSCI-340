import numpy as np

from .object3D import Object3D
from ..utils.vector import vec, normalize


class Light(Object3D):
    DUMMY = 1
    DIRECTIONAL = 2
    POINT = 3

    def __init__(self, color=vec(1, 1, 1),
                 attenuation=vec(1, 0, 0),
                 lightType=1):
        super().__init__()
        self.lightType = lightType
        self.color = vec(*color)
        self.attentuation = vec(*attenuation)       


class DirectionalLight(Light):
    def __init__(self, direction, color=vec(1, 1, 1)):
        super().__init__(color=color,
                         lightType=Light.DIRECTIONAL)
        self.setDirection(direction)

    def setDirection(self, direction):
        targetPosition = self.getPosition() + direction
        self.lookAt(targetPosition)

    def lookAt(self, targetPosition):
        diff = targetPosition - self.position
        lookFwd = normalize(diff)
        pitch = np.arcsin(-lookFwd[1])
        yaw = np.arctan2(lookFwd[0], lookFwd[2])
        self.rotation[1] = yaw
        self.rotation[0] = pitch


class PointLight(Light):
    def __init__(self, direction, color=vec(1, 1, 1),
                 attentuation=vec(1, 0, 0.1)):
        super().__init__(color=color,
                         attenuation=attenuation,
                         lightType=Light.POINT)
        self.position = vec(*position)
