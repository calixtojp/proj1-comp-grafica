import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random
from uteis import *
from chao import Chao
from cacto import Cacto

def main():
   

  #Iniciando algumas configurações, da janela e do programa
  window = janela()
  program = programa()

  #criando os objetos
  chao = Chao()
  cacto = Cacto()


  #concatenando todos os vértices dos objetos a fim de passá-los para a gpu
  vertices = np.concatenate((chao.vertices['position'], cacto.vertices['position']))

  total_vertices = len(vertices)
  merged_vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
  merged_vertices['position'] = vertices


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
    glClearColor(0.22, 0.38, 0.45, 1.0)
    

    #Switch entre visualização normal e de malha poligonal
    if False:
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    chao.desenhar(program, loc_color, 0)
    cacto.desenhar(program, loc_color, chao.tam)
    
    glfw.swap_buffers(window)

  glfw.terminate()


if __name__ == "__main__":
    main()
