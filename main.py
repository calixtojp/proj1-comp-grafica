from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
import glm
import platform, ctypes, os

from camera import Camera, Camera_Movement
from shader_m import Shader
import uteis
import interacoes
from objeto import Objeto
from luzes import Luz

def main() -> int:
    window = uteis.config_inicial()
    luz = Luz()

    caixa0 = Objeto('caixa.obj','caixa.jpg','caixa.jpg', trans = luz.pos[0])
    caixa1 = Objeto('caixa.obj','caixa.jpg','caixa.jpg', tam=10,trans = luz.pos[1])
    chao = Objeto('chao.obj','chao.jpg','chao.jpg',tam=1, trans = [0, -10, 0], scale=[1, 0.7, 1])
    ceu = Objeto('esfera2.obj', 'nightSky.jpg', 'nightSky.jpg', tam=10)
    nave = Objeto('nave.obj', 'nave_diffuse.png', 'nave_spec.png', tam=0.6, trans=[0, 45, 0])
    vaca = Objeto('vaca.obj', 'vaca.jpeg', 'vaca.jpeg', tam=0.3, trans=[0, -10.5, 0],angle=50,rot=[1, 0, 1])
    cacto = Objeto('cacto.obj', 'cacto.jpg','cacto.jpg', tam=0.08,trans=[100, -60, 40], angle=-90, rot=[1, 0, 0], scale=[1, 0.7, 1])
    minion = Objeto('minion.obj', 'minion.png', 'minion.png', tam=0.7,trans=[0, 40, 0])
    tocha = Objeto('tocha.obj', 'tocha.jpeg', 'tocha.jpeg', tam=0.25)
    pedra = Objeto('pedra.obj', 'pedra.jpg', 'pedra.jpg', tam=0.01,trans=[600, -430, 600])
    
    while (not glfwWindowShouldClose(window)):
        interacoes.preProc()
        interacoes.processInput(window)

        luz.preProcObj()
        luz.aplicar()

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # view/projection transformations
        projection = glm.perspective(glm.radians(interacoes.camera.Zoom), interacoes.SCR_WIDTH / interacoes.SCR_HEIGHT, 0.1, 100.0)
        view = interacoes.camera.GetViewMatrix()
        luz.lightingShader.setMat4("projection", projection)
        luz.lightingShader.setMat4("view", view)

        #----------------------------------------------DESENHAR---------------------------------------#
        chao.desenhar(luz.lightCubeShader)
        ceu.desenhar(luz.lightCubeShader)
        nave.desenhar(luz.lightCubeShader)
        vaca.desenhar(luz.lightCubeShader)
        cacto.desenhar(luz.lightCubeShader)
        minion.desenhar(luz.lightCubeShader)
        tocha.desenhar(luz.lightCubeShader)

        #teste pra desenhar a pedra com specular menor ---------------------------------
        luz.configurar_iluminacao(specular_=0.01)#diminuo o specular da pedra antes de desenhar
        pedra.desenhar(luz.lightCubeShader)
        luz.configurar_iluminacao(specular_=1)#volto o specular da pedra depois de desenhar


        #-------------------------------------------LAMPADAS-----------------------------------------#
        luz.preProcLampada(projection, view)
        caixa0.desenhar(luz.lightCubeShader)
        caixa1.desenhar(luz.lightCubeShader)             
        

        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()
    return 0

main()
