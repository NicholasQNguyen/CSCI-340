from . import AbstractGeometry


class ObjectFileGeometry(AbstractGeometry):
    def __init__(self, objFileName):
        super().__init__()
        self.objFileName = objFileName
        
        fp = open(self.objFileName, "r")
        
        self.vertices  = []
        self.faces     = []
        self.normals   = []
        self.texcoords = []
        
        for line in fp:
            if line[0] == "#":
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == "v":
                self.vertices.append(map(float, values[1:4]))
            elif values[1] == "vn":
                self.normals.append(map(float, values[1:4]))
            elif values[0] == "vt":
                self.texcoords.append(map(float, values[1:3]))
            elif values[0] == "f":
                faceVertices = []
                normals = []
                texcoords = []
                for v in values[1:]:
                    w = v.split("/")
                    faceVertices.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        normals.append(int(w[2]))
                    else:
                        normals.append(0)
                self.faces.append((faceVertices, texcoords, normals))
        vertices = []
        normals = []
        texcoords = []
        for face in self.faces:
            vertices.append(face[0])
            normals.append(face[1])
            texcoords.append(face[2])
            print("FACE", face)
        for current in range(1, len(vertices) -1):
            p0 = 0
            p1 = current
            p2 = current + 1
            for i in [0, current, current + 1]:
                pass
        """
        When add atributes to geometry.
        If you have vertexUVCoords, use vec2 not vec3.
        """
