from . import Object3D
from ..utils.vector import vec


class Light(Object3D):
    DUMMY = 1
    DIRECTIONAL = 2
    POINT = 3
    def __init__(self, color=vec(1,1,1),
                 attenuation=vec(1,0,0),
                 lightType = 1):
        super().__init__()
        self.lightType   = lightType
        self.color       = vec(*color)
        self.attenuation = vec(*attenuation)

class DirectionalLight(Light):
    def __init__(self, direction, color=vec(1,1,1)):
        super().__init__(color=color,
                         lightType=Light.DIRECTIONAL)
        self.setDirection(direction)

class PointLight(Light):
    def __init__(self, position, color=vec(1,1,1),
                 attenuation=vec(1,0,0.1)):
        super().__init__(color=color,
                         attenuation=attenuation,
                         lightType=Light.POINT)
        self.position = vec(*position)