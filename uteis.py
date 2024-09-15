import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random

def janela():

  glfw.init()
  glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
  window = glfw.create_window(700, 700, "Esfera", None, None)
  glfw.make_context_current(window)
  glfw.show_window(window)
  #Isso garante que o OpenGL renderize objetos 3D corretamente, levando em consideração 
  #a profundidade dos vértices e ocultando superfícies que deveriam estar atrás de outras.
  glEnable(GL_DEPTH_TEST) ### importante para 3D

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

def passar_para_gpu(program, vertices):
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

def merge_vertices(vertices):

  print(vertices)
  # Collect the 'position' arrays from each object
  positions = [obj['position'] for obj in vertices]
  
  # Concatenate all the 'position' arrays
  merged_positions = np.concatenate(positions)
  
  # Create a new NumPy structured array for the merged vertices
  total_vertices = len(merged_positions)
  merged_vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
  merged_vertices['position'] = merged_positions
  
  return merged_vertices

def get_matriz_rotacao_x(angulo):
  cos_x = math.cos(angulo)
  sin_x = math.sin(angulo)

  mat_rot_x = np.array([    1.0,   0.0,    0.0, 0.0, 
                            0.0, cos_x, -sin_x, 0.0, 
                            0.0, sin_x,  cos_x, 0.0, 
                            0.0,   0.0,    0.0, 1.0], np.float32)
  
  return mat_rot_x

def get_matriz_rotacao_y(angulo):
  cos_y = math.cos(angulo)
  sin_y = math.sin(angulo)

  mat_rot_y = np.array([    cos_y,  0.0, sin_y, 0.0, 
                            0.0,    1.0,   0.0, 0.0, 
                           -sin_y, 0.0, cos_y, 0.0, 
                            0.0,    0.0,   0.0, 1.0], np.float32)

  return mat_rot_y

def get_matriz_rotacao_z(angulo):
  cos_z = math.cos(angulo)
  sin_z = math.sin(angulo)

  mat_rot_z = np.array([    cos_z, -sin_z, 0.0, 0.0, 
                            sin_z,  cos_z, 0.0, 0.0, 
                            0.0,      0.0, 1.0, 0.0, 
                            0.0,      0.0, 0.0, 1.0], np.float32)
  
  return mat_rot_z

def get_matriz_translacao(tx,ty,tz):
  mat_translacao = np.array([    1.0,   0.0,    0.0, tx, 
                                  0.0,   1.0,    0.0, ty, 
                                  0.0,   0.0,    1.0, tz, 
                                  0.0,   0.0,    0.0, 1.0], np.float32)
  
  return mat_translacao