import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random
from uteis import *


# Entrada: angulo de t, altura h, raio r
# Saida: coordenadas no cilindro
def CoordCilindro(t, h, r):
  x = r * math.cos(t)
  y = r * math.sin(t)
  z = h
  return (x,y,z)


def CIRILO(h,r):

  num_sectors = 20 # qtd de sectors (longitude)
  num_stacks = 20 # qtd de stacks (latitude)

  # grid sectos vs stacks (longitude vs latitude)
  sector_step = (PI*2)/num_sectors # variar de 0 até 2π
  stack_step = h/num_stacks # variar de 0 até H

  # vamos gerar um conjunto de vertices representantes poligonos
  # para a superficie da esfera.
  # cada poligono eh representado por dois triangulos
  vertices_list = []
  for j in range(0,num_stacks): # para cada stack (latitude)
      
    for i in range(0,num_sectors): # para cada sector (longitude) 
        
      u = i * sector_step # angulo setor
      v = j * stack_step # altura da stack
      
      un = 0 # angulo do proximo sector
      if i+1==num_sectors:
          un = PI*2
      else: un = (i+1)*sector_step
          
      vn = 0 # altura da proxima stack
      if j+1==num_stacks:
          vn = h
      else: vn = (j+1)*stack_step
      
      # verticies do poligono
      p0=CoordCilindro(u, v, r)
      p1=CoordCilindro(u, vn, r)
      p2=CoordCilindro(un, v, r)
      p3=CoordCilindro(un, vn, r)
      
      # triangulo 1 (primeira parte do poligono)
      vertices_list.append(p0)
      vertices_list.append(p2)
      vertices_list.append(p1)
      
      # triangulo 2 (segunda e ultima parte do poligono)
      vertices_list.append(p3)
      vertices_list.append(p1)
      vertices_list.append(p2)
      
      if v == 0:
          vertices_list.append(p0)
          vertices_list.append(p2)
          vertices_list.append(CoordCilindro(0, v, 0))
      if vn == h:
          #faz um triangulo a partir do mesmo angulo u, mas com as alturas em h = vn
          vertices_list.append(p1)
          vertices_list.append(p3)
          vertices_list.append(CoordCilindro(0, vn, 0))

  total_vertices = len(vertices_list)
  vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
  vertices['position'] = np.array(vertices_list)

  return vertices
  

def multiplica_matriz(a,b):
  m_a = a.reshape(4,4)
  m_b = b.reshape(4,4)
  m_c = np.dot(m_a,m_b)
  c = m_c.reshape(1,16)
  return c

def desenhar(program, vertices, loc_color):
  ### apenas para visualizarmos o cilindro rotacionando
  global d
  d -= 0.01 # modifica o angulo de rotacao em cada iteracao
  cos_d = math.cos(d)
  sin_d = math.sin(d)

  mat_rotation_z = np.array([     cos_d, -sin_d, 0.0, 0.0, 
                                  sin_d,  cos_d, 0.0, 0.0, 
                                  0.0,      0.0, 1.0, 0.0, 
                                  0.0,      0.0, 0.0, 1.0], np.float32)

  mat_rotation_x = np.array([     1.0,   0.0,    0.0, 0.0, 
                                  0.0, cos_d, -sin_d, 0.0, 
                                  0.0, sin_d,  cos_d, 0.0, 
                                  0.0,   0.0,    0.0, 1.0], np.float32)

  mat_rotation_y = np.array([     cos_d,  0.0, sin_d, 0.0, 
                                  0.0,    1.0,   0.0, 0.0, 
                                  -sin_d, 0.0, cos_d, 0.0, 
                                  0.0,    0.0,   0.0, 1.0], np.float32)

  mat_transform = multiplica_matriz(mat_rotation_z,mat_rotation_x)
  mat_transform = multiplica_matriz(mat_rotation_y,mat_transform)

  # a matriz de transformação é passada para o shader, que aplicará 
  # essa rotação a todos os vértices do objeto.
  loc = glGetUniformLocation(program, "mat_transformation")
  glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

  
  for triangle in range(0,len(vertices),3):  
    random.seed( triangle )
    R = random.random()
    G = random.random()
    B = random.random()  

    # Essa parte aqui faz o desenho 
    glUniform4f(loc_color, R, G, B, 1.0)
    glDrawArrays(GL_TRIANGLES, triangle, 3)     

def main():
   
  window = janela()
  program = programa()

  vertices = CIRILO(0.9, 0.1)

  passar_para_gpu(program, vertices)

  # Não sei oq exatamente isso faz, mas no notebook do professor, 
  # tá falando q pega a localização da variável de cor (uniform) do Fragment Shader
  # pra poder alterar ela no laço da janela. N sei oq significa.

  loc_color = glGetUniformLocation(program, "color")

  #ângulo de rotação do objeto. Inicialmente é zero, mas vai sendo decrementada 
  # a cada iteração para gerar o movimento de rotação.
  global d
  d = 0.0

  while not glfw.window_should_close(window):

    glfw.poll_events() #Leitura de eventos da janela
    
    # Limpa a tela para preparar o próximo quadro.
    # O fundo é definido como branco (1.0, 1.0, 1.0, 1.0).
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    if False:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    desenhar(program, vertices, loc_color)
    
    glfw.swap_buffers(window)

  glfw.terminate()


if __name__ == "__main__":
    main()
