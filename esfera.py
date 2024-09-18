import numpy as np
import random
from OpenGL.GL import *
import math

PI = 3.141592

class Esfera:
    #Cria uma esfera a partir de um tamanho de raio qualquer r
    def __init__(self, r):
        self.r = r
        self.num_sectors = 32
        self.num_stacks = 32

        self.sector_step = (PI*2)/self.num_sectors
        self.stack_step = PI/self.num_stacks

        self.vertices = []
        self.cria_esfera()

        self.tam = len(self.vertices)

        self.d = 0

    def cria_esfera(self):
        vertices_list = []

        sector_step = 2 * PI / self.num_sectors  # passo para os setores (longitude)
        stack_step = PI / self.num_stacks        # passo para as stacks (latitude)

        for i in range(self.num_stacks):
            stack_angle1 = PI / 2 - i * stack_step        # ângulo da stack atual (latitude)
            stack_angle2 = PI / 2 - (i + 1) * stack_step  # ângulo da próxima stack
            xy1 = self.r * math.cos(stack_angle1)         # raio na coordenada xy da stack atual
            xy2 = self.r * math.cos(stack_angle2)         # raio na coordenada xy da próxima stack
            z1 = self.r * math.sin(stack_angle1)          # coordenada z da stack atual
            z2 = self.r * math.sin(stack_angle2)          # coordenada z da próxima stack

            for j in range(self.num_sectors):
                sector_angle = j * sector_step  # ângulo do setor (longitude)

                # Coordenadas da stack atual (pontos de um círculo)
                x1 = xy1 * math.cos(sector_angle)
                y1 = xy1 * math.sin(sector_angle)

                # Coordenadas da próxima stack (pontos do próximo círculo)
                x2 = xy2 * math.cos(sector_angle)
                y2 = xy2 * math.sin(sector_angle)

                # Próximo setor para conectar os triângulos
                next_sector_angle = (j + 1) * sector_step
                x1_next = xy1 * math.cos(next_sector_angle)
                y1_next = xy1 * math.sin(next_sector_angle)
                x2_next = xy2 * math.cos(next_sector_angle)
                y2_next = xy2 * math.sin(next_sector_angle)

                # Criação de dois triângulos para cada segmento
                vertices_list.append((x1, y1, z1))     # Primeiro triângulo
                vertices_list.append((x2, y2, z2))
                vertices_list.append((x1_next, y1_next, z1))

                vertices_list.append((x1_next, y1_next, z1))  # Segundo triângulo
                vertices_list.append((x2, y2, z2))
                vertices_list.append((x2_next, y2_next, z2))

        #coloca todos os vértices em um único vetor
        total_vertices = len(vertices_list)
        self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
        self.vertices['position'] = np.array(vertices_list)
