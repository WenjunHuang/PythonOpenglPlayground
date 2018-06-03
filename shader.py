from OpenGL.GL import *
from utility import *


class Shader:
    def __init__(self, vertexPath, fragmentPath):
        vertex = compile_shader(glCreateShader(GL_VERTEX_SHADER),
                                "vertex", vertexPath)
        fragment = compile_shader(glCreateShader(GL_FRAGMENT_SHADER),
                                  "fragment", fragmentPath)
        self.program = compile_and_link_program(vertex, fragment)
        glDeleteShader(vertex)
        glDeleteShader(fragment)

    def use(self):
        glUseProgram(self.program)

    def setBool(self, name, value: bool):
        glUniform1i(glGetUniformLocation(self.program, name), value)

    def setInt(self, name, value):
        glUniform1i(glGetUniformLocation(self.program, name), value)

    def setFloat(self, name, value):
        glUniform1f(glGetUniformLocation(self.program, name), value)
