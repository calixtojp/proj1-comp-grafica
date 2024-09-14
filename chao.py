import numpy as np
import random
from OpenGL.GL import *
import math

class Chao:
  def __init__(self):
    self.d = 0
    self.t_x = 0
    self.t_y = -0.5

    # preparando espaço para 4 vértices usando 3 coordenadas (x,y,z)
    self.vertices = np.zeros(4, [("position", np.float32, 3)])

    # preenchendo as coordenadas de cada vértice
    self.vertices['position'] = [
      # Face 1 do Cubo (vértices do quadrado)
      (-1, -0.5, +0.2),
      (+1, -0.5, +0.2),
      (-1, +0.5, +0.2),
      (+1, +0.5, +0.2),
  ]

  def multiplica_matriz(self,a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c

  def desenhar(self, program, loc_color, pos):
      
      ### apenas para visualizarmos o cubo rotacionando
      #self.d -= 0.001 # modifica o angulo de rotacao em cada iteracao
      cos_d = math.cos(self.d)
      sin_d = math.sin(self.d)
      
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
      
      mat_translacao = np.array([     1.0,  0.0, 0.0,     self.t_x, 
                                      0.0,    1.0,   0.0, self.t_y, 
                                      0.0,    0.0,   1.0, 0.0, 
                                      0.0,    0.0,   0.0, 1.0], np.float32)


      # sequencia de transformações: rotação z, rotação y, rotação x, translação
      mat_transform = self.multiplica_matriz(mat_rotation_z,mat_rotation_y)
      mat_transform = self.multiplica_matriz(mat_rotation_x,mat_transform)
      mat_transform = self.multiplica_matriz(mat_translacao,mat_transform) #translacao ultima


      loc = glGetUniformLocation(program, "mat_transformation")
      glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)
      
      
      glUniform4f(loc_color, 0.49, 0.33, 0.10, 1)  ### brown 
      glDrawArrays(GL_TRIANGLE_STRIP, 0+pos, 4)