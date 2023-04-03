"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from .abstract import AbstractMaterial
from ..objects.lights import Light

class BasicMaterial(AbstractMaterial):
    """Contains basic shader codes."""

    lightCalcLambert = \
    """
    vec3 lightCalc(Light light, vec3 startingColor, vec3 diffuse,
                   vec3 pointPosition, vec3 pointNormal)
    {
        // Set initial values
        vec3 totalColor = startingColor;
        float lightAttenuation;
        vec3 lightDirection;
        float diffuseValue;

        // Calculate attenuation and light direction
        if (light.lightType == 1)
        {
            return startingColor;
        }
        else if (light.lightType == 2)
        {
            lightDirection = normalize(light.direction);
        }
        
        else
        {
            lightDirection = normalize(light.position - pointPosition);
            float a = light.attenuation[0];
            float b = light.attenuation[1];
            float c = light.attenuation[2];
            float d = distance(pointPosition, light.position);
            lightAttenuation = 1 / (a + (b * d) + (c * d * d));
        }
        // Normalize point normal and calculate diffuse value 
        vec3 nPointNormal = normalize(pointNormal);
        diffuseValue = max(dot(nPointNormal, lightDirection), 0.0); 
        diffuseValue *= lightAttenuation;

        // Calculate the total color increase for diffuse and
        //    add it to total color
        totalColor += (diffuse - totalColor) * diffuseValue;

        // Return the total color times the light's color
        return totalColor * light.color;
    }
    """
    
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
        fragmentShaderCode = \
        Light.lightStruct + \
        self.lightCalcLambert + \
        """
        uniform vec3 baseColor;
        uniform bool useVertexColors;
        uniform float ambMul;
        in vec3 color;
        in vec3 normal;
        in vec3 position;
        out vec4 fragColor;
        void main()
        {
            vec3 diffuse = color;
            vec3 total = diffuse * ambMul;
            total = lightCalc(light0, total, diffuse, position, normal);
            total = lightCalc(light1, total, diffuse, position, normal);
            total = lightCalc(light2, total, diffuse, position, normal);
            total = lightCalc(light3, total, diffuse, position, normal);
            fragColor = vec4(total, 1.0);
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
        
