import numpy as np
import random
from OpenGL.GL import *

class Lua:
    def __init__(self, radius=0.5, subdivisions=20):
        self.radius = radius
        self.subdivisions = subdivisions
        self.vertices = []
        self.colors = []
        self.generate_sphere()

    def generate_sphere(self):
        # Gera vértices para uma esfera usando subdivisões em uma malha triangular
        for i in range(self.subdivisions):
            lat0 = np.pi * (-0.5 + float(i) / self.subdivisions)
            z0 = np.sin(lat0)
            zr0 = np.cos(lat0)

            lat1 = np.pi * (-0.5 + float(i + 1) / self.subdivisions)
            z1 = np.sin(lat1)
            zr1 = np.cos(lat1)

            for j in range(self.subdivisions):
                lng = 2 * np.pi * float(j) / self.subdivisions
                x = np.cos(lng)
                y = np.sin(lng)

                self.vertices.append((x * zr0 * self.radius, y * zr0 * self.radius, z0 * self.radius))
                self.vertices.append((x * zr1 * self.radius, y * zr1 * self.radius, z1 * self.radius))

                # Gerando cores aleatórias para os triângulos
                self.colors.append((random.random(), random.random(), random.random(), 1.0))
                self.colors.append((random.random(), random.random(), random.random(), 1.0))

    def get_vertices(self):
        return np.array(self.vertices, dtype=np.float32)

    def get_colors(self):
        return np.array(self.colors, dtype=np.float32)
