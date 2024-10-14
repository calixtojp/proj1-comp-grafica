import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random
import models as m


class Arvore:  
    def __init__(self, matrix):
        self.matrix = matrix

        modelo = m.load_model_from_file('arvore/arvore10.obj')

        self.vertices_list = []    
        self.textures_coord_list = []

        ### inserindo vertices do modelo no vetor de vertices
        print('Processando modelo arvore.obj. Vertice inicial:', len(self.vertices_list))
        faces_visited = []
        for face in modelo['faces']:
            if face[2] not in faces_visited:
                print(face[2],' vertice inicial =', len(self.vertices_list))
                faces_visited.append(face[2])
            for vertice_id in face[0]:
                self.vertices_list.append(modelo['vertices'][vertice_id-1])
            for texture_id in face[1]:
                self.textures_coord_list.append(modelo['texture'][texture_id-1])
        print('Processando modelo arvore.obj. Vertice final:', len(self.vertices_list))

        #Converter para numpy array p
        self.vertices_list = np.array(self.vertices_list, dtype=np.float32)
        self.textures_coord_list = np.array(self.textures_coord_list, dtype=np.float32)


        ### carregando textura equivalente e definindo um id (buffer): use um id por textura!
        m.load_texture_from_file(0,'arvore/bark_0021.jpg')
        m.load_texture_from_file(1,'arvore/DB2X2_L01.png')

    def desenha_arvore(self,program):
        # aplica a matriz model
        
        # rotacao
        angle = 0.0
        r_x = 0.0; r_y = 0.0; r_z = 1.0
        
        # translacao
        t_x = 0.0; t_y = -5.0; t_z = 0.0
        
        # escala
        s_x = 5.0; s_y = 5.0; s_z = 5.0
        
        mat_model = self.matrix.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_FALSE, mat_model)
        
        
        ### desenho o tronco da arvore
        #define id da textura do modelo
        glBindTexture(GL_TEXTURE_2D, 0)
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, 0, 20262) ## renderizando
        
        ### desenho as folhas
        #define id da textura do modelo
        glBindTexture(GL_TEXTURE_2D, 1)
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, 20262, 41172-20262) ## renderizando
        

