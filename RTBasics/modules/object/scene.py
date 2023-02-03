class Scene(object):
    def __init__(self, camera):
        self.cam = camera
        self.objectList = []
        self.lightList = []

    def addObject(self, newObject):
        self.objectList.append(newObject)

    def addLight(self, newLight):
        self.lightList.appedn(newLight)

    def nearestObject(self, ray):
        pass

    def shadowed(self, obj, ray):
        pass
