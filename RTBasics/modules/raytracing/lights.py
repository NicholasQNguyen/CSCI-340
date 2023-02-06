from abc import ABC, abstractmethod
from ..utils.vector import vec, magnitude


class AbstractLight(ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def getColor(self):
        """Returns the color of the light"""
        return self.color

    @abstractmethod
    def getVectorToLight(self, point):
        """Returns a vector pointing towards the light"""
        pass

    @abstractmethod
    def getDistance(self, point):
        """Returns the distance to the light"""
        pass


class PointLight(AbstractLight):
    def __init__(self, color, position=vec(0, 0, 0)):
        super().__init__(color, position)

    def getVectorToLight(self, point):
        """Returns a vector pointing towards the light"""
        return point - self.position

    def getDistance(self, point):
        """Returns the distance to the light"""
        return magnitude(point - self.position)


class DirectionalLight(AbstractLight):
    def __init__(self, color, position=vec(0, 0, 0)):
        super().__init__(color, position)
        self.lightVec = self.position - vec(0, 0, 0)

    def getVectorToLight(self, point):
        """Returns a vector pointing towards the light"""
        return self.lightVec

    def getDistance(self, point):
        """Returns the distance to the light"""
        return magnitude(point - self.position)