import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random
import glm

class Matrizes:

    def __init__(self, c):
        self.cameraPos   = glm.vec3(0.0,  0.0,  1.0)
        self.cameraFront = glm.vec3(0.0,  0.0, -1.0)
        self.cameraUp    = glm.vec3(0.0,  1.0,  0.0)

        self.inc_fov = 0
        self.inc_near = 0
        self.inc_far = 0
        self.inc_view_up = 0

        self.c = c
   
    def get_matriz_rotacao_x(self, angulo):
        #gera uma matriz de rotação em x a partir de um dado ângulo

        cos_x = math.cos(angulo)
        sin_x = math.sin(angulo)

        mat_rot_x = np.array([    1.0,   0.0,    0.0, 0.0, 
                                0.0, cos_x, -sin_x, 0.0, 
                                0.0, sin_x,  cos_x, 0.0, 
                                0.0,   0.0,    0.0, 1.0], np.float32)
    
        return mat_rot_x

    def get_matriz_rotacao_y(self, angulo):
        #gera uma matriz de rotação em y a partir de um dado ângulo
        cos_y = math.cos(angulo)
        sin_y = math.sin(angulo)

        mat_rot_y = np.array([    cos_y,  0.0, sin_y, 0.0, 
                                    0.0,    1.0,   0.0, 0.0, 
                                -sin_y, 0.0, cos_y, 0.0, 
                                    0.0,    0.0,   0.0, 1.0], np.float32)

        return mat_rot_y

    def get_matriz_rotacao_z(self, angulo):
        #gera uma matriz de rotação em z a partir de um dado ângulo
        cos_z = math.cos(angulo)
        sin_z = math.sin(angulo)

        mat_rot_z = np.array([    cos_z, -sin_z, 0.0, 0.0, 
                                    sin_z,  cos_z, 0.0, 0.0, 
                                    0.0,      0.0, 1.0, 0.0, 
                                    0.0,      0.0, 0.0, 1.0], np.float32)
        
        return mat_rot_z

    def get_matriz_translacao(self, tx,ty,tz):
        #gera uma matriz de translação a partir de dadas posições

        mat_translacao = np.array([     1.0,   0.0,    0.0, tx, 
                                        0.0,   1.0,    0.0, ty, 
                                        0.0,   0.0,    1.0, tz, 
                                        0.0,   0.0,    0.0, 1.0], np.float32)
        
        return mat_translacao

    def get_matriz_escala(self, sx, sy, sz):
        #gera uma matriz de escala a partir de dadas proporções
        mat_escala = np.array([       sx,   0.0,    0.0, 0.0, 
                                        0.0,   sy,    0.0, 0.0, 
                                        0.0,   0.0,   sz,  0.0, 
                                        0.0,   0.0,   0.0, 1.0], np.float32)

        return mat_escala    

    def multiplica_matriz(self, a,b):
        #multiplica matrizes 4x4

        m_a = a.reshape(4,4)
        m_b = b.reshape(4,4)
        m_c = np.dot(m_a,m_b)
        c = m_c.reshape(1,16)
        return c

    def model(self, angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
        
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

    def view(self):
        mat_view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp);
        mat_view = np.array(mat_view)
        return mat_view

    def projection(self):
        
        # perspective parameters: fovy, aspect, near, far
        mat_projection = glm.perspective(glm.radians(45.0), self.c.largura/self.c.altura, 0.1, 1000.0)
        mat_projection = np.array(mat_projection)    
        return mat_projection