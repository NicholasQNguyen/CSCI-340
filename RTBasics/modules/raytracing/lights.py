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
    def __init__(self, color):
        super().__init__(color, position)

    def getVectorToLight(self, point):
        """Returns a vector pointing towards the light"""
        pass
    
    def getDistance(self, point):
        """Returns the distance to the light"""
        pass

class DirectionalLight(AbstractLight):
    def __init__(self, color):
        super().__init__(color, position)

    def getVectorToLight(self, point):
        """Returns a vector pointing towards the light"""
        pass
    
    def getDistance(self, point):
        """Returns the distance to the light"""
        pass
