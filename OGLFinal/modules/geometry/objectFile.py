class ObjectFileGeometery(AbstractGeometry):
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
                vertex = float(values[1:4])
            elif values[1] == "vn":
                normal = float(values[1:4])
            elif values[0] == "vt":
                textureCoordinate = float(values[1:3])
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
                self.texcoords.append(texcoords)
                self.faces.append(faceVertices)
                self.normals.append(normals)
        for face in self.faces:
            
