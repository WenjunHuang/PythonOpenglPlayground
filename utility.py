from OpenGL.GL import *


def check_shader_error(shader, name):
    # check for shader compile errors
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise Exception('failed to compile shader "%s":\n%s' % (name, glGetShaderInfoLog(shader)))


def check_link_error(program, name):
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise Exception('failed to link program "%s":\n%s' % (name, glGetProgramInfoLog(program)))


def compile_shader(shader, shader_name, shader_file):
    source = None
    with open(shader_file) as file:
        source = file.readlines()

    glShaderSource(shader, source)
    glCompileShader(shader)
    check_shader_error(shader, shader_name)

    return shader


def compile_and_link_program(*shaders):
    program = glCreateProgram()
    for shader in shaders:
        glAttachShader(program, shader)
    glLinkProgram(program)
    check_link_error(program, "program")

    return program
