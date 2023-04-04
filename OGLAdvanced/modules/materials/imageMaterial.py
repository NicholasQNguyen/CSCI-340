from .abstract import AbstractMaterial
from ..objects.lights import Light


class ImageMaterial(AbstractMaterial):
    """Contains basic shader codes."""
    def __init__(self):
        vertexShaderCode = """
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
                   discard;
                diffuse *= tColor.rgb;
            }
            vec3 total = diffuse;
            total = total * ambMul;
            vec3 specular = (diffuse + vec3(0.1,0.1,0.1)) * specMul;
            if (shaded)
            {
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
        fragmentShaderCode = \
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
        
    
