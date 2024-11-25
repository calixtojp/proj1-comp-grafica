from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
import glm
import platform, ctypes, os

from camera import Camera, Camera_Movement
from shader_m import Shader
import uteis as ut
import interacoes as it
from objeto import Objeto
from luzes import Luz

def main() -> int:

    window = ut.config_inicial()
    luz = Luz()

    caixa0 = Objeto('caixa.obj','caixa.jpg','caixa.jpg', trans = luz.pos[0])
    caixa1 = Objeto('caixa.obj','caixa.jpg','caixa.jpg', tam=10,trans = luz.pos[1])
    chao = Objeto('chao.obj','chao.jpg','chao.jpg', trans = [0, -10, 0], scale=[1, 0.7, 1])
    ceu = Objeto('esfera2.obj', 'nightSky.jpg', 'nightSky.jpg', tam=10)

    
    while (not glfwWindowShouldClose(window)):
        
        it.preProc()
        it.processInput(window)

        luz.preProcObj()
        luz.aplicar()
        
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # view/projection transformations
        projection = glm.perspective(glm.radians(it.camera.Zoom), it.SCR_WIDTH / it.SCR_HEIGHT, 0.1, 100.0)
        view = it.camera.GetViewMatrix()
        luz.lightingShader.setMat4("projection", projection)
        luz.lightingShader.setMat4("view", view)


        #----------------------------------------------DESENHAR---------------------------------------#
        chao.desenhar(luz.lightCubeShader)
        ceu.desenhar(luz.lightCubeShader)

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
