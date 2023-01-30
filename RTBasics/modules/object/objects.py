class Object3D(object):
    def __init__(self, position):
        self.position = position


class Sphere(Object3D):
    def __init__(self, radius, position, ambient, diffuse,
                 specular, shininess, specCoeff):
        super().__init__(self, position)
        self.material = Material(ambient, diffuse, specular, shininess)
        self.radius = radius
        

class Plane(Object3D):
    def __init__(self, normal, position, ambient, diffusse, specular,
                 shininess, specCoeff):
        super().__init__(self, position)
        self.material = Material(ambient, diffuse, specular, shininess)
        self.normal = normal


class Material(object):
    def __init__(ambient, diffuse, specular, shininess):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
