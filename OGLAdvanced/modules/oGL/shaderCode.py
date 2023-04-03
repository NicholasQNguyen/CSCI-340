vertexShaderWithNormals = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        uniform vec3 baseColor;
        uniform bool useVertexColors;
        uniform bool useFaceNormals;
        in vec3 vertexPosition;
        in vec3 vertexColor;
        in vec3 faceNormal;
        in vec3 vertexNormal;
        out vec3 color;
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
            
            color = baseColor;
            if (useVertexColors)
                color *= vertexColor;
            
        }
        
"""

lightStruct = """
        struct Light
        {
            // 1 = DUMMY, 2 = DIRECTIONAL, 3 = POINT
            int lightType;
            
            // used by all lights
            vec3 color;
            
            // used by directional lights
            vec3 direction;
            
            // used by point lights
            vec3 position;
            vec3 attenuation;
        };
        
        uniform Light light0;
        uniform Light light1;
        uniform Light light2;
        uniform Light light3;
"""

lightCalcLambert = """
        vec3 lightCalc(Light light,
                       vec3 startingColor,
                       vec3 diffuse,
                       vec3 pointPosition,
                       vec3 pointNormal)
        {
            // Check for dummy lights
            if (light.lightType == 1)
            {
                return startingColor;
            }
            
            vec3 totalColor = startingColor;            
            float attenuation = 1.0;
            vec3 lightDirection;
            if (light.lightType == 2)
            {
                lightDirection = normalize(light.direction);
            }
            else if (light.lightType == 3)
            {
                lightDirection = normalize(pointPosition - light.position);
                float distance = length(light.position - pointPosition);
                attenuation = 1.0 / light.attenuation[0] + 
                                    light.attenuation[1] * distance +
                                    light.attenuation[2] * distance * distance;
            } 
            pointNormal = normalize(pointNormal);
            float diffuseValue = max(dot(pointNormal, lightDirection), 0);
            diffuseValue *= attenuation;
            totalColor += (diffuse - totalColor) * diffuseValue;
            return light.color * totalColor;
        }
"""

lightCalcPhong = """
        uniform vec3 viewPosition;
        uniform float specularStrength;
        uniform float shininess;
        vec3 lightCalc(Light light,
                       vec3 startingColor,
                       vec3 diffuse,
                       vec3 specular,
                       vec3 pointPosition,
                       vec3 pointNormal)
        {
            // Check for dummy lights
            if (light.lightType == 1)
            {
                return startingColor;
            }
            
            vec3 totalColor = startingColor;     
            
            return light.color * totalColor;
        }
"""
