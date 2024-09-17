import numpy as np
import random
from OpenGL.GL import *
import math
import cilindro
import esfera
import uteis as ut

PI = 3.141592 

class Nave:
  def __init__(self):

    # self.raio_esfera_central = 0.1
    # self.raio_cilindro_central = 0.3
    # self.raio_cilindro_externo = 0.7
    # self.altura_cilindro_central = 0.2
    # self.altura_cilindro_externo = 0.2

    self.esfera_central = esfera.Esfera(0.3)#vermelho
    self.cilindro_central = cilindro.Cilindro(0.15, 0.5)#azul
    self.cilindro_externo = cilindro.Cilindro(0.1, 0.9)#verde

    # v = np.concatenate((self.cilindro_central.vertices['position'], self.cilindro_externo.vertices['position']))

    v = np.concatenate((self.esfera_central.vertices['position'], self.cilindro_central.vertices['position']))
    v = np.concatenate((v, self.cilindro_externo.vertices['position']))

    total_vertices = len(v)
    self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
    self.vertices['position'] = v

    # self.tam = len(self.cilindro_central.vertices) + len(self.cilindro_externo.vertices)
    print(f"tam esfera: {len(self.esfera_central.vertices)}")
    print(f"tam cilindro central: {len(self.cilindro_central.vertices)}")
    print(f"tam cilindro externo: {len(self.cilindro_externo.vertices)}")

    self.tam = len(self.esfera_central.vertices) + len(self.cilindro_central.vertices) + len(self.cilindro_externo.vertices)


  def multiplica_matriz(self,a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c
  

  def desenhar(self, program, loc_color, pos):
    pos_atual = pos

    #----------------------Desenhando a esfera central----------------------------#
    # Criação das matrizes de rotação (se necessário)
    mat_rotation_x = ut.get_matriz_rotacao_x(0)
    mat_rotation_y = ut.get_matriz_rotacao_y(0)
    mat_rotation_z = ut.get_matriz_rotacao_z(0)

    # Translação
    mat_translation = ut.get_matriz_translacao(0, 0, 0)

    # Aplicando transformações
    mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

    # A matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    # Pintando a esfera de vermelho
    glUniform4f(loc_color, 1.0, 0.0, 0.0, 1.0)  # vermelho

    # Desenhando a esfera usando GL_TRIANGLES
    glDrawArrays(GL_TRIANGLES, pos_atual, len(self.esfera_central.vertices))

    pos_atual += len(self.esfera_central.vertices)  # Atualizando a posição atual da GPU
    #----------------------Desenhando o cilindro interno/central----------------------------#
    #rotações
    mat_rotation_x = ut.get_matriz_rotacao_x(0)
    mat_rotation_y = ut.get_matriz_rotacao_y(2)
    mat_rotation_z = ut.get_matriz_rotacao_z(math.pi / 2)

    #translação
    mat_translation = ut.get_matriz_translacao(0, 0, 0)

    #aplicando transformações
    mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    #pintando
    glUniform4f(loc_color, 0.0, 0.0, 1, 1)#azul
    
    #desenhando
    glDrawArrays(GL_TRIANGLES, pos_atual, len(self.cilindro_central.vertices))
    pos_atual += len(self.cilindro_central.vertices) #atualizando a posição atual da GPU

    #----------------------Desenhando o cilindro externo----------------------------#
    #rotações
    mat_rotation_x = ut.get_matriz_rotacao_x(0)
    mat_rotation_y = ut.get_matriz_rotacao_y(2)
    mat_rotation_z = ut.get_matriz_rotacao_z(math.pi / 2)

    #translação
    mat_translation = ut.get_matriz_translacao(0, 0, 0)

    #aplicando transformações
    mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    #pintando
    glUniform4f(loc_color, 0.0, 0.5, 0.0, 1)#verde

    #desenhando
    glDrawArrays(GL_TRIANGLES, pos_atual, len(self.cilindro_externo.vertices))
    pos_atual += len(self.cilindro_externo.vertices) #atualizando a posição atual da GPU