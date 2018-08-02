from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image
from shader import Shader
import glm
import glfw
import numpy


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


SCR_WIDTH = 800
SCR_HEIGHT = 600

if not glfw.init():
    exit(-1)

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "Coordination Systems", None, None)
glfw.make_context_current(window)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

ourShader = Shader("6.1.coordinate_systems_v.glsl", "6.1.coordinate_systems_f.glsl")
vertices = numpy.array([
    # positions    # texture coords
    0.5, 0.5, 0.0, 1.0, 1.0,  # top right
    0.5, -0.5, 0.0, 1.0, 0.0,  # bottom right
    -0.5, -0.5, 0.0, 0.0, 0.0,  # bottom left
    -0.5, 0.5, 0.0, 0.0, 1.0  # top left
], dtype='float32')
indices = numpy.array([
    0, 1, 3,  # first triangle
    1, 2, 3  # second triangle
], dtype='int32')

VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)
EBO = glGenBuffers(1)

glBindVertexArray(VAO)

glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

# position attribute
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, None)
glEnableVertexAttribArray(0)

# texture coord attribute
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

# texture 1
texture1 = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture1)

# set the texture wrapping parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

# set texture filtering parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# load image, create texture and generate mipmaps
with Image.open("container.jpg").transpose(Image.FLIP_TOP_BOTTOM) as image:
    imdata = numpy.fromstring(image.tobytes(), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, imdata)
    glGenerateMipmap(GL_TEXTURE_2D)

# texture 2
texture2 = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture2)
# set the texture wrapping parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
# set texture filtering parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

with Image.open("awesomeface.png").transpose(Image.FLIP_TOP_BOTTOM) as image:
    imdata = numpy.fromstring(image.tobytes(), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, imdata)
    glGenerateMipmap(GL_TEXTURE_2D)

ourShader.use()
ourShader.setInt("texture1", 0)
ourShader.setInt("texture2", 1)

while not glfw.window_should_close(window):
    process_input(window)

    # render
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # bind textures on corresponding texture units
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture1)
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, texture2)

    # activate shader
    ourShader.use()

    model = glm.rotate(glm.mat4(1.0), glm.radians(-55.0), glm.vec3(1.0, 0.0, 0.0))
    view = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -3.0))
    projection = glm.perspective(glm.radians(45.0), SCR_WIDTH / SCR_HEIGHT, 0.1, 100.0)

    # retrieve the matrix uniform locations
    modelLoc = glGetUniformLocation(ourShader.program, "model")
    viewLoc = glGetUniformLocation(ourShader.program, "view")
    projectionLoc = glGetUniformLocation(ourShader.program, "projection")

    # pass them to the shaders (3 different ways)
    glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(model))
    glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, glm.value_ptr(projection))

    # render container
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)

    glfw.swap_buffers(window)
    glfw.poll_events()

glDeleteVertexArrays(1, (VAO,))
glDeleteBuffers(1, (VBO,))
glDeleteBuffers(1, (EBO,))

glfw.terminate()
