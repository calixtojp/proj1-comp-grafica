import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random
import glm


def janela():
  #Essa função garante configurações iniciais da janela

  glfw.init()
  glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
  window = glfw.create_window(1600, 12200, "Projeto 2", None, None)
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
        attribute vec2 texture_coord;
        varying vec2 out_texture;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
        }
        """
  
  fragment_code = """
        uniform vec4 color;
        varying vec2 out_texture;
        uniform sampler2D samplerTexture;
        
        void main(){
            vec4 texture = texture2D(samplerTexture, out_texture);
            gl_FragColor = texture;
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

def passar_para_gpu(program, item, modo):
  #função que passa os objetos ou as texturas para a GPU a partir de um programa a depender do modo escolhido
  print(f"MODOOOOOOO ========================= {modo}")
  print(type(item))
  print(item.shape)
  print("-------------------------------------------------------------------")

  #configurações padrão para passar os vértices
  shader_var = "position"
  num = 2

  #caso queiramos passar a textura, alteramos as config
  if(modo=="textura"):
    shader_var = "texture_coord"
    num = 3

  # Pedindo um buffer para a GPU
  buffer = glGenBuffers(1)

  # Tornando esse buffer o padrão
  glBindBuffer(GL_ARRAY_BUFFER, buffer)

  # Fazendo upload dos dados 
  glBufferData(GL_ARRAY_BUFFER, item.nbytes, item, GL_STATIC_DRAW)

  # Calcula o espaçamento entre os dados de vértices no buffer
  stride = item.strides[0]
  offset = ctypes.c_void_p(0)

  # Conecta o atributo de posição do buffer com o shader
  loc = glGetAttribLocation(program, shader_var)
  glEnableVertexAttribArray(loc)
  glVertexAttribPointer(loc, num, GL_FLOAT, False, stride, offset)


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

def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    
    angle = math.radians(angle)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade

    
    # aplicando translacao
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando rotacao
    matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
    
    # aplicando escala
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    
    matrix_transform = np.array(matrix_transform).T # pegando a transposta da matriz (glm trabalha com ela invertida)
    
    return matrix_transform



cameraPos   = glm.vec3(0.0,  0.0,  1.0);
cameraFront = glm.vec3(0.0,  0.0, -1.0);
cameraUp    = glm.vec3(0.0,  1.0,  0.0);

inc_fov = 0
inc_near = 0
inc_far = 0
inc_view_up = 0

altura = 1600
largura = 1200

def view():
    global cameraPos, cameraFront, cameraUp
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
    mat_view = np.array(mat_view)
    return mat_view

def projection():
    global altura, largura, inc_fov, inc_near, inc_far
    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(glm.radians(45.0), largura/altura, 0.1, 1000.0)
    mat_projection = np.array(mat_projection)    
    return mat_projection