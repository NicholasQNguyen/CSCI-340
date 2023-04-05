from .abstract import AbstractMaterial
from .texture import Texture
from ..oGL.shaderCode import lightCalcPhong, lightStruct, vertexShaderWithNormals, imageVertexShader, imageFragmentShader
from OpenGL.GL import *

class ImageMaterial(AbstractMaterial):
    """Contains basic shader codes."""
    def __init__(self, texture=None, properties={}):
        self.texture = Texture(texture)
        
        vertexShaderCode = \
        imageVertexShader

        fragmentShaderCode = \
        lightStruct + lightCalcPhong + imageFragmentShader

        super().__init__(vertexShaderCode, fragmentShaderCode)
        self.addUniform("Light", "light0", None )
        self.addUniform("Light", "light1", None )
        self.addUniform("Light", "light2", None )
        self.addUniform("Light", "light3", None )        
        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.addUniform("vec3", "viewPosition", [0,0,0])
        self.addUniform("bool", "useUVColors", True) 
        self.addUniform("float", "ambMul", 0.3)
        self.addUniform("float", "specMul", 1.5)
        self.addUniform("float", "specularStrength", 1)
        self.addUniform("float", "shininess", 300)
        self.addUniform("bool", "useFaceNormals", False)
        self.addUniform("bool", "useVertexColors", False)
        self.locateUniforms()
        self.texture.uploadData()
