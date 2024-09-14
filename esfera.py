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


    # Entrada: angulo de longitude, latitude, raio
    # Saida: coordenadas na esfera
    def F(u,v,r):
        x = r*math.sin(v)*math.cos(u)
        y = r*math.sin(v)*math.sin(u)
        z = r*math.cos(v)
        return (x,y,z)