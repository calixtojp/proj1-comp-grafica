import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random

class Cacto:  
    def __init__(self, matrix, models):
        self.matrix = matrix
        self.m = models

        self.vertices_list = []    
        self.textures_coord_list = []

        modelo = self.m.load_model_from_file('cacto/cacto2.obj')

        ### inserindo vertices do modelo no vetor de vertices
        for face in modelo['faces']:
            for vertice_id in face[0]:
                self.vertices_list.append( modelo['vertices'][vertice_id-1] )
            for texture_id in face[1]:
                self.textures_coord_list.append( modelo['texture'][texture_id-1] )

        #Converter para numpy array p
        self.vertices_list = np.array(self.vertices_list, dtype=np.float32)
        self.textures_coord_list = np.array(self.textures_coord_list, dtype=np.float32)


        ### carregando textura equivalente e definindo um id (buffer): use um id por textura!
        self.m.load_texture_from_file(3,'cacto/cacto.jpg')

    def desenha(self, program, pos):
        # aplica a matriz model
        
        # rotacao
        angle = -90
        r_x = 1.0; r_y = 0.0; r_z = 0.0
        
        # translacao
        t_x = 15.0; t_y = -5.0; t_z = 0.0
        
        # escala
        s_x = 0.1; s_y = 0.1; s_z = 0.1 
        
        mat_model = self.matrix.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_FALSE, mat_model)
        
        
        #define id da textura do modelo
        glBindTexture(GL_TEXTURE_2D, 3)
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, pos, len(self.vertices_list)) ## renderizando
        
        