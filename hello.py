from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glfw


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


if not glfw.init():
    exit(-1)

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE,glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

window = glfw.create_window(800, 600, "LearnOpenGl", None, None)
glfw.make_context_current(window)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

glGenBuffers(1)

while not glfw.window_should_close(window):
    process_input(window)

    # render
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
