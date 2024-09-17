import numpy as np
import random
from OpenGL.GL import *
import uteis as ut
from esfera import Esfera

class Nuvem:
    def __init__(self, quantidade_esferas, intervalo_raios, espalhamento=1):
        self.quantidade_esferas = quantidade_esferas
        self.intervalo_raios = intervalo_raios
        self.esferas = []
        self.posicoes = []  # Lista para armazenar as posições de cada esfera

        # Criar as esferas com raios aleatórios dentro do intervalo e armazenar seus vértices
        vertices = []
        P_x, P_y, P_z = 0.6, 0.5, 1 # Posição inicial da primeira esfera
        R_anterior = 0  # Raio anterior, usado para gerar a variação nas posições

        for _ in range(quantidade_esferas):
            raio = random.uniform(intervalo_raios[0], intervalo_raios[1])
            esfera = Esfera(raio)
            self.esferas.append(esfera)

            # Gerar a posição para a esfera atual
            if len(self.posicoes) > 0:  # Para as esferas subsequentes

                P_x += random.uniform(R_anterior*espalhamento*(-1), R_anterior*espalhamento*(1))
                P_y += random.uniform(R_anterior*espalhamento*(-0.5), R_anterior*espalhamento*(0.5))
                # P_z += random.uniform(lim_inferior, lim_superior)

            self.posicoes.append((P_x, P_y, P_z))

            # Concatenar os vértices de cada esfera
            if len(vertices) == 0:
                vertices = esfera.vertices['position']
            else:
                vertices = np.concatenate((vertices, esfera.vertices['position']))

            R_anterior = raio  # Atualizar o raio anterior

        # Armazenar todos os vértices em uma variável só
        total_vertices = len(vertices)
        self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
        self.vertices['position'] = vertices

        # Guardar o tamanho total dos vértices para facilitar o desenho
        self.tam = total_vertices

    def multiplica_matriz(self, a, b):
        m_a = a.reshape(4, 4)
        m_b = b.reshape(4, 4)
        m_c = np.dot(m_a, m_b)
        c = m_c.reshape(1, 16)
        return c

    def desenhar(self, program, loc_color, pos):
        pos_atual = pos
        offset = 0  # Índice para percorrer os vértices da nuvem

        # Percorrer as esferas e desenhá-las em suas posições fixas
        for i, esfera in enumerate(self.esferas):
            P_x, P_y, P_z = self.posicoes[i]  # Pegar a posição predefinida da esfera

            # Definir a translação da esfera
            mat_translation = ut.get_matriz_translacao(P_x, P_y, P_z)

            # Aplicar a matriz de transformação (somente translação aqui)
            loc = glGetUniformLocation(program, "mat_transformation")
            glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)

            # Definir a cor das esferas (brancas)
            glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)

            # Desenhar a esfera atual usando GL_TRIANGLES
            glDrawArrays(GL_TRIANGLES, pos_atual + offset, esfera.tam)
            offset += esfera.tam  # Atualizar o offset para a próxima esfera