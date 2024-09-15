import numpy as np
import random
from OpenGL.GL import *
import math
from cilindro import Cilindro
from uteis import *

class Cacto:  
  def __init__(self):
    self.cilindro1 = Cilindro(0.5,   0.1)
    self.cilindro2 = Cilindro(0.2,   0.05)
    self.cilindro3 = Cilindro(0.2,   0.05)
    self.cilindro4 = Cilindro(0.15,   0.03)
    self.cilindro5 = Cilindro(0.15,   0.03)

    

    #v = cilindro1.vertices['position']
    v = np.concatenate((self.cilindro1.vertices['position'], self.cilindro2.vertices['position']))
    v = np.concatenate((v, self.cilindro3.vertices['position']))
    v = np.concatenate((v, self.cilindro4.vertices['position']))
    v = np.concatenate((v, self.cilindro5.vertices['position']))

    total_vertices = len(v)
    self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
    self.vertices['position'] = v

    #tamanho de 1 cilindro no gpu
    self.c_tam = len(self.cilindro1.vertices)

    #tamanho total em gpu
    self.tam = self.c_tam*5




  def multiplica_matriz(self,a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c

  def desenhar(self, program, loc_color, pos):

    #----------------------Desenhando o tronco central do cacto----------------------------#

    mat_rotation_x = get_matriz_rotacao_x(0)
    mat_rotation_y = get_matriz_rotacao_y(1.5)
    mat_rotation_z = get_matriz_rotacao_z(math.pi / 2)
    mat_translation = get_matriz_translacao(0.5, -0.7, 0)

    mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    #Pintando
    glUniform4f(loc_color, 0.2, 0.4, 0.16, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos, self.c_tam) 

    #----------------------Desenhando o tronco vertical a direita do cacto----------------------------#
    mat_rotation_x = get_matriz_rotacao_x(0)
    mat_rotation_y = get_matriz_rotacao_y(1.5)
    mat_rotation_z = get_matriz_rotacao_z(math.pi / 2)
    mat_translation = get_matriz_translacao(0.7, -0.42, 0)

    mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader, que aplicará 
    # essa rotação a todos os vértices do objeto.
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)


    #Pintando
    glUniform4f(loc_color, 0.2, 0.4, 0.16, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos+(self.c_tam*1), self.c_tam)

    #----------------------Desenhando o tronco vertical a esquerda do cacto----------------------------#
    mat_rotation_x = get_matriz_rotacao_x(0)
    mat_rotation_y = get_matriz_rotacao_y(1.5)
    mat_rotation_z = get_matriz_rotacao_z(math.pi / 2)
    mat_translation = get_matriz_translacao(0.3, -0.5, 0)

    mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader, que aplicará 
    # essa rotação a todos os vértices do objeto.
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)


    #Pintando
    glUniform4f(loc_color, 0.2, 0.4, 0.16, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos+(self.c_tam*2), self.c_tam)             

    #----------------------Desenhando o tronco horizontal a esquerda do cacto----------------------------#
    mat_rotation_x = get_matriz_rotacao_x(0)
    mat_rotation_y = get_matriz_rotacao_y(1.5)
    mat_rotation_z = get_matriz_rotacao_z(0)
    mat_translation = get_matriz_translacao(0.25, -0.50, 0)

    mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader, que aplicará 
    # essa rotação a todos os vértices do objeto.
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)


    #Pintando
    glUniform4f(loc_color, 0.2, 0.4, 0.16, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos+(self.c_tam*3), self.c_tam)    

    #----------------------Desenhando o tronco horizontal a esquerda do cacto----------------------------#
    mat_rotation_x = get_matriz_rotacao_x(0)
    mat_rotation_y = get_matriz_rotacao_y(1.5)
    mat_rotation_z = get_matriz_rotacao_z(0)
    mat_translation = get_matriz_translacao(0.60, -0.45, 0)

    mat_transform = self.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = self.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = self.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader, que aplicará 
    # essa rotação a todos os vértices do objeto.
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)


    #Pintando
    glUniform4f(loc_color, 0.2, 0.4, 0.16, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos+(self.c_tam*4), self.c_tam)    