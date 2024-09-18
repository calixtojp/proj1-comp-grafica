import numpy as np
import random
from OpenGL.GL import *
import math
from cilindro import Cilindro
import uteis as ut

class Homem:  
  def __init__(self):
    #Define os cilindros que compõem o homem
    self.cilindro1 = Cilindro(0.25,   0.1)
    self.cilindro2 = Cilindro(0.3,   0.04)
    self.cilindro3 = Cilindro(0.3,   0.04)
    self.cilindro4 = Cilindro(0.25,   0.03)
    self.cilindro5 = Cilindro(0.25,   0.03)
    self.cilindro6 = Cilindro(0.1,   0.08)

    
    #concatena em um vetor só
    v = np.concatenate((self.cilindro1.vertices['position'], self.cilindro2.vertices['position']))
    v = np.concatenate((v, self.cilindro3.vertices['position']))
    v = np.concatenate((v, self.cilindro4.vertices['position']))
    v = np.concatenate((v, self.cilindro5.vertices['position']))
    v = np.concatenate((v, self.cilindro6.vertices['position']))

    total_vertices = len(v)
    self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
    self.vertices['position'] = v

    #tamanho de 1 cilindro no gpu
    self.c_tam = len(self.cilindro1.vertices)

    #tamanho total em gpu
    self.tam = self.c_tam*6

  def desenhar(self, program, loc_color, pos):
    # Coordena os cilindros para formar o desenho de um homem 
    # e trata as transformações e eventos do teclado


    #----------------------Desenhando o tronco do homem----------------------------#
    mat_rotation_x = ut.get_matriz_rotacao_x(0)
    mat_rotation_y = ut.get_matriz_rotacao_y(2)
    mat_rotation_z = ut.get_matriz_rotacao_z(math.pi / 2)
    mat_translation = ut.get_matriz_translacao(-0.5+ut.homem_x, -0.6+ut.homem_y, 0)

    mat_transform = ut.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = ut.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = ut.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    #Pintando
    glUniform4f(loc_color, 0.98, 0.98, 0.98, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos, self.c_tam) 


    #----------------------Desenhando a perna esquerda do homem----------------------------#
    mat_rotation_x = ut.get_matriz_rotacao_x(0)
    mat_rotation_y = ut.get_matriz_rotacao_y(1.6)
    mat_rotation_z = ut.get_matriz_rotacao_z(math.pi / 2)
    mat_translation = ut.get_matriz_translacao(-0.56+ut.homem_x, -0.9+ut.homem_y, 0)

    mat_transform = ut.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = ut.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = ut.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    #Pintando
    glUniform4f(loc_color, 0.2, 0.35, 0.92, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos+(self.c_tam*1), self.c_tam) 


    #----------------------Desenhando a perna direita do homem----------------------------#
    mat_rotation_x = ut.get_matriz_rotacao_x(0)
    mat_rotation_y = ut.get_matriz_rotacao_y(1.6)
    mat_rotation_z = ut.get_matriz_rotacao_z(math.pi / 2)
    mat_translation = ut.get_matriz_translacao(-0.44+ut.homem_x, -0.9+ut.homem_y, 0)

    mat_transform = ut.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = ut.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = ut.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    #Pintando
    glUniform4f(loc_color, 0.2, 0.35, 0.92, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos+(self.c_tam*2), self.c_tam) 


    #----------------------Desenhando o braco direito do homem----------------------------#
    mat_rotation_x = ut.get_matriz_rotacao_x(0)
    mat_rotation_y = ut.get_matriz_rotacao_y(2)
    mat_rotation_z = ut.get_matriz_rotacao_z(-0.5)
    mat_translation = ut.get_matriz_translacao(-0.41+ut.homem_x, -0.45+ut.homem_y, 0)

    mat_transform = ut.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = ut.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = ut.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    #Pintando
    glUniform4f(loc_color, 0.44, 0.31, 0.17, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos+(self.c_tam*3), self.c_tam) 


    #----------------------Desenhando o braco esquerdo do homem----------------------------#
    mat_rotation_x = ut.get_matriz_rotacao_x(0)
    mat_rotation_y = ut.get_matriz_rotacao_y(1.7)
    mat_rotation_z = ut.get_matriz_rotacao_z(0.5)
    mat_translation = ut.get_matriz_translacao(-0.81+ut.homem_x, -0.58+ut.homem_y, 0)

    mat_transform = ut.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = ut.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = ut.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    #Pintando
    glUniform4f(loc_color, 0.44, 0.31, 0.17, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos+(self.c_tam*4), self.c_tam) 


     #----------------------Desenhando a cabeca do homem----------------------------#
    mat_rotation_x = ut.get_matriz_rotacao_x(0)
    mat_rotation_y = ut.get_matriz_rotacao_y(1.9)
    mat_rotation_z = ut.get_matriz_rotacao_z(math.pi / 2)
    mat_translation = ut.get_matriz_translacao(-0.5+ut.homem_x, -0.35+ut.homem_y, -0.7)

    mat_transform = ut.multiplica_matriz(mat_rotation_x, mat_rotation_y)
    mat_transform = ut.multiplica_matriz(mat_rotation_z, mat_transform)
    mat_transform = ut.multiplica_matriz(mat_translation, mat_transform)

    # a matriz de transformação é passada para o shader
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    #Pintando
    glUniform4f(loc_color, 0.44, 0.31, 0.17, 1)
    #Desenhando
    glDrawArrays(GL_TRIANGLES, pos+(self.c_tam*5), self.c_tam) 