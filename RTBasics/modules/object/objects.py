class Object3D(object):
    def __init__(self, position, castsShadow=True):
        self.position = position
        self.castsShadow = castsShadow


class Sphere(Object3D):
    def __init__(self, radius, position, ambient, diffuse,
                 specular, shininess, specCoeff):
        super().__init__(position, True)
        self.material = Material(ambient, diffuse, specular, shininess)
        self.radius = radius

    def getRadius(self):
        return self.radius
        

class Plane(Object3D):
    def __init__(self, normal, position, ambient, diffuse, specular,
                 shininess, specCoeff):
        super().__init__(position, False)
        self.material = Material(ambient, diffuse, specular, shininess)
        self.normal = normal

    def getNormal(self):
        return self.normal


class Material(object):
    def __init__(self, ambient, diffuse, specular, shininess):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
