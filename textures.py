import glfw
import numpy
from pil import Image

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

window = glfw.create_window(800, 600, "LearnOpenGL", None, None)
glfw.make_context_current(window)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

ourShader = Shader("4.1.texture_v.glsl", "4.1.texture_f.glsl")
vertices = numpy.array([
    # positions    colors         texture coords
    0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,  # top right
    0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,  # bottom right
    -0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # bottom left
    -0.5, 0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0  # top left
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
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)

# set the texture wrapping parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
# set texture filtering parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

with Image.open("container.jpg").transpose(Image.FLIP_TOP_BOTTOM) as image:
    imdata = numpy.fromstring(image.tobytes(), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, imdata)
    glGenerateMipmap(GL_TEXTURE_2D)

while not glfw.window_should_close(window):
    process_input(window)

    # render
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # bind texture
    glBindTexture(GL_TEXTURE_2D, texture)

    # render container
    ourShader.use()
    glBindVertexArray(vao)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)
    glfw.poll_events()

glDeleteVertexArrays(1, (vao,))
glDeleteBuffers(1, (vbo,))
glDeleteBuffers(1, (ebo, 0))
glfw.terminate()
