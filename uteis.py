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
  mat_translacao = np.array([     1.0,   0.0,    0.0, tx, 
                                  0.0,   1.0,    0.0, ty, 
                                  0.0,   0.0,    1.0, tz, 
                                  0.0,   0.0,    0.0, 1.0], np.float32)
  
  return mat_translacao

def get_matriz_escala(sx, sy, sz):
    
  mat_escala = np.array([       sx,   0.0,    0.0, 0.0, 
                                0.0,   sy,    0.0, 0.0, 
                                0.0,   0.0,   sz,  0.0, 
                                0.0,   0.0,   0.0, 1.0], np.float32)

  return mat_escala    



#https://www.glfw.org/docs/3.3/group__keys.html


malha = False
escala_cacto = 1

def key_event(window,key,scancode,action,mods):
    global malha, escala_cacto

    if key == 77 and action == glfw.PRESS:
      malha = not malha
    
    if key == 88 and action == glfw.REPEAT:
      escala_cacto += 0.01

    if key == 90 and action == glfw.REPEAT:
      escala_cacto -= 0.01
        
    