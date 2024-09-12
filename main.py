import glfw
from OpenGL.GL import *
from objetos import Objetos

def main():
    # Inicializar GLFW
    if not glfw.init():
        return

    # Configurar janela
    window = glfw.create_window(800, 800, "Cena Principal", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Habilitar teste de profundidade
    glEnable(GL_DEPTH_TEST)

    # Criar objetos
    objetos = Objetos()

    # Loop principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Rotacionar a lua
        # objetos.rotate_lua()
        objetos.rotate()

        # Desenhar a lua
        # objetos.draw_lua()
        objetos.draw()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
