"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from .abstract import AbstractMaterial

class BasicMaterial(AbstractMaterial):
    """Contains basic shader codes."""
    
    def __init__(self):
        vertexShaderCode = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec3 vertexColor;
        uniform vec3 baseColor;
        uniform bool useVertexColors;
        uniform bool useFaceNormals;
        in vec3 faceNormal;
        in vec3 vertexNormal;
        out vec3 color;
        out vec3 normal;
        out vec3 position;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            position = vec3(modelMatrix * vec4(vertexPosition,1));

            if (useFaceNormals)
            {
                normal =normalize(mat3(modelMatrix)*faceNormal);
            }
            else
            {
                normal =normalize(mat3(modelMatrix)*vertexNormal);
            }
            color = baseColor;
            if (useVertexColors)
            {
                color *= vertexColor; 
            }
        }
        """
        fragmentShaderCode = """
        uniform vec3 baseColor;
        uniform bool useVertexColors;
        in vec3 color;
        out vec4 fragColor;
        void main()
        {
            vec4 tempColor = vec4(baseColor, 1.0);
            if (useVertexColors)
                tempColor *= vec4(color, 1.0);
            fragColor = tempColor;
        }
        """
        super().__init__(vertexShaderCode, fragmentShaderCode)
        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.addUniform("bool", "useVertexColors", False)
        self.locateUniforms()
        
