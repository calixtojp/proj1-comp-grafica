import numpy as np
import random
from OpenGL.GL import *
import math

PI = 3.141592

class Esfera:
    def __init__(self, r):
        self.r = r
        self.num_sectors = 32
        self.num_stacks = 32

        self.sector_step = (PI*2)/self.num_sectors
        self.stack_step = PI/self.num_stacks

        self.vertices = []
        self.cria_esfera()

        self.d = 0


    #Entrada: angulo de t, altura h, raio r
    # Saida: coordenadas no cilindro
    def CoordCilindro(self, t, h, r):
        x = r * math.cos(t)
        y = r * math.sin(t)
        z = h
        return (x,y,z)

    def multiplica_matriz(self,a,b):
        m_a = a.reshape(4,4)
        m_b = b.reshape(4,4)
        m_c = np.dot(m_a,m_b)
        c = m_c.reshape(1,16)
        return c


    def cria_esfera(self):
        print("Criando esfera")
        # vamos gerar um conjunto de vertices representantes poligonos
        # para a superficie da esfera.
        # cada poligono eh representado por dois triangulos
        vertices_list = []
        for i in range(0, self.num_sectors): # para cada sector (longitude)
            for j in range(0, self.num_stacks): # para cada stack (latitude)
                
                
                
                u = i * self.sector_step # angulo setor
                v = j * self.stack_step # angulo stack
                
                un = 0 # angulo do proximo sector
                if i+1==self.num_sectors:
                    un = PI*2
                else: un = (i+1)*self.sector_step
                    
                vn = 0 # angulo do proximo stack
                if j+1==self.num_stacks:
                    vn = PI
                else: vn = (j+1)*self.stack_step
                
                # vertices do poligono
                p0=self.CoordCilindro(u, v, self.r)
                p1=self.CoordCilindro(u, vn, self.r)
                p2=self.CoordCilindro(un, v, self.r)
                p3=self.CoordCilindro(un, vn, self.r)
                
                # triangulo 1 (primeira parte do poligono)
                vertices_list.append(p0)
                vertices_list.append(p2)
                vertices_list.append(p1)
                
                # triangulo 2 (segunda e ultima parte do poligono)
                vertices_list.append(p3)
                vertices_list.append(p1)
                vertices_list.append(p2)


        total_vertices = len(vertices_list)
        self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
        self.vertices['position'] = np.array(vertices_list)

    def desenhar(self, program, loc_color, pos):
        
        ### apenas para visualizarmos a esfera rotacionando
        self.d -= 0.001
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
        
        mat_transform = self.multiplica_matriz(mat_rotation_z, mat_rotation_x)
        mat_transform = self.multiplica_matriz(mat_rotation_y, mat_transform)

        loc = glGetUniformLocation(program, "mat_transformation")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

        for triangle in range(0, len(self.vertices), 3):
            random.seed(triangle)
            R = random.random()
            G = random.random()
            B = random.random()

            glUniform4f(loc_color, R, G, B, 1.0)
            glDrawArrays(GL_TRIANGLES, triangle, 3)
