"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from .abstract import AbstractMaterial
from ..oGL.shaderCode import lightCalcPhong, lightStruct, vertexShaderWithNormals
from OpenGL.GL import *

class PhongMaterial(AbstractMaterial):
    def __init__(self, properties={}):
        vShaderCode = vertexShaderWithNormals
        
        fShaderCode = lightStruct + lightCalcPhong + """
        uniform float ambMul; 
        uniform float specMul;
        uniform float alpha;
        uniform bool shaded;
        in vec3 position;
        in vec3 normal;
        in vec3 color;
        out vec4 fragColor;
        void main()
        {
            vec3 diffuse = color;
            vec3 specular = (diffuse + vec3(0.1,0.1,0.1)) * specMul;
            vec3 total =  diffuse * ambMul;
            total = lightCalc(light0, total, color, specular,
                              position, normal);
            total = lightCalc(light1, total, color, specular,
                              position, normal);
            total = lightCalc(light2, total, color, specular,
                              position, normal);
            total = lightCalc(light3, total, color, specular,
                              position, normal);
            
            fragColor = vec4(total, alpha);
        }
        """
        
        super().__init__(vShaderCode, fShaderCode)
        
        self.addUniform("Light", "light0", None )
        self.addUniform("Light", "light1", None )
        self.addUniform("Light", "light2", None )
        self.addUniform("Light", "light3", None )        
        self.addUniform("mat4", "projectionMatrix", [0, 0, 0])
        self.addUniform("mat4", "viewMatrix", [0, 0, 0])
        self.addUniform("mat4", "modelMatrix", [0, 0, 0])
        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.addUniform("vec3", "viewPosition", [0,0,0])
        self.addUniform("vec2", "repeatUV", [0, 0])
        self.addUniform("vec2", "offsetUV", [0, 0])
        self.addUniform("float", "ambMul", 0.3)
        self.addUniform("float", "specMul", 1.5)
        self.addUniform("float", "specularStrength", 1)
        self.addUniform("float", "shininess", 300)
        self.addUniform("float", "alpha", 1.0)
        self.addUniform("bool", "useFaceNormals", False)
        self.addUniform("bool", "useVertexColors", False)
        self.addUniform("bool", "shaded", False)
        
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
