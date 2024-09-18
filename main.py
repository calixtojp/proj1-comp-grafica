import glfw
from OpenGL.GL import *
import numpy as np
import uteis as ut
from chao import Chao
from cacto import Cacto
from homem import Homem
from nave import Nave
from nuvem import Nuvem

def main():
  
  #Iniciando algumas configurações, da janela e do programa
  window = ut.janela()
  program = ut.programa()

  #criando os objetos
  chao = Chao()
  cacto = Cacto()
  homem = Homem()
  nave = Nave(0.6)

  qntd_nuvens = 20
  intervalo_raios = (0.04, 0.19)
  nuvem = Nuvem(qntd_nuvens, intervalo_raios, 1)

  #concatenando todos os vértices dos objetos a fim de passá-los para a gpu
  vertices = np.concatenate((chao.vertices['position'], cacto.vertices['position']))
  vertices = np.concatenate((vertices, homem.vertices['position']))
  vertices = np.concatenate((vertices, nave.vertices['position']))
  vertices = np.concatenate((vertices, nuvem.vertices['position']))

  total_vertices = len(vertices)
  merged_vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
  merged_vertices['position'] = vertices

  #passando todos os vértices pra gpu
  ut.passar_para_gpu(program, merged_vertices)

  #pegando a variável de cor do programa criado
  loc_color = glGetUniformLocation(program, "color")

  #configurando o teclado
  glfw.set_key_callback(window,ut.key_event)

  #Loop principal que efetivamente mostra a janela
  while not glfw.window_should_close(window):

    glfw.poll_events() #Leitura de eventos da janela
    
    # Limpa a tela para preparar o próximo quadro.
    # O fundo é definido como branco (1.0, 1.0, 1.0, 1.0).
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.44, 0.6, 0.7, 1.0)

    #Ativa o uso de transparência
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    #Switch entre visualização normal e de malha poligonal
    if ut.malha:
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

    #desenha os objetos de acordo com suas posições iniciais na GPU
    pos_gpu = 0
    chao.desenhar(program, loc_color, pos_gpu)
    pos_gpu += chao.tam
    cacto.desenhar(program, loc_color, pos_gpu)
    pos_gpu += cacto.tam
    homem.desenhar(program, loc_color, pos_gpu)
    pos_gpu += homem.tam
    nave.desenhar(program, loc_color, pos_gpu)
    pos_gpu += nave.tam
    nuvem.desenhar(program, loc_color, pos_gpu)
    pos_gpu += nuvem.tam
    
    #Termina o programa
    glfw.swap_buffers(window)

  glfw.terminate()


if __name__ == "__main__":
    main()
