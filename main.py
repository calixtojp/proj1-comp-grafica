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

# lighting
lightPos = glm.vec3(1.2, 1.0, 2.0)

def main() -> int:
    # glfw: initialize and configure
    # ------------------------------
    glfwInit()
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    if (platform.system() == "Darwin"): # APPLE
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)

    # glfw window creation
    # --------------------
    window = glfwCreateWindow(it.SCR_WIDTH, it.SCR_HEIGHT, "LearnOpenGL", None, None)
    if (window == None):

        print("Failed to create GLFW window")
        glfwTerminate()
        return -1

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, it.framebuffer_size_callback)
    glfwSetCursorPosCallback(window, it.mouse_callback)
    glfwSetScrollCallback(window, it.scroll_callback)

    # tell GLFW to capture our mouse
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)

    # configure global opengl state
    # -----------------------------
    glEnable(GL_DEPTH_TEST)

    # build and compile our shader zprogram
    # ------------------------------------
    lightingShader = Shader("shaders/6.multiple_lights.vs", "shaders/6.multiple_lights.fs")
    lightCubeShader = Shader("shaders/6.light_cube.vs", "shaders/6.light_cube.fs")
    # set up vertex data (and buffer(s)) and configure vertex attributes
    # ------------------------------------------------------------------

    minion = Objeto('minion.obj', 'minion.png', 'minion.png')
    cacto = Objeto('cacto.obj', 'cacto.jpg', 'cacto.jpg', tam=0.1)

    # positions of the point lights
    pointLightPositions = [
        glm.vec3( 10.7,  0.2,  2.0),
        glm.vec3( -10.3, -3.3, -4.0)
    ]

    # shader configuration
    # --------------------
    lightingShader.use()
    lightingShader.setInt("material.diffuse", 0)
    lightingShader.setInt("material.specular", 1)

    # render loop
    # -----------
    while (not glfwWindowShouldClose(window)):

        # per-frame time logic
        # --------------------
        currentFrame = glfwGetTime()
        it.deltaTime = currentFrame - it.lastFrame
        it.lastFrame = currentFrame

        # input
        # -----
        it.processInput(window)

        # render
        # ------
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # be sure to activate shader when setting uniforms/drawing objects
        lightingShader.use()
        lightingShader.setVec3("viewPos", it.camera.Position)
        lightingShader.setFloat("material.shininess", 32.0)

        
        #   Here we set all the uniforms for the 5/6 types of lights we have. We have to set them manually and index 
        #   the proper PointLight struct in the array to set each uniform variable. This can be done more code-friendly
        #   by defining light types as classes and set their values in there, or by using a more efficient uniform approach
        #   by using 'Uniform buffer objects', but that is something we'll discuss in the 'Advanced GLSL' tutorial.
           
        s = 1
        d = 1
        a = 1

        # directional light
        lightingShader.setVec3("dirLight.direction", -0.2, -1.0, -0.3)
        lightingShader.setVec3("dirLight.ambient", a*0.05, a*0.05, a*0.05)
        lightingShader.setVec3("dirLight.diffuse", d*0.4, d*0.4, d*0.4)
        lightingShader.setVec3("dirLight.specular", s*0.5, s*0.5, s*0.5)
        # point light 1
        lightingShader.setVec3("pointLights[0].position", pointLightPositions[0])
        lightingShader.setVec3("pointLights[0].ambient", a*0.05, a*0.05, a*0.05)
        lightingShader.setVec3("pointLights[0].diffuse", d*0.8, d*0.8, d*0.8)
        lightingShader.setVec3("pointLights[0].specular", s*1.0, s*1.0, s*1.0)
        lightingShader.setFloat("pointLights[0].constant", 1.0)
        lightingShader.setFloat("pointLights[0].linear", 0.09)
        lightingShader.setFloat("pointLights[0].quadratic", 0.032)
        # point light 2
        lightingShader.setVec3("pointLights[1].position", pointLightPositions[1])
        lightingShader.setVec3("pointLights[1].ambient", a*0.05, a*0.05, a*0.05)
        lightingShader.setVec3("pointLights[1].diffuse", d*0.8, d*0.8, d*0.8)
        lightingShader.setVec3("pointLights[1].specular", s*1.0, s*1.0, s*1.0)
        lightingShader.setFloat("pointLights[1].constant", 1.0)
        lightingShader.setFloat("pointLights[1].linear", 0.09)
        lightingShader.setFloat("pointLights[1].quadratic", 0.032)
        # spotLight
        lightingShader.setVec3("spotLight.position", it.camera.Position)
        lightingShader.setVec3("spotLight.direction", it.camera.Front)
        lightingShader.setVec3("spotLight.ambient", a*0.0, a*0.0, a*0.0)
        lightingShader.setVec3("spotLight.diffuse", d*1.0, d*1.0, d*1.0)
        lightingShader.setVec3("spotLight.specular", s*1.0, s*1.0, s*1.0)
        lightingShader.setFloat("spotLight.constant", 1.0)
        lightingShader.setFloat("spotLight.linear", 0.09)
        lightingShader.setFloat("spotLight.quadratic", 0.032)
        lightingShader.setFloat("spotLight.cutOff", glm.cos(glm.radians(12.5)))
        lightingShader.setFloat("spotLight.outerCutOff", glm.cos(glm.radians(15.0)))     

        # view/projection transformations
        projection = glm.perspective(glm.radians(it.camera.Zoom), it.SCR_WIDTH / it.SCR_HEIGHT, 0.1, 100.0)
        view = it.camera.GetViewMatrix()
        lightingShader.setMat4("projection", projection)
        lightingShader.setMat4("view", view)

        # world transformation
        model = glm.mat4(1.0)
        lightingShader.setMat4("model", model)


        #----------------------------------------------DESENHAR---------------------------------------#
        minion.desenhar(lightingShader)
        cacto.desenhar(lightingShader)
        
        #-------------------------------------------LAMPADAS-----------------------------------------#
        # also draw the lamp object(s)
        lightCubeShader.use()
        lightCubeShader.setMat4("projection", projection)
        lightCubeShader.setMat4("view", view)

        # we now draw as many light bulbs as we have point lights.
        for i in range(2):
            model = glm.mat4(1.0)
            model = glm.translate(model, pointLightPositions[i])
            model = glm.scale(model, glm.vec3(0.1)) # Make it a smaller cube
            lightCubeShader.setMat4("model", model)
            glDrawArrays(GL_TRIANGLES, 0, 288)
        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        # -------------------------------------------------------------------------------
        glfwSwapBuffers(window)
        glfwPollEvents()

    # glfw: terminate, clearing all previously allocated GLFW resources.
    glfwTerminate()
    return 0

main()
