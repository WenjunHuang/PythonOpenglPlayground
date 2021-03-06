import glfw
import numpy
import glm
from PIL import Image

from shader import *


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

window = glfw.create_window(800, 600, "LearnOpenGL", None, None)
glfw.make_context_current(window)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

ourShader = Shader("4.1.texture_v.glsl", "4.1.texture_f.glsl")
vertices = numpy.array([
    # positions    colors         texture coords
    0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 2.0, 2.0,  # top right
    0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 2.0, 0.0,  # bottom right
    -0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # bottom left
    -0.5, 0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 2.0  # top left
], dtype='float32')

indices = numpy.array([
    0, 1, 3,  # first triangle
    1, 2, 3  # second triangle
], dtype='int32')

vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)
ebo = glGenBuffers(1)

glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

# position attribute
glVertexAttribPointer(0, 3, GL_FLOAT, False, 8 * 4, None)
glEnableVertexAttribArray(0)
# color attribute
glVertexAttribPointer(1, 3, GL_FLOAT, False, 8 * 4, ctypes.c_void_p(3 * 4))
glEnableVertexAttribArray(1)
# texture coord attribute
glVertexAttribPointer(2, 2, GL_FLOAT, False, 8 * 4, ctypes.c_void_p(6 * 4))
glEnableVertexAttribArray(2)

# load and create a texture
texture1 = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture1)

# set the texture wrapping parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
# set texture filtering parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

with Image.open("container.jpg").transpose(Image.FLIP_TOP_BOTTOM) as image:
    imdata = numpy.fromstring(image.tobytes(), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, imdata)
    glGenerateMipmap(GL_TEXTURE_2D)

texture2 = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture2)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
with Image.open("awesomeface.png").transpose(Image.FLIP_TOP_BOTTOM) as image:
    imdata = numpy.fromstring(image.tobytes(), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, imdata)
    glGenerateMipmap(GL_TEXTURE_2D)

ourShader.use()
glUniform1i(glGetUniformLocation(ourShader.program, "texture1"), 0)
ourShader.setInt("texture2", 1)

trans = glm.translate(glm.mat4(1.0), glm.vec3(0.5, -0.5, 0.0))
trans = glm.scale(trans, glm.vec3(0.5, 0.5, 0.5))
trans = glm.rotate(trans, glm.radians(90.0), glm.vec3(0.0, 0.0, 1.0))
transformLoc = glGetUniformLocation(ourShader.program, "transform")

while not glfw.window_should_close(window):
    process_input(window)

    # render
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # bind texture
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture1)
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, texture2)

    # render container
    ourShader.use()
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, glm.value_ptr(trans))
    glBindVertexArray(vao)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)
    glfw.poll_events()

glDeleteVertexArrays(1, (vao,))
glDeleteBuffers(1, (vbo,))
glDeleteBuffers(1, (ebo, 0))
glfw.terminate()
