from OpenGL.GL import *
import numpy as np
import math

class Lua:
    def __init__(self, radius=0.05, num_segments=12):
        self.radius = radius
        self.num_segments = num_segments

        # Ângulos de rotação
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0

        # Buffers
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.cbo = glGenBuffers(1)

        # Gera os vértices e as cores aleatórias da esfera
        self.vertices, self.colors = self.generate_sphere()
        
        # Configura a esfera
        self.setup_lua()

    def generate_sphere(self):
        vertices = []
        colors = []
        for i in range(self.num_segments):
            theta1 = i * (2 * np.pi / self.num_segments)
            theta2 = (i + 1) * (2 * np.pi / self.num_segments)

            for j in range(self.num_segments):
                phi1 = j * (np.pi / self.num_segments)
                phi2 = (j + 1) * (np.pi / self.num_segments)

                # Ponto 1
                x1 = self.radius * math.sin(phi1) * math.cos(theta1)
                y1 = self.radius * math.cos(phi1)
                z1 = self.radius * math.sin(phi1) * math.sin(theta1)
                vertices.append([x1, y1, z1])

                # Ponto 2
                x2 = self.radius * math.sin(phi2) * math.cos(theta1)
                y2 = self.radius * math.cos(phi2)
                z2 = self.radius * math.sin(phi2) * math.sin(theta1)
                vertices.append([x2, y2, z2])

                # Ponto 3
                x3 = self.radius * math.sin(phi2) * math.cos(theta2)
                y3 = self.radius * math.cos(phi2)
                z3 = self.radius * math.sin(phi2) * math.sin(theta2)
                vertices.append([x3, y3, z3])

                # Cores aleatórias para cada triângulo
                colors.append(np.random.rand(4))
                colors.append(np.random.rand(4))
                colors.append(np.random.rand(4))

        vertices = np.array(vertices, dtype=np.float32)
        colors = np.array(colors, dtype=np.float32)
        return vertices, colors

    def setup_lua(self):
        glBindVertexArray(self.vao)

        # Carregar vértices
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, None)

        # Carregar cores
        glBindBuffer(GL_ARRAY_BUFFER, self.cbo)
        glBufferData(GL_ARRAY_BUFFER, self.colors.nbytes, self.colors, GL_STATIC_DRAW)
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(4, GL_FLOAT, 0, None)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))

    def rotate(self, speed_x=0.01, speed_y=0.01, speed_z=0.01):
        # Incrementar os ângulos de rotação
        self.angle_x += speed_x
        self.angle_y += speed_y
        self.angle_z += speed_z

        # Matriz de rotação no eixo X
        cos_x = math.cos(self.angle_x)
        sin_x = math.sin(self.angle_x)
        rotation_x = np.array([
            [1.0,  0.0,    0.0,   0.0],
            [0.0,  cos_x, -sin_x,  0.0],
            [0.0,  sin_x,  cos_x,  0.0],
            [0.0,  0.0,    0.0,   1.0]
        ], dtype=np.float32)

        # Matriz de rotação no eixo Y
        cos_y = math.cos(self.angle_y)
        sin_y = math.sin(self.angle_y)
        rotation_y = np.array([
            [cos_y,  0.0,  sin_y,  0.0],
            [0.0,    1.0,   0.0,   0.0],
            [-sin_y, 0.0,  cos_y,  0.0],
            [0.0,    0.0,   0.0,   1.0]
        ], dtype=np.float32)

        # Matriz de rotação no eixo Z
        cos_z = math.cos(self.angle_z)
        sin_z = math.sin(self.angle_z)
        rotation_z = np.array([
            [cos_z, -sin_z, 0.0,   0.0],
            [sin_z,  cos_z, 0.0,   0.0],
            [0.0,     0.0,  1.0,   0.0],
            [0.0,     0.0,  0.0,   1.0]
        ], dtype=np.float32)

        # Multiplicando as rotações
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(rotation_x)
        glMultMatrixf(rotation_y)
        glMultMatrixf(rotation_z)
