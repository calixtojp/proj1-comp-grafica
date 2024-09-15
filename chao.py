import numpy as np
import random
from OpenGL.GL import *
import math
from uteis import *

class Chao:
  def __init__(self):

    #---------------CRIANDO A TERRA----------------#
    # preenchendo as coordenadas de cada vértice
    terra = [
      (-1, -0.5, 0),
      (+1, -0.5, 0),
      (-1, +0.5, 0),
      (+1, +0.5, 0),
    ]
    tam_terra = 4

    #----------------CRIANDO A GRAMA---------------#
    n_gramas = 66
    grama = []
    x = -1

    for i in range(n_gramas):
      # preenchendo as coordenadas de cada vértice 
      # automaticamente e acordo com o padrao da grama
      x += 0.03
      grama.append((x,        +0.35, 0))
      grama.append((x + 0.01, +0.35, 0))
      grama.append((x,        +0.55, 0))
      grama.append((x + 0.01, +0.55, 0))

    #-------------SETANDO OS VERTICES-------------#
    # preparando espaço de tamanho 'tam' para vértices usando 3 coordenadas (x,y,z)
    self.tam = tam_terra + n_gramas*4

    self.vertices = np.zeros(self.tam, [("position", np.float32, 3)])
    self.vertices['position'] = np.array(grama + terra, np.float32)

    self.r_len = len(self.vertices['position'])


  def multiplica_matriz(self,a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c

  def desenhar(self, program, loc_color, pos):
        
    mat_translacao = get_matriz_translacao(0, -0.5, 0)
    
    mat_transform = mat_translacao

    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)
    
    #Grama    
    glUniform4f(loc_color, 0.3, 0.44, 0.26, 1)  
    glDrawArrays(GL_TRIANGLE_STRIP, pos, self.tam-4)

    #Terra
    glUniform4f(loc_color, 0.78, 0.6, 0.35, 1)  
    glDrawArrays(GL_TRIANGLE_STRIP, pos+self.tam-4, 4)
