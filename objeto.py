import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random

class Objeto:  
    def __init__(self, matrix, models, dir_obj, dir_tex, id_tex):
        self.matrix = matrix
        self.m = models
        self.id_tex = id_tex

        self.vertices_list = []    
        self.textures_coord_list = []
        self.normals_list = []

        modelo = self.m.load_model_from_file(dir_obj)

        ### inserindo vertices do modelo no vetor de vertices
        for face in modelo['faces']:
            for vertice_id in face[0]:
                a = len(modelo['vertices'][vertice_id-1])
                print(f'modelo["vertices"].lenght:{a}')
                self.vertices_list.append( modelo['vertices'][vertice_id-1] )
            for texture_id in face[1]:
                b = len(modelo['texture'][texture_id-1])
                print(f'modelo["texture"].lenght:{b}')
                self.textures_coord_list.append( modelo['texture'][texture_id-1] )
            for normal_id in face[2]:
                c = len(modelo['normals'][normal_id-1])
                print(f'modelo["normals"].lenght:{c}')
                self.normals_list.append( modelo['normals'][normal_id-1] )

        #Converter para numpy array p
        self.vertices_list = np.array(self.vertices_list, dtype=np.float32)
        self.textures_coord_list = np.array(self.textures_coord_list, dtype=np.float32)
        self.normals_list = np.array(self.normals_list, dtype=np.float32)


        ### carregando textura equivalente e definindo um id (buffer): use um id por textura!
        self.m.load_texture_from_file(id_tex, dir_tex)

    def desenha(self,program, pos_ini, angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, ka, kd, ks, ns, tipo):
        # aplica a matriz model
        
        # rotacao -> vc define o angulo em graus no angle e dps monta um vetor (x,x,x). Se x = 1, vai rodar no eixo. Se 0, não vai
        #angle = 0.0
        #r_x = 0.0; r_y = 0.0; r_z = 1.0 
        
        # translacao
        #t_x = 0.0; t_y = -5.0; t_z = 0.0
        
        # escala
        #s_x = 5.0; s_y = 5.0; s_z = 5.020262
        
        mat_model = self.matrix.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_FALSE, mat_model)
        
        loc_ka = glGetUniformLocation(program, "ka") # recuperando localizacao da variavel ka na GPU
        glUniform1f(loc_ka, ka) # envia ka pra gpu

        loc_kd = glGetUniformLocation(program, "kd") # recuperando localizacao da variavel kd na GPU
        glUniform1f(loc_kd, kd) ### envia kd pra gpu
        
        loc_ks = glGetUniformLocation(program, "ks") # recuperando localizacao da variavel ks na GPU
        glUniform1f(loc_ks, ks) ### envia ks pra gpu        
    
        loc_ns = glGetUniformLocation(program, "ns") # recuperando localizacao da variavel ns na GPU
        glUniform1f(loc_ns, ns) ### envia ns pra gpu  

        if tipo == "luz":
            loc_light_pos = glGetUniformLocation(program, "lightPos") # recuperando localizacao da variavel lightPos na GPU
            glUniform3f(loc_light_pos, t_x, t_y, t_z) ### posicao da fonte de luz

        
        #define id da textura do modelo
        glBindTexture(GL_TEXTURE_2D, self.id_tex)
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, pos_ini, len(self.vertices_list)) ## renderizando
        
        

