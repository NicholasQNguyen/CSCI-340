"""
Author: Liz Matthews
"""

from . import AbstractMaterial
from ..oGL.shaderCode import lightCalcLambert, lightStruct, vertexShaderWithNormals
from OpenGL.GL import *

class ImageMaterial(AbstractMaterial):
    def __init__(self, texture=None, properties={}):
        vShaderCode = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition; 
        in vec2 vertexUV;
        out vec2 UV;
        void main() {
            gl_Position = projectionMatrix * viewMatrix *
                          modelMatrix * vec4(vertexPosition, 1);
                
            UV = vertexUV;
        }
     
        """
        fShaderCode = """
        
        uniform sampler2D texture;
        in vec2 UV;
        out vec4 fragColor;
        void main()
        {
            vec4 diffuse = texture2D(texture, UV);
            if (diffuse.a < 0.01)
                discard;
            
            fragColor = diffuse;
        }
        """
        
        super().__init__(vShaderCode, fShaderCode)
        
        self.addUniform("sampler2D", "texture", [texture.textureRef, 1])
        
        self.locateUniforms()
        
        # Render vertices as surface
        self.settings["drawStyle"] = GL_TRIANGLES
        
        # Render both sides? default: front side only
        # Vertices ordered counterclockwise
        self.settings["doubleSide"] = True
        
        # Render triangles as wireframe?
        self.settings["wireframe"] = False
        
        # Line thickness for wireframe rendering
        self.settings["lineWidth"] = 1
        self.setProperties(properties)
        
    def updateRenderSettings(self):
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
            
        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        glLineWidth(self.settings["lineWidth"])  
