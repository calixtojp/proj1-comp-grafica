import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random

malha = False
escala_cacto = 1
homem_x = 0
homem_y = 0
nave_x = homem_x
nave_y = homem_y
rotacao_nave = 0


def janela():
  #Essa função garante configurações iniciais da janela

  glfw.init()
  glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
  window = glfw.create_window(700, 700, "Projeto 1", None, None)
  glfw.make_context_current(window)
  glfw.show_window(window)

  #Isso garante que o OpenGL renderize objetos 3D corretamente, levando em consideração 
  #a profundidade dos vértices e ocultando superfícies que deveriam estar atrás de outras.
  glEnable(GL_DEPTH_TEST) ### importante para 3D

  return window

def programa():
  #Essa função garante configurações iniciais do programa

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
  
  # Pedindo programa e slots de shader para a GPU
  program  = glCreateProgram()
  vertex   = glCreateShader(GL_VERTEX_SHADER)
  fragment = glCreateShader(GL_FRAGMENT_SHADER)

  # Definindo fonte do shader
  glShaderSource(vertex, vertex_code)
  glShaderSource(fragment, fragment_code)

  # Compilando shaders
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

  # Atribuindo objetos do shader para o programa
  glAttachShader(program, vertex)
  glAttachShader(program, fragment)

  # Criando programa
  glLinkProgram(program)
  if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
    
  # Fazendo esse programa ser o padrão
  glUseProgram(program)
  return program

def passar_para_gpu(program, vertices):
  #função que passa os os vérticese criados em CPU para a GPU a partir de um programa

  # Pedindo um buffer para a GPU
  buffer = glGenBuffers(1)

  # Tornando esse buffer o padrão
  glBindBuffer(GL_ARRAY_BUFFER, buffer)

  # Fazendo upload dos dados 
  glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
  glBindBuffer(GL_ARRAY_BUFFER, buffer)

    # Calcula o espaçamento entre os dados de vértices no buffer
  stride = vertices.strides[0]
  offset = ctypes.c_void_p(0)

    # Conecta o atributo de posição do buffer com o shader
  loc = glGetAttribLocation(program, "position")
  glEnableVertexAttribArray(loc)
  glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

def get_matriz_rotacao_x(angulo):
  #gera uma matriz de rotação em x a partir de um dado ângulo

  cos_x = math.cos(angulo)
  sin_x = math.sin(angulo)

  mat_rot_x = np.array([    1.0,   0.0,    0.0, 0.0, 
                            0.0, cos_x, -sin_x, 0.0, 
                            0.0, sin_x,  cos_x, 0.0, 
                            0.0,   0.0,    0.0, 1.0], np.float32)
  
  return mat_rot_x

def get_matriz_rotacao_y(angulo):
  #gera uma matriz de rotação em y a partir de um dado ângulo
  cos_y = math.cos(angulo)
  sin_y = math.sin(angulo)

  mat_rot_y = np.array([    cos_y,  0.0, sin_y, 0.0, 
                            0.0,    1.0,   0.0, 0.0, 
                           -sin_y, 0.0, cos_y, 0.0, 
                            0.0,    0.0,   0.0, 1.0], np.float32)

  return mat_rot_y

def get_matriz_rotacao_z(angulo):
  #gera uma matriz de rotação em z a partir de um dado ângulo
  cos_z = math.cos(angulo)
  sin_z = math.sin(angulo)

  mat_rot_z = np.array([    cos_z, -sin_z, 0.0, 0.0, 
                            sin_z,  cos_z, 0.0, 0.0, 
                            0.0,      0.0, 1.0, 0.0, 
                            0.0,      0.0, 0.0, 1.0], np.float32)
  
  return mat_rot_z

def get_matriz_translacao(tx,ty,tz):
  #gera uma matriz de translação a partir de dadas posições

  mat_translacao = np.array([     1.0,   0.0,    0.0, tx, 
                                  0.0,   1.0,    0.0, ty, 
                                  0.0,   0.0,    1.0, tz, 
                                  0.0,   0.0,    0.0, 1.0], np.float32)
  
  return mat_translacao

def get_matriz_escala(sx, sy, sz):
  #gera uma matriz de escala a partir de dadas proporções
  mat_escala = np.array([       sx,   0.0,    0.0, 0.0, 
                                0.0,   sy,    0.0, 0.0, 
                                0.0,   0.0,   sz,  0.0, 
                                0.0,   0.0,   0.0, 1.0], np.float32)

  return mat_escala    

def multiplica_matriz(a,b):
    #multiplica matrizes 4x4

    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c


def key_event(window,key,scancode,action,mods):
    #Trata de interações da cena com o teclado

    global malha, escala_cacto, homem_x, homem_y, rotacao_nave

    if key == 80 and action == glfw.PRESS: # tecla P
      malha = not malha
    
    if key == 88 and action == glfw.REPEAT: # tecla X
      escala_cacto += 0.01

    if key == 90 and action == glfw.REPEAT: # tecla Z
      escala_cacto -= 0.01

    if key == 262 and action == glfw.REPEAT: # tecla seta direita
      homem_x += 0.01

    if key == 263 and action == glfw.REPEAT: # tecla seta esquerda 
      homem_x -= 0.01

    if key == 265 and action == glfw.REPEAT: # tecla seta cima
      homem_y += 0.01

    if key == 264 and action == glfw.REPEAT: # tecla seta baixo
      homem_y -= 0.01

    if key == 65 and action == glfw.REPEAT: # tecla A
      rotacao_nave += 0.02

    if key == 83 and action == glfw.REPEAT: # tecla S
      rotacao_nave -= 0.02
    