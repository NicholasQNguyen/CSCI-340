"""
Author: Liz Matthews
Code modified from
https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from .abstract import AbstractMaterial
from ..objects.lights import Light
from ..oGL.shaderCode import lightCalcPhong, lightStruct, vertexShaderWithNormals
from OpenGL.GL import *


class MountainMaterial(AbstractMaterial):
    """Contains mountain shader codes."""
    def __init__(self, properties={}):
        vertexShaderCode = \
        """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        uniform bool useFaceNormals;
        in vec3 vertexPosition;
        in vec3 faceNormal;
        in vec3 vertexNormal;
        out vec3 normal;
        out vec3 position;
        void main() {
            gl_Position = projectionMatrix * viewMatrix *
                          modelMatrix * vec4(vertexPosition, 1);                  
            position = vec3(modelMatrix * vec4(vertexPosition, 1));
            
            if (useFaceNormals)
                normal = normalize(mat3(modelMatrix) * faceNormal);
            else
                normal = normalize(mat3(modelMatrix) * vertexNormal);    
        }
        """

        fragmentShaderCode = lightStruct + lightCalcPhong + \
        """
        const vec3 colors[] = vec3[](
        vec3(0.0,        0.0,        0.54509804),
        vec3(0.39215686, 0.58431373, 0.92941176),
        vec3(0.0,        0.39215686, 0.0       ),
        vec3(0.4,        0.80392157, 0.0       ),
        vec3(0.54509804, 0.27058824, 0.0745098 ),
        vec3(0.90196078, 0.90196078, 0.98039216),
        vec3(1.0,        1.0,        1.0)
        );
        /*
        // Tester vector
        const vec3 colors[] = vec3[](
        vec3(0.5,        0.0,        0.5),
        vec3(0.5, 0.0, 0.5),
        vec3(0.5,        0.0, 0.5       ),
        vec3(0.5,        0.0, 0.5       ),
        vec3(0.5, 0.0, 0.5 ),
        vec3(0.5, 0.0, 0.5),
        vec3(0.5,        0.0,        0.5)
        );
        */
        const float split = 0.8;
        uniform float ambMul; 
        uniform float specMul;
        uniform float maxHeight;
        uniform float minHeight;
        uniform float alpha;
        in vec3 position;
        in vec3 normal;
        out vec4 fragColor;
        void main()
        {
            float height = position[1];
            float percent = (height - minHeight) / (maxHeight - minHeight);    
            vec3 diffuse;
            if (percent < split)
            {
                diffuse = mix(colors[0], colors[1], percent / split);
            }
            else 
            {
                float newPercent = (percent - split) / (1.0 - split);
                int startIndex = 2;
                int endIndex = 6;
                newPercent = newPercent * (endIndex - startIndex);
                int index = int(floor(newPercent));
                newPercent = fract(newPercent);
                index += startIndex;
                diffuse = mix(colors[index], colors[index+1], newPercent);
            }
            fragColor = vec4(diffuse, 1);
            vec3 specular = (diffuse + vec3(0.1,0.1,0.1)) * specMul;
            vec3 total =  diffuse * ambMul;
            total = lightCalc(light0, total, diffuse, specular,
                              position, normal);
            total = lightCalc(light1, total, diffuse, specular,
                              position, normal);
            total = lightCalc(light2, total, diffuse, specular,
                              position, normal);
            total = lightCalc(light3, total, diffuse, specular,
                              position, normal);
            // fragColor = vec4(total, alpha);
        }
        """
        super().__init__(vertexShaderCode, fragmentShaderCode)
        self.addUniform("Light", "light0", None )
        self.addUniform("Light", "light1", None )
        self.addUniform("Light", "light2", None )
        self.addUniform("Light", "light3", None )        
        self.addUniform("bool", "useFaceNormals", False)        
        self.addUniform("float", "ambMul", 0.3)
        self.addUniform("float", "specMul", 1.5)
        self.addUniform("float", "maxHeight", 1.25)
        self.addUniform("float", "minHeight", 0)
        self.addUniform("float", "alpha", 1.0)
        self.locateUniforms()

        # Render both sides? default: both side only
        # Vertices ordered counterclockwise
        self.settings["doubleSide"] = True
 
    def updateRenderSettings(self):
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
