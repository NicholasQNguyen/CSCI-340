from base import Base
from openGLUtils import OpenGLUtils
from OpenGL.GL import *


class Test(Base):
    def initialize(self):
        vsCode = \
            """
            void main()
            {
                gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
            }
            """
        fsCode = \
            """
            out vec4 fragColor;
            void main()
            {
                gl_Position = vec4(1.0, 1.0, 0.0, 1.0);
            }
            """
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)
        glPointSize(10)

    def update(self):
        glUseProgram(self.programRef)
        glDrawArrays(GL_POINTS, 0, 1)


if __name__ == "__main__":
    Test().run()
