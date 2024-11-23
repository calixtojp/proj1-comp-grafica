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

    minion = Objeto('minion.obj', 'minion.png', 'minion.png')
    cacto = Objeto('cacto.obj', 'cacto.jpg', 'cacto.jpg', tam=0.1)

    luz.configurar()
    
    while (not glfwWindowShouldClose(window)):
        
        it.preProc()
        it.processInput(window)

        luz.aplicar()
        
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # view/projection transformations
        projection = glm.perspective(glm.radians(it.camera.Zoom), it.SCR_WIDTH / it.SCR_HEIGHT, 0.1, 100.0)
        view = it.camera.GetViewMatrix()
        luz.lightingShader.setMat4("projection", projection)
        luz.lightingShader.setMat4("view", view)


        #----------------------------------------------DESENHAR---------------------------------------#
        minion.desenhar(luz.lightingShader)
        cacto.desenhar(luz.lightingShader)
        
        #-------------------------------------------LAMPADAS-----------------------------------------#
        # also draw the lamp object(s)
        luz.lightCubeShader.use()
        luz.lightCubeShader.setMat4("projection", projection)
        luz.lightCubeShader.setMat4("view", view)

        # we now draw as many light bulbs as we have point lights.
        for i in range(2):
            model = glm.mat4(1.0)
            model = glm.translate(model, luz.pos[i])
            model = glm.scale(model, glm.vec3(0.1)) # Make it a smaller cube
            luz.lightCubeShader.setMat4("model", model)
            glDrawArrays(GL_TRIANGLES, 0, 288)
        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        # -------------------------------------------------------------------------------
        glfwSwapBuffers(window)
        glfwPollEvents()

    # glfw: terminate, clearing all previously allocated GLFW resources.
    glfwTerminate()
    return 0

main()
