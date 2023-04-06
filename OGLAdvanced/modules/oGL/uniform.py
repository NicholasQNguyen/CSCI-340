"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from OpenGL.GL import *

class Uniform(object):
    def __init__(self, dataType, data):
        # type of data:
        #  int | bool | float | vec2 | vec3 | vec4 | mat4
        self.dataType = dataType
        self.data = data
        self.variableRef = None
    
    def locateVariable(self, programRef, variableName):
        self.variableRef = glGetUniformLocation(programRef,
                                                variableName)
        if self.dataType == "Light":
            self.variableRef = {}
            self.variableRef["lightType"] = glGetUniformLocation(programRef,
                                            variableName + ".lightType")
            self.variableRef["color"]     = glGetUniformLocation(programRef,
                                            variableName + ".color")
            self.variableRef["direction"] = glGetUniformLocation(programRef,
                                            variableName + ".direction")
            self.variableRef["position"]  = glGetUniformLocation(programRef,
                                            variableName + ".position")
            self.variableRef["attenuation"]=glGetUniformLocation(programRef,
                                            variableName + ".attenuation")
        else:
            self.variableRef = glGetUniformLocation(programRef,
                                                    variableName)

    def uploadData(self):
        if self.variableRef == -1:
            return
        if self.dataType == "int":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "bool":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "float":
            glUniform1f(self.variableRef, self.data)
        elif self.dataType == "vec2":
            glUniform2f(self.variableRef, self.data[0], self.data[1])
        elif self.dataType == "vec3":
            glUniform3f(self.variableRef, self. data[0],
                        self.data[1], self.data[2])
        elif self.dataType == "vec4":
            glUniform4f(self.variableRef, self.data[0],
                        self.data[1], self.data[2], self.data[3])
        elif self.dataType == "mat4":
            glUniformMatrix4fv(self.variableRef, 1, GL_TRUE, self.data)
        
        elif self.dataType == "Light":
            glUniform1i(self.variableRef["lightType"],
                        int(self.data.lightType))
            glUniform3f(self.variableRef["color"], *self.data.color)
            direction = self.data.getDirection()
            glUniform3f(self.variableRef["direction"], *direction[:3])
            position = self.data.getPosition()
            glUniform3f(self.variableRef["position"], *position)
            glUniform3f(self.variableRef["attenuation"],
                        *self.data.attenuation)

        elif self.dataType == "sampler2D":
            textureObjectRef, textureUnitRef = self.data
            # activate texture unit
            glActiveTexture(GL_TEXTURE0 + textureUnitRef)
            # associate texture object reference to currently
            # active texture unit
            glBindTexture(GL_TEXTURE_2D, textureObjectRef)
            # upload texture unit number (0...15) to
            # uniform variable in shader
            glUniform1i(self.variableRef, textureUnitRef)

