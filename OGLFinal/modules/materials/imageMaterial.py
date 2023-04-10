"""
Author: Liz Matthews
"""
from .abstract import AbstractMaterial
from ..oGL.shaderCode import lightCalcPhong, lightStruct, vertexShaderWithNormals
from OpenGL.GL import *


class ImageMaterial(AbstractMaterial):
    def __init__(self, texture=None, properties={}):
        vShaderCode = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        uniform vec3 baseColor;
        uniform vec2 repeatUV;
        uniform vec2 offsetUV;
        uniform bool useVertexColors;
        uniform bool useFaceNormals;
        in vec3 vertexColor;
        in vec3 vertexPosition;
        in vec3 vertexNormal;
        in vec3 faceNormal;
        in vec2 vertexUV;
        out vec3 color;
        out vec3 normal;
        out vec3 position;
        out vec2 UV;
        void main() {
            gl_Position = projectionMatrix * viewMatrix *
                          modelMatrix * vec4(vertexPosition, 1);
                          
            position = vec3(modelMatrix * vec4(vertexPosition, 1));
            
            if (useFaceNormals)
                normal = normalize(mat3(modelMatrix) * faceNormal);
            else
                normal = normalize(mat3(modelMatrix) * vertexNormal);
            
            color = baseColor;
            if (useVertexColors)
                color *= vertexColor;
            
            UV = vertexUV * repeatUV + offsetUV;
        }
        """
        fShaderCode = \
        lightStruct + lightCalcPhong + \
        """
        uniform sampler2D texture;
        uniform bool useUVColors;
        uniform bool shaded;
        uniform float ambMul;
        uniform float specMul;
        in vec3 color;
        in vec3 position;
        in vec3 normal;
        in vec2 UV;
        out vec4 fragColor;
        void main()
        {
            vec3 diffuse = color;
            if (useUVColors)
            {
                vec4 tColor = texture2D(texture, UV);
                if (tColor.a < 0.01)
                {
                   discard;
                }
                diffuse *= tColor.rgb;
            }
            vec3 total =  diffuse;
            total = total * ambMul;
            if (shaded)
            {
                vec3 specular = (diffuse + vec3(0.1,0.1,0.1)) * specMul;
                total = lightCalc(light0, total, diffuse, specular,
                                  position, normal);
                total = lightCalc(light1, total, diffuse, specular,
                                  position, normal);
                total = lightCalc(light2, total, diffuse, specular,
                                  position, normal);
                total = lightCalc(light3, total, diffuse, specular,
                                  position, normal);
            }
            fragColor = vec4(total, 1);
        }
"""

        super().__init__(vShaderCode, fShaderCode)
        
        self.addUniform("sampler2D", "texture", [texture.textureRef, 1])
        self.addUniform("Light", "light0", None )
        self.addUniform("Light", "light1", None )
        self.addUniform("Light", "light2", None )
        self.addUniform("Light", "light3", None )
        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.addUniform("mat4", "projectionMatrix", [0,0,0])
        self.addUniform("vec3", "viewPosition", [0,0,0])
        self.addUniform("mat4", "viewMatrix", [0,0,0])
        self.addUniform("mat4", "modelMatrix", [0,0,0])
        self.addUniform("vec2", "repeatUV", [0,0])
        self.addUniform("vec2", "offsetUV", [0,0])
        self.addUniform("float", "ambMul", 0.3)
        self.addUniform("float", "specMul", 1.5)
        self.addUniform("float", "specularStrength", 1)
        self.addUniform("float", "shininess", 300)
        self.addUniform("float", "alpha", 1.0)
        self.addUniform("bool", "useFaceNormals", False)
        self.addUniform("bool", "useUVColors", True)
        self.addUniform("bool", "useVertexColors", False)
        self.addUniform("bool", "shaded", True)
        
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
