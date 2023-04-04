vertexShaderWithNormals = """
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

lightCalcPhong = \
        """
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
            float diffuseValue = 0.0;
            float specularValue = 0.0;
            float attenuation = 1.0;
            vec3 lightDirection;
            
            if (light.lightType == 2)
            {
                lightDirection = normalize(light.direction);
            }
            else if (light.lightType == 3)
            {
                // Calculate attenuation and light direction
                lightDirection = normalize(pointPosition - light.position);
                float distance = length(pointPosition - light.position);
                attenuation = 1.0 / light.attenuation[0] + 
                                    light.attenuation[1] * distance +
                                    light.attenuation[2] * distance * distance;
            }
            // Normalize point normal and calculate diffuse value   
            pointNormal = normalize(pointNormal);
            diffuseValue = max(dot(pointNormal, lightDirection), 0.0);
            diffuseValue *= attenuation;
            if (diffuseValue > 0)
            {
                // Calculate view direction
                vec3 viewDirection = normalize(pointPosition - viewPosition);

                // Calculate the reflected direction
                vec3 reflectedDirection = normalize(reflect(lightDirection, pointNormal));

                // Calculate the specular value
                specularValue = max(dot(viewDirection, reflectedDirection), 0.0);

                // Calculate final specular value 
                specularValue = specularStrength * pow(specularValue, shininess);
            }

            // Calculate the total color increase for diffuse and
            //    add it to total color
            totalColor += (diffuse - totalColor) * diffuseValue;

            // Calculate the total color increase for specular and
            //    add it to total color
            totalColor += (specular - totalColor) * specularValue;

            // Return the total color times the light's color
            return totalColor * light.color;
        }
"""
