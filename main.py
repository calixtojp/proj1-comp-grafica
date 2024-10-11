import glfw
from OpenGL.GL import *
import numpy as np
import uteis as ut
from arvore import Arvore

def main():
  
  #Iniciando algumas configurações, da janela e do programa
  window = ut.janela()
  program = ut.programa()

  #criando os objetos
  arv = Arvore()
  

  #concatenando todos os vértices dos objetos a fim de passá-los para a gpu
  vertices = arv.vertices_list
  total_vertices = len(vertices)
  merged_vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
  merged_vertices['position'] = vertices

  texture = arv.textures_coord_list
  total_texture = len(texture)
  merged_texture = np.zeros(total_texture, [("position", np.float32, 2)])
  merged_texture['position'] = texture

  #passando todos os vértices pra gpu
  ut.passar_para_gpu(program, merged_vertices, "vertices")
  ut.passar_para_gpu(program, texture, "textura")

  #pegando a variável de cor do programa criado
  loc_color = glGetUniformLocation(program, "color")

  #configurando o teclado
  #glfw.set_key_callback(window,ut.key_event)

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
    if False:
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

    #desenha os objetos de acordo com suas posições iniciais na GPU
    arv.desenha_arvore(program)

    #matrizes view e projection
    mat_view = ut.view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    mat_projection = ut.projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
        
    #Termina o programa
    glfw.swap_buffers(window)

  glfw.terminate()


if __name__ == "__main__":
    main()
