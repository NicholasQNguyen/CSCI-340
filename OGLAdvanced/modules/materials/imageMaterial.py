from .abstract import AbstractMaterial
from .texture import Texture
from ..oGL.shaderCode import lightCalcPhong, lightStruct, vertexShaderWithNormals
from OpenGL.GL import *

class ImageMaterial(AbstractMaterial):
    """Contains basic shader codes."""
    def __init__(self, texture=None, properties={}):
        self.texture = Texture(texture)
        
        vertexShaderCode = \
        """
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
                {
                color *= vertexColor;
                }
            UV = vertexUV * repeatUV + offsetUV;
        }
        """

        fragmentShaderCode = \
        lightStruct + lightCalcPhong + \
        """
        uniform sampler2D texture;
        uniform bool useVertexColors;
        uniform float ambMul;
        uniform float specMul;
        uniform bool useUVColors;
        in vec3 color;
        in vec3 normal;
        in vec3 position;
        in vec2 UV;
        out vec4 fragColor;
        void main()
        {
            vec3 diffuse = color;
            if (useUVColors)
            {
                vec4 tColor = texture2D(texture, UV);
                if (tColor.z < 0.01)
                {
                    discard;
                }
                diffuse *= tColor.rgb;
            }
            vec3 total =  diffuse;
            total = total * ambMul;
            vec3 specular = (diffuse + vec3(0.1,0.1,0.1)) * specMul;
            total = lightCalc(light0, total, diffuse, specular,
                              position, normal);
            total = lightCalc(light1, total, diffuse, specular,
                              position, normal);
            total = lightCalc(light2, total, diffuse, specular,
                              position, normal);
            total = lightCalc(light3, total, diffuse, specular,
                              position, normal);
            fragColor = vec4(total, 1);
        }
        """
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
