from lua import Lua
from OpenGL.GL import *
import numpy as np
import math

class Objetos:
    def __init__(self):
        self.lua = Lua()
        self.angle_x = 0.0  # Inicialização do ângulo de rotação no eixo X
        self.angle_y = 0.0  # Inicialização do ângulo de rotação no eixo Y
        self.angle_z = 0.0  # Inicialização do ângulo de rotação no eixo Z

        # Buffers para a lua
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.cbo = glGenBuffers(1)

        self.setup_lua()

    def setup_lua(self):
        glBindVertexArray(self.vao)

        # Carregar vértices da Lua
        vertices = self.lua.get_vertices()
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Atributo de posição
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, None)

        # Carregar cores
        colors = self.lua.get_colors()
        glBindBuffer(GL_ARRAY_BUFFER, self.cbo)
        glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)

        # Atributo de cor
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(4, GL_FLOAT, 0, None)

    def draw_lua(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, len(self.lua.vertices))

    def rotate_lua(self, speed=0.01):
        # Incrementar os ângulos de rotação
        self.angle_x += speed
        self.angle_y += speed / 2  # Velocidade de rotação diferente para Y
        self.angle_z += speed / 3  # Velocidade de rotação diferente para Z

        # Cálculos de seno e cosseno para cada eixo
        cos_x = math.cos(self.angle_x)
        sin_x = math.sin(self.angle_x)
        cos_y = math.cos(self.angle_y)
        sin_y = math.sin(self.angle_y)
        cos_z = math.cos(self.angle_z)
        sin_z = math.sin(self.angle_z)

        # Matriz de rotação no eixo X
        rotation_x = np.array([
            [1.0,  0.0,    0.0,   0.0],
            [0.0,  cos_x, -sin_x,  0.0],
            [0.0,  sin_x,  cos_x,  0.0],
            [0.0,  0.0,    0.0,   1.0]
        ], dtype=np.float32)

        # Matriz de rotação no eixo Y
        rotation_y = np.array([
            [cos_y,  0.0,  sin_y,  0.0],
            [0.0,    1.0,   0.0,   0.0],
            [-sin_y, 0.0,  cos_y,  0.0],
            [0.0,    0.0,   0.0,   1.0]
        ], dtype=np.float32)

        # Matriz de rotação no eixo Z
        rotation_z = np.array([
            [cos_z, -sin_z, 0.0,   0.0],
            [sin_z,  cos_z, 0.0,   0.0],
            [0.0,     0.0,  1.0,   0.0],
            [0.0,     0.0,  0.0,   1.0]
        ], dtype=np.float32)

        # Carregar e multiplicar as matrizes de rotação (ordem: Z, Y, X)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(rotation_z)
        glMultMatrixf(rotation_y)
        glMultMatrixf(rotation_x)