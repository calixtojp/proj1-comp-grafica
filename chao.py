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

  def desenhar(self, program, loc_color, pos):
    #coordena a grama e a terra para formar um chão na cena 

    mat_translacao = get_matriz_translacao(0, -0.5, 0)
    
    mat_transform = mat_translacao

    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)
    
    #Grama    
    glUniform4f(loc_color, 0.3, 0.44, 0.26, 1)  #pinta
    glDrawArrays(GL_TRIANGLE_STRIP, pos, self.tam-4) #desenha

    #Terra
    glUniform4f(loc_color, 0.78, 0.6, 0.35, 1)  #pinta
    glDrawArrays(GL_TRIANGLE_STRIP, pos+self.tam-4, 4) #desenha
