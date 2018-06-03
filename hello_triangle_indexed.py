from OpenGL.GL import *
from utility import *
import glfw
import numpy
import math

SCR_WIDTH = 600
SCR_HEIGHT = 600

vertexShaderSource = None
with open('simple_v.glsl') as file:
    vertexShaderSource = file.readlines()

fragmentShaderSource = None
with open('simple_f.glsl') as file:
    fragmentShaderSource = file.readlines()


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", None, None)
glfw.make_context_current(window)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

# build and compile our shader program

# vertex shader
vertexShader = compile_shader(glCreateShader(GL_VERTEX_SHADER), shader_file="simple_v.glsl",
                              shader_name="vertex shader")

# fragment shader
fragmentShader = compile_shader(glCreateShader(GL_FRAGMENT_SHADER), shader_file="simple_f.glsl",
                                shader_name="fragment shader")

vertexShader2 = compile_shader(glCreateShader(GL_VERTEX_SHADER), shader_file="simple_v2.glsl",
                               shader_name="vertex shader")
fragmentShader2 = compile_shader(glCreateShader(GL_FRAGMENT_SHADER), shader_file="simple_f2.glsl",
                                 shader_name="another color fragment shader")

# link shaders
shaderProgram = compile_and_link_program(vertexShader, fragmentShader)
shaderProgram2 = compile_and_link_program(vertexShader2, fragmentShader2)

glDeleteShader(vertexShader)
glDeleteShader(fragmentShader)
glDeleteShader(vertexShader2)
glDeleteShader(fragmentShader2)

# vertices = numpy.array([0.5, 0.5, 0.0,
#                         0.5, -0.5, 0.0,
#                         -0.5, -0.5, 0.0,
#                         -0.5, 0.5, 0.0], dtype='float32')
vertices = numpy.array([0.5, 0.5, 0.0,
                        0.5, -0.5, 0.0,
                        -0.5, -0.5, 0.0], dtype='float32')
vertices2 = numpy.array([0.5, 0.5, 0.0, 1.0, 0.0, 0.0,
                         -0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                         -0.5, 0.5, 0.0, 0.0, 0.0, 1.0], dtype='float32')
indices = numpy.array([0, 1, 3,
                       1, 2, 3], dtype='int32')

VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)
EBO = glGenBuffers(1)

VAO2 = glGenVertexArrays(1)
VBO2 = glGenBuffers(1)

# bind the vertex array object first
glBindVertexArray(VAO)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, None)
glEnableVertexAttribArray(0)

# another vao
glBindVertexArray(VAO2)
glBindBuffer(GL_ARRAY_BUFFER, VBO2)
glBufferData(GL_ARRAY_BUFFER, vertices2, GL_STATIC_DRAW)
glVertexAttribPointer(0, 3, GL_FLOAT, False, 24, None)
glEnableVertexAttribArray(0)
glVertexAttribPointer(1, 3, GL_FLOAT, False, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

while not glfw.window_should_close(window):
    process_input(window)

    # render
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # draw our first triangle
    timeValue = glfw.get_time()
    greenValue = math.sin(timeValue) / 2.0 + 0.5
    vertexColorLocation = glGetUniformLocation(shaderProgram, "ourColor")
    glUseProgram(shaderProgram)
    glUniform4f(vertexColorLocation, 0.0, greenValue, 0.0, 1.0)
    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    glUseProgram(shaderProgram2)
    glBindVertexArray(VAO2)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    # glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)
    glfw.poll_events()

glDeleteVertexArrays(1, (VAO,))
glDeleteBuffers(1, (VBO,))
glDeleteBuffers(1, (EBO,))
glfw.terminate()
