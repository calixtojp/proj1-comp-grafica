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

        self.rotacoes = {'angle': 0.0, 'r_x': 0.0, 'r_y': 0.0, 'r_z': 1.0}
        self.translacoes = {'t_x': 0.0, 't_y': 0.0, 't_z': 0.0}
        self.escalas = {'s_x': 1.0, 's_y': 1.0, 's_z': 1.0}
        self.iluminacao = {'ka': 1.0, 'kd': 1.0, 'ks': 1.0, 'ns': 1.0}
        self.tipo = "refletor"

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

    def desenha(self, program, pos_ini):
        # aplica a matriz model
        mat_model = self.matrix.model(
            self.rotacoes['angle'], self.rotacoes['r_x'], self.rotacoes['r_y'], self.rotacoes['r_z'],
            self.translacoes['t_x'], self.translacoes['t_y'], self.translacoes['t_z'],
            self.escalas['s_x'], self.escalas['s_y'], self.escalas['s_z']
        )
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_FALSE, mat_model)
        
        loc_ka = glGetUniformLocation(program, "ka") # recuperando localizacao da variavel ka na GPU
        glUniform1f(loc_ka, self.iluminacao['ka']) # envia ka pra gpu
        loc_kd = glGetUniformLocation(program, "kd") # recuperando localizacao da variavel kd na GPU
        glUniform1f(loc_kd, self.iluminacao['kd']) ### envia kd pra gpu
        
        loc_ks = glGetUniformLocation(program, "ks") # recuperando localizacao da variavel ks na GPU
        glUniform1f(loc_ks, self.iluminacao['ks']) ### envia ks pra gpu        
    
        loc_ns = glGetUniformLocation(program, "ns") # recuperando localizacao da variavel ns na GPU
        glUniform1f(loc_ns, self.iluminacao['ns']) ### envia ns pra gpu  
        
        if self.tipo == "emissor":
            loc_light_pos = glGetUniformLocation(program, "lightPos") # recuperando localizacao da variavel lightPos na GPU
            glUniform3f(loc_light_pos, self.translacoes['t_x'], self.translacoes['t_y'], self.translacoes['t_z']) ### posicao da fonte de luz
        
        # define id da textura do modelo
        glBindTexture(GL_TEXTURE_2D, self.id_tex)
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, pos_ini, len(self.vertices_list)) ## renderizando