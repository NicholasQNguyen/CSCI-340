"""
Author: Liz Matthews
"""

from . import AbstractMaterial
from ..oGL.shaderCode import lightStruct, lightCalcLambert, vertexShaderWithNormals
from OpenGL.GL import *

class LambertMaterial(AbstractMaterial):
    def __init__(self, properties={}):
        vShaderCode = vertexShaderWithNormals
        
        fShaderCode = lightStruct + lightCalcLambert + """
        uniform float ambMul;
        in vec3 color;
        in vec3 normal;
        in vec3 position;
        out vec4 fragColor;
        void main()
        {
            vec3 diffuse = color;
            vec3 total = diffuse * ambMul;
            total = lightCalc(light0, total, diffuse,
                               position, normal);
            total = lightCalc(light1, total, diffuse,
                               position, normal);
            total = lightCalc(light2, total, diffuse,
                               position, normal);
            total = lightCalc(light3, total, diffuse,
                               position, normal);
            
            fragColor = vec4(total, 1.0);
        }
        """
        
        super().__init__(vShaderCode, fShaderCode)
        
        self.addUniform("Light", "light0", None)
        self.addUniform("Light", "light1", None)
        self.addUniform("Light", "light2", None)
        self.addUniform("Light", "light3", None)        
        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.addUniform("float", "ambMul", 0.3)
        self.addUniform("bool", "useVertexColors", False)
        self.addUniform("bool", "useFaceNormals", False)
        
        self.locateUniforms()
        
        # Render vertices as surface
        self.settings["drawStyle"] = GL_TRIANGLES
        
        # Render both sides? default: front side only
        # Vertices ordered counterclockwise
        self.settings["doubleSide"] = False
        
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
