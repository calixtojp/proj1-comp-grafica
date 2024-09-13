import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import random
from uteis import *
from cilindro import Cirilo

def main():
   
  window = janela()
  program = programa()

  cilindro = Cirilo(0.9, 0.1)

  cilindro2 = Cirilo(0.4, 0.7)

  vertices = np.concatenate((cilindro2.vertices['position'], cilindro.vertices['position']))

  print(len(cilindro.vertices))
  print(cilindro.vertices)


  pos = 2520


  print("--------------------------------------------")
  print(len(cilindro2.vertices))
  print(cilindro2.vertices)

  print("--------------------------------------------")

  total_vertices = len(vertices)
  merged_vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
  merged_vertices['position'] = vertices


  print(len(merged_vertices))
  print(merged_vertices)
  print("--------------------------------------------")


  passar_para_gpu(program, merged_vertices)

  # Não sei oq exatamente isso faz, mas no notebook do professor, 
  # tá falando q pega a localização da variável de cor (uniform) do Fragment Shader
  # pra poder alterar ela no laço da janela. N sei oq significa.

  loc_color = glGetUniformLocation(program, "color")

  while not glfw.window_should_close(window):

    glfw.poll_events() #Leitura de eventos da janela
    
    # Limpa a tela para preparar o próximo quadro.
    # O fundo é definido como branco (1.0, 1.0, 1.0, 1.0).
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    if True:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    cilindro2.desenhar(program, loc_color, 0)
    cilindro.desenhar(program, loc_color, 2520)
    
    glfw.swap_buffers(window)

  glfw.terminate()


if __name__ == "__main__":
    main()
