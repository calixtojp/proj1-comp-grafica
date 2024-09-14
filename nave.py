import numpy as np
import random
from OpenGL.GL import *
import math
import cilindro
import esfera

PI = 3.141592 

class Nave:
  def __init__(self):

    self.raio_esfera_central = 0.1
    self.raio_cilindro_central = 0.3
    self.raio_cilindro_externo = 0.7
    self.altura_cilindro_central = 0.2
    self.altura_cilindro_externo = 0.2

    self.vertices = []
    self.cria_nave()

    self.d = 0

  
  def cria_nave(self):
    # vamos gerar um conjunto de vertices representantes poligonos
    # para a superficie da nave.
    # cada poligono eh representado por dois triangulos

    vertices_list = []
    cilindro_central = cilindro.Cirilo(self.altura_cilindro_central, self.raio_cilindro_central)
    cilindro_externo = cilindro.Cirilo(self.altura_cilindro_externo, self.raio_cilindro_externo)
    esfera_central = esfera.Esfera(self.raio_esfera_central)

    vertices_list = np.concatenate((cilindro_central.vertices['position'], cilindro_externo.vertices['position'], esfera_central.vertices['position']))