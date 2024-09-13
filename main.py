import glfw
from OpenGL.GL import *
from objetos import Objetos
from uteis import *

def main():

    # # Inicializar GLFW
    # if not glfw.init():
    #     return

    # # Configurar janela
    # window = glfw.create_window(800, 800, "Cena Principal", None, None)
    # if not window:
    #     glfw.terminate()
    #     return

    # glfw.make_context_current(window)


    window = janela()

    #loc_color = glGetUniformLocation(program, "color")
    

    # Criar objetos
    objetos = Objetos()

    # Loop principal
    while not glfw.window_should_close(window):
        glfw.poll_events()

        print('janeluda')

        # Limpa a tela para preparar o próximo quadro.
        # O fundo é definido como branco (1.0, 1.0, 1.0, 1.0).
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)

        print("gl clear")

        # Rotacionar a lua
        # objetos.rotate_lua()
        objetos.rotate()
        print("rotate")

        # Desenhar a lua
        # objetos.draw_lua()
        objetos.draw()
        print("draw")

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
