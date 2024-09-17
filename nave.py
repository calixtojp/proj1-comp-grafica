import numpy as np
import random
from OpenGL.GL import *
import math
import cilindro
import esfera
import uteis as ut

PI = 3.141592 

class Nave:
  def __init__(self, tamanho):

    self.raio_esfera_central = 0.1
    self.raio_cilindro_central = 0.5
    self.raio_cilindro_externo = 0.9
    self.altura_cilindro_central = 0.18
    self.altura_cilindro_externo = 0.1

    #vermelho
    self.esfera_central = esfera.Esfera(0.3*tamanho)

    #azul
    self.cilindro_central = cilindro.Cilindro(
      self.altura_cilindro_central*tamanho,
      self.raio_cilindro_central*tamanho)
    
    #verde
    self.cilindro_externo = cilindro.Cilindro(
      self.altura_cilindro_externo*tamanho,
      self.raio_cilindro_externo*tamanho)
    
    # #amarelo
    self.qtd_cilindros_abducao = 4
    self.cilindros_abducao = []
    #primeiro criado o mais de fora e dps o mais de dentro
    for i in range(self.qtd_cilindros_abducao):
      self.cilindros_abducao.append(cilindro.Cilindro(1.38, (self.raio_esfera_central*(1.7))-(i*0.1)))# de fora pra dentro

    v = np.concatenate((self.esfera_central.vertices['position'], self.cilindro_central.vertices['position']))
    v = np.concatenate((v, self.cilindro_externo.vertices['position']))
    for i in range(self.qtd_cilindros_abducao):
      v = np.concatenate((v, self.cilindros_abducao[i].vertices['position']))

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
  

  def desenhar(self, program, loc_color, pos, rotacao):
    pos_atual = pos

    pos_esfera_central_x = -0.5
    pos_esfera_central_y = 0.5
    pos_esfera_central_z = 0

    angulo_cilindros_x = rotacao
    angulo_cilindros_y = (math.pi)/ 1.8
    angulo_cilindros_z = (math.pi) / 2


    #----------------------Desenhando a esfera central----------------------------#
    # Criação das matrizes de rotação (se necessário)
    mat_rotation_x = ut.get_matriz_rotacao_x(0)
    mat_rotation_y = ut.get_matriz_rotacao_y(0)
    mat_rotation_z = ut.get_matriz_rotacao_z(0)

    # Translação
    mat_translation = ut.get_matriz_translacao(-0.5, 0.54, 0)

    # Aplicando transformações
    mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

    # A matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    # Pintando a esfera de vermelho
    glUniform4f(loc_color, 1, 0.0, 0.0, 1.0)  # vermelho

    # Desenhando a esfera usando GL_TRIANGLES
    glDrawArrays(GL_TRIANGLES, pos_atual, len(self.esfera_central.vertices))

    pos_atual += len(self.esfera_central.vertices)  # Atualizando a posição atual da GPU


    #----------------------Desenhando o cilindro interno/central----------------------------#

    #rotações
    mat_rotation_x = ut.get_matriz_rotacao_x(angulo_cilindros_x)
    mat_rotation_y = ut.get_matriz_rotacao_y(angulo_cilindros_y)
    mat_rotation_z = ut.get_matriz_rotacao_z(angulo_cilindros_z)

    #translação
    mat_translation = ut.get_matriz_translacao(-0.5, 0.48, 0)

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
    mat_rotation_x = ut.get_matriz_rotacao_x(angulo_cilindros_x)
    mat_rotation_y = ut.get_matriz_rotacao_y(angulo_cilindros_y)
    mat_rotation_z = ut.get_matriz_rotacao_z(angulo_cilindros_z)

    #translação
    mat_translation = ut.get_matriz_translacao(-0.5, 0.5, 0)

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

    #----------------------Desenhando Cilindro abdução--------------# 153 255 153 | 0.6 1 0.6
    for cilindro_at in range(self.qtd_cilindros_abducao):
      fator_mult = (self.qtd_cilindros_abducao-cilindro_at)/(self.qtd_cilindros_abducao)
      print(f"fator mult: {fator_mult}")
      #rotações
      mat_rotation_x = ut.get_matriz_rotacao_x(0)
      mat_rotation_y = ut.get_matriz_rotacao_y(angulo_cilindros_y)
      mat_rotation_z = ut.get_matriz_rotacao_z(angulo_cilindros_z)

      #translação
      mat_translation = ut.get_matriz_translacao(-0.5, -0.9, 0)

      #aplicando transformações
      mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
      mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
      mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

      # a matriz de transformação é passada para o shader
      loc = glGetUniformLocation(program, "mat_transformation")
      glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

      #pintando. 
      #Vai ficando menos transparente conforme o cilindro vai para o centro
      #começa pintando o mais de fora q é o mais transparente e mais claro e vai ficando mais escuro e sólido
      R = 0.6
      G = 1
      B = 0.6
      print(f"R: {R} G: {G} B: {B}")
      glUniform4f(loc_color, R, G, B, fator_mult)

      #desenhando
      glDrawArrays(GL_TRIANGLES, pos_atual, len(self.cilindro_externo.vertices))
      pos_atual += len(self.cilindro_externo.vertices) #atualizando a posição atual da GPU


    #----------------------Desenhando esferas do contorno--------------#
    # # Criação das matrizes de rotação (se necessário)
    # mat_rotation_x = ut.get_matriz_rotacao_x(0)
    # mat_rotation_y = ut.get_matriz_rotacao_y(0)
    # mat_rotation_z = ut.get_matriz_rotacao_z(0)

    # # Translação
    # mat_translation = ut.get_matriz_translacao(-0.5, 0.54, 0)

    # # Aplicando transformações
    # mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    # mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
    # mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

    # # A matriz de transformação é passada para o shader
    # loc = glGetUniformLocation(program, "mat_transformation")
    # glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    # # Pintando a esfera de vermelho
    # glUniform4f(loc_color, 1, 0.0, 0.0, 1.0)  # vermelho

    # # Desenhando a esfera usando GL_TRIANGLES
    # glDrawArrays(GL_TRIANGLES, pos_atual, len(self.esfera_central.vertices))

    # pos_atual += len(self.esfera_central.vertices)  # Atualizando a posição atual da GPU