class AbstractLight(object):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        

class PointLight(AbstractLight):
    pass


class DirectionalLight(AbstractLight):
    pass
