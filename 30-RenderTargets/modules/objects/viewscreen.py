from . import Camera, Mesh
from ..geometry import RectangleGeometry
from ..materials import ImageMaterial
from ..oGL.renderTarget import RenderTarget
from ..utils.vector import normalize, magnitude, vec
from OpenGL.GL import *
import numpy as np

class Viewscreen(Mesh):
    def __init__(self, position, direction,
                 viewPosition, viewDirection,
                 resolution=[512,512],
                 size = [1,1]):
        self.camera = Camera(aspectRatio=resolution[0]/resolution[1])
        
        self.camera.setPosition(viewPosition)
        self.camera.setDirection(viewDirection)
        self.camera.updateViewMatrix()        
        self.size = np.array(size)        
        self.renderTarget = RenderTarget(resolution,
                            properties={"wrap": GL_CLAMP_TO_BORDER})       
        
        geom = RectangleGeometry(width=self.size[0], height=self.size[1])
        mat = ImageMaterial(self.renderTarget.texture,
                            {"useUVColors" : True,
                             "doubleSide" : True})
        super().__init__(geom, mat)
        
        self.setPosition(position)
        self.setDirection(direction)
        
        