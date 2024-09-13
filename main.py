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

  passar_para_gpu(program, cilindro.vertices)

  # Não sei oq exatamente isso faz, mas no notebook do professor, 
  # tá falando q pega a localização da variável de cor (uniform) do Fragment Shader
  # pra poder alterar ela no laço da janela. N sei oq significa.

  loc_color = glGetUniformLocation(program, "color")

  #ângulo de rotação do objeto. Inicialmente é zero, mas vai sendo decrementada 
  # a cada iteração para gerar o movimento de rotação.
  global d
  d = 0.0

  while not glfw.window_should_close(window):

    glfw.poll_events() #Leitura de eventos da janela
    
    # Limpa a tela para preparar o próximo quadro.
    # O fundo é definido como branco (1.0, 1.0, 1.0, 1.0).
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    if False:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    cilindro.desenhar(program, loc_color)
    
    glfw.swap_buffers(window)

  glfw.terminate()


if __name__ == "__main__":
    main()
