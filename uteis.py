import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random

def janela():

  glfw.init()
  glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
  window = glfw.create_window(800, 800, "Cena", None, None)
  glfw.make_context_current(window)
  glfw.show_window(window)

  # Habilitar teste de profundidade
  glEnable(GL_DEPTH_TEST)

  return window


def programa():
  vertex_code = """
        attribute vec3 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,1.0);
        }
        """
  
  fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """
  
  # Request a program and shader slots from GPU
  program  = glCreateProgram()
  vertex   = glCreateShader(GL_VERTEX_SHADER)
  fragment = glCreateShader(GL_FRAGMENT_SHADER)

  # Set shaders source
  glShaderSource(vertex, vertex_code)
  glShaderSource(fragment, fragment_code)

  # Compile shaders
  glCompileShader(vertex)
  if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")
  
  glCompileShader(fragment)
  if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")

  # Attach shader objects to the program
  glAttachShader(program, vertex)
  glAttachShader(program, fragment)

  # Build program
  glLinkProgram(program)
  if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
    
  # Make program the default program
  glUseProgram(program)

  return program


def passar_para_gpu(vertices):
  # Request a buffer slot from GPU
  buffer = glGenBuffers(1)
  # Make this buffer the default one
  glBindBuffer(GL_ARRAY_BUFFER, buffer)


  # Upload data
  glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
  glBindBuffer(GL_ARRAY_BUFFER, buffer)

  # Bind the position attribute
  # --------------------------------------
  stride = vertices.strides[0]
  offset = ctypes.c_void_p(0)

  loc = glGetAttribLocation(program, "position")
  glEnableVertexAttribArray(loc)
  glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)
  