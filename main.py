import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random
from uteis import *
from cilindro import Cirilo
from chao import Chao
from esfera import Esfera

def main():
   

  #Iniciando algumas configurações, da janela e do programa
  window = janela()
  program = programa()

  #criando os objetos
  cilindro = Cirilo(0.9, 0.1)

  # cilindro2 = Cirilo(0.4, 0.7)

  # chao = Chao()

  bola = Esfera(0.5)

  #concatenando todos os vértices dos objetos a fim de passá-los para a gpu
  vertices = np.concatenate((bola.vertices['position'], cilindro.vertices['position']))
  # vertices = np.concatenate((vertices, chao.vertices['position']))
  # vertices = np.concatenate((vertices, bola.vertices['position']))

  total_vertices = len(vertices)
  merged_vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
  merged_vertices['position'] = vertices


  #ISSO AQUI É O QUE VAI INDICAR A POSICAO INICIAL DE CADA UM
  print(f"cilindro 1 :{len(cilindro.vertices)}")
  # print(f"cilindro 2 :{len(cilindro2.vertices)}")
  # print(f"chao :{len(chao.vertices)}")
  print(f"bola :{len(bola.vertices)}")
  # print(f"total :{len(merged_vertices)}")


  #passando todos os vértices pra gpu
  passar_para_gpu(program, merged_vertices)

  #pegando a variável de cor do programa criado
  loc_color = glGetUniformLocation(program, "color")


  #Loop principal que efetivamente mostra a janela
  while not glfw.window_should_close(window):

    glfw.poll_events() #Leitura de eventos da janela
    
    # Limpa a tela para preparar o próximo quadro.
    # O fundo é definido como branco (1.0, 1.0, 1.0, 1.0).
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    

    #Switch entre visualização normal e de malha poligonal
    if False:
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    bola.desenhar(program, loc_color, 0)
    cilindro.desenhar(program, loc_color, 6144)
    
    glfw.swap_buffers(window)

  glfw.terminate()


if __name__ == "__main__":
    main()