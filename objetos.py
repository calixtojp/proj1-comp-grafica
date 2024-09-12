from lua import Lua
from OpenGL.GL import *
import numpy as np
import math

class Objetos:
    def __init__(self):
        self.lua = Lua()
        self.angle = 0.0  # Inicialização do ângulo de rotação

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
        self.angle += speed
        cos_angle = math.cos(self.angle)
        sin_angle = math.sin(self.angle)

        # Matriz de rotação
        rotation_matrix = np.array([
            [cos_angle, -sin_angle, 0.0, 0.0],
            [sin_angle, cos_angle,  0.0, 0.0],
            [0.0,       0.0,        1.0, 0.0],
            [0.0,       0.0,        0.0, 1.0]
        ], dtype=np.float32)

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(rotation_matrix)
