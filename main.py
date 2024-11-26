from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
import glm
import platform, ctypes, os

from camera import Camera, Camera_Movement
from shader_m import Shader
import uteis
import interacoes as it
from objeto import Objeto
from luzes import Luz

def main() -> int:
    window = uteis.config_inicial()
    luz = Luz()

    chao = Objeto('chao.obj','chao.jpg','chao.jpg', trans = [0, -10, 0], scale=[10, 0.7, 10])
    ceu = Objeto('esfera2.obj', 'nightSky.jpg', 'nightSky.jpg', scale=[20, 20, 20])
    nave = Objeto('nave.obj', 'nave_diffuse.png', 'nave_spec.png', trans=[it.nave_x, it.nave_y, it.nave_z], scale=[0.8,0.8,0.8])
    vaca = Objeto('vaca.obj', 'vaca.jpeg', 'vaca.jpeg', tam=0.3, trans=[0, -10.5, 0],angle=50,rot=[1, 0, 1])
    cacto = Objeto('cacto.obj', 'cacto.jpg','cacto.jpg', tam=0.08,trans=[100, -60, 40], angle=-90, rot=[1, 0, 0], scale=[1, 0.7, 1])
    minion = Objeto('minion.obj', 'minion.png', 'minion.png',trans=[0, 44.5, 0], scale=[0.7, 0.7, 0.7])
    tocha = Objeto('tocha.obj', 'tocha.jpeg', 'tocha.jpeg', trans=[2, 44, 0.5], scale=[0.1, 0.1, 0.1])
    cilindroNaveEx = Objeto('cilindro.obj', 'chao.jpg', 'chao.jpg', trans=luz.pos[0], scale=[60, 0.2, 60])
    cilindroNaveIn = Objeto('cilindro.obj', 'chao.jpg', 'chao.jpg', trans=luz.pos[1], scale=[60, 1, 60])
    cilindroTocha = Objeto('cilindro.obj', 'chao.jpg', 'chao.jpg', trans=luz.pos[2], scale=[2, 1, 2])
    pedra = Objeto('pedra.obj', 'pedra.jpg', 'pedra.jpg', tam=0.01,trans=[600, -430, 600])
    cj2 = Objeto('cj2.obj', 'cj2.png', 'cj2.png', trans=[0, 8, 0], scale=[3, 3, 3])
    

    while (not glfwWindowShouldClose(window)):
        it.preProc()
        it.processInput(window)

        luz.preProcObj()
        luz.aplicar()

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # view/projection transformations
        projection = glm.perspective(glm.radians(it.camera.Zoom), it.SCR_WIDTH / it.SCR_HEIGHT, 0.1, 1000.0)
        view = it.camera.GetViewMatrix()
        luz.lightingShader.setMat4("projection", projection)
        luz.lightingShader.setMat4("view", view)

        #----------------------------------------------DESENHAR---------------------------------------#

        #usar como referênca a posição da nave para fazer os desenhos
        pos_nave = [it.nave_x, it.nave_y, it.nave_z]

        #modificar a posição das luzes
        luz.pos = [
                glm.vec3(it.nave_x,  it.nave_y+9,  it.nave_z),
                glm.vec3(it.nave_x, it.nave_y+13, it.nave_z),
                glm.vec3(it.nave_x+2.05, it.nave_y+23, it.nave_z+0.5)
            ]
        
        chao.desenhar(luz.lightCubeShader)
        ceu.desenhar(luz.lightCubeShader)

        #nave
        luz.configurar_iluminacao(ambient_=5)
        nave.trans = pos_nave
        nave.desenhar(luz.lightCubeShader)
        luz.configurar_iluminacao(ambient_=1)

        vaca.desenhar(luz.lightCubeShader)
        cacto.desenhar(luz.lightCubeShader)

        #minion
        minion.trans = [it.nave_x, it.nave_y+22.5, it.nave_z]
        minion.desenhar(luz.lightCubeShader)
        
        #tocha
        tocha.trans = [luz.pos[2].x, luz.pos[2].y-1.7, luz.pos[2].z]
        tocha.desenhar(luz.lightCubeShader)

        #teste pra desenhar a pedra com specular menor ---------------------------------
        luz.configurar_iluminacao(specular_=0.01)#diminuo o specular da pedra antes de desenhar
        pedra.desenhar(luz.lightCubeShader)
        luz.configurar_iluminacao(specular_=1)#volto o specular da pedra depois de desenhar

        cj2.trans = [it.nave_x, it.nave_y+15, it.nave_z]
        cj2.desenhar(luz.lightCubeShader)

        #-------------------------------------------LAMPADAS-----------------------------------------#
        luz.preProcLampada(projection, view)

        cilindroTocha.trans = [luz.pos[2].x, luz.pos[2].y, luz.pos[2].z]
        cilindroTocha.desenhar(luz.lightCubeShader)
       

        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()
    return 0

main()
