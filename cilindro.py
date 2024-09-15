import numpy as np
import random
from OpenGL.GL import *
import math

PI = 3.141592 

class Cilindro:
  def __init__(self, h, r):

    self.h = h
    self.r = r

    self.num_sectors = 20 # qtd de sectors (longitude)
    self.num_stacks = 20 # qtd de stacks (latitude)

    # grid sectos vs stacks (longitude vs latitude)
    self.sector_step = (PI*2)/self.num_sectors # variar de 0 até 2π
    self.stack_step = h/self.num_stacks # variar de 0 até H
    
    self.vertices = []
    self.cria_cilindro()

    self.d = 0

  #Entrada: angulo de t, altura h, raio r
  # Saida: coordenadas no cilindro
  def CoordCilindro(self, t, h, r):
    x = r * math.cos(t)
    y = r * math.sin(t)
    z = h
    return (x,y,z)


  def cria_cilindro(self):
    # vamos gerar um conjunto de vertices representantes poligonos
    # para a superficie da esfera.
    # cada poligono eh representado por dois triangulos

    vertices_list = []
    for j in range(0,self.num_stacks): # para cada stack (latitude)
        
      for i in range(0,self.num_sectors): # para cada sector (longitude) 
          
        u = i * self.sector_step # angulo setor
        v = j * self.stack_step # altura da stack
        
        un = 0 # angulo do proximo sector
        if i+1==self.num_sectors:
            un = PI*2
        else: un = (i+1)*self.sector_step
            
        vn = 0 # altura da proxima stack
        if j+1==self.num_stacks:
            vn = self.h
        else: vn = (j+1)*self.stack_step
        
        # verticies do poligono
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
        
        if v == 0:
            vertices_list.append(p0)
            vertices_list.append(p2)
            vertices_list.append(self.CoordCilindro(0, v, 0))
        if vn == self.h:
            #faz um triangulo a partir do mesmo angulo u, mas com as alturas em h = vn
            vertices_list.append(p1)
            vertices_list.append(p3)
            vertices_list.append(self.CoordCilindro(0, vn, 0))

    total_vertices = len(vertices_list)
    self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
    self.vertices['position'] = np.array(vertices_list)