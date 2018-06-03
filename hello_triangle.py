from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glfw
import numpy


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


SCR_WIDTH = 800
SCR_HEIGHT = 600

vertexShaderSource = None
with open("simple_v.glsl", "r") as file:
    vertexShaderSource = file.readlines()

fragmentShaderSource = None
with open("simple_f.glsl") as file:
    fragmentShaderSource = file.readlines()

glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", None, None)
glfw.make_context_current(window)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

# build and compile our shader program
vertexShader = glCreateShader(GL_VERTEX_SHADER)
glShaderSource(vertexShader, vertexShaderSource)
glCompileShader(vertexShader)

# check for shader compile errors
if not glGetShaderiv(vertexShader, GL_COMPILE_STATUS):
    raise Exception('failed to compile shader "%s":\n%s' % ("vertex shader", glGetShaderInfoLog(vertexShader)))

fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(fragmentShader, fragmentShaderSource)
glCompileShader(fragmentShader)
if not glGetShaderiv(fragmentShader, GL_COMPILE_STATUS):
    raise Exception('failed to compile shader "%s":\n%s' % ("fragment shader", glGetShaderInfoLog(fragmentShader)))

shaderProgram = glCreateProgram()
glAttachShader(shaderProgram, vertexShader)
glAttachShader(shaderProgram, fragmentShader)
glLinkProgram(shaderProgram)
if not glGetProgramiv(shaderProgram, GL_LINK_STATUS):
    raise Exception("error when link program %s" % glGetProgramInfoLog(shaderProgram))

glDeleteShader(vertexShader)
glDeleteShader(fragmentShader)

vertices = numpy.array([-0.5, -0.5, 0.0,
                        0.5, -0.5, 0.0,
                        0.0, 0.5, 0.0], dtype='float32')
vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)

# bind the Vertex Array Object first
glBindVertexArray(vao)

# then bind and set vertex buffer(s)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, None)
glEnableVertexAttribArray(0)

# unbind
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

while not glfw.window_should_close(window):
    process_input(window)

    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shaderProgram)
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    glfw.swap_buffers(window)
    glfw.poll_events()

glDeleteVertexArrays(1, (vao,))
glDeleteBuffers(1, (vbo,))
glfw.terminate()
