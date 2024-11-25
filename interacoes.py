from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
from camera import Camera, Camera_Movement
import glm
import platform, ctypes, os

# settings
SCR_WIDTH = 1200
SCR_HEIGHT = 900

# camera
camera = Camera(glm.vec3(0.0, 0.0, 3.0))
lastX = SCR_WIDTH / 2.0
lastY = SCR_HEIGHT / 2.0
firstMouse = True

# timing
deltaTime = 0.0
lastFrame = 0.0

#posicionamento de objetos
delta_x = 0
delta_y = 0
delta_z = 0

toggle_sl = 1
toggle_pl1 = 1
toggle_pl2 = 1
toggle_pl3 = 1
toggle_dir = 1

spec = 1
dif = 1
amb = 1


#prepara pra usar a processInput()
def preProc():
    global deltaTime, lastFrame

    currentFrame = glfwGetTime()
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame

# process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
# ---------------------------------------------------------------------------------------------------------
def processInput(window: GLFWwindow) -> None:
    global camera, toggle_dir, toggle_pl1, toggle_pl2, toggle_pl3, toggle_sl, spec, dif, amb

    key_processed = False 

    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS):
        glfwSetWindowShouldClose(window, True)

    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.FORWARD, deltaTime)
    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.BACKWARD, deltaTime)
    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.LEFT, deltaTime)
    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.RIGHT, deltaTime)
    if(glfwGetKey(window, GLFW_KEY_1) == GLFW_PRESS):
        amb -= 0.2 
    if(glfwGetKey(window, GLFW_KEY_2) == GLFW_PRESS):
        amb += 0.2
    if(glfwGetKey(window, GLFW_KEY_3) == GLFW_PRESS):
        dif -= 0.2 
    if(glfwGetKey(window, GLFW_KEY_4) == GLFW_PRESS):
        dif += 0.2
    if(glfwGetKey(window, GLFW_KEY_5) == GLFW_PRESS):
        spec -= 0.2
    if(glfwGetKey(window, GLFW_KEY_6) == GLFW_PRESS):
        spec += 0.2

    if glfwGetKey(window, GLFW_KEY_F1) == GLFW_PRESS:
        if not key_processed:
            if(toggle_dir == 0):
                toggle_dir = 1
            else:
                toggle_dir = 0
            key_processed = True
    elif glfwGetKey(window, GLFW_KEY_F1) == GLFW_RELEASE:
        key_processed = False

    if glfwGetKey(window, GLFW_KEY_F2) == GLFW_PRESS:
        if not key_processed:
            if(toggle_pl1 == 0):
                toggle_pl1 = 1
            else:
                toggle_pl1 = 0
            key_processed = True
    elif glfwGetKey(window, GLFW_KEY_F2) == GLFW_RELEASE:
        key_processed = False


    if glfwGetKey(window, GLFW_KEY_F3) == GLFW_PRESS:
        if not key_processed:
            if(toggle_pl2 == 0):
                toggle_pl2 = 1
            else:
                toggle_pl2 = 0
            key_processed = True
    elif glfwGetKey(window, GLFW_KEY_F3) == GLFW_RELEASE:
        key_processed = False


    if glfwGetKey(window, GLFW_KEY_F4) == GLFW_PRESS:
        if not key_processed:
            if(toggle_pl3 == 0):
                toggle_pl3 = 1
            else:
                toggle_pl3 = 0
            key_processed = True
    elif glfwGetKey(window, GLFW_KEY_F4) == GLFW_RELEASE:
        key_processed = False


    if glfwGetKey(window, GLFW_KEY_F5) == GLFW_PRESS:
        if not key_processed:
            if(toggle_sl == 0):
                toggle_sl = 1
            else:
                toggle_sl = 0
            key_processed = True
    elif glfwGetKey(window, GLFW_KEY_F5) == GLFW_RELEASE:
        key_processed = False


# glfw: whenever the mouse moves, this callback is called
# -------------------------------------------------------
def mouse_callback(window: GLFWwindow, xpos: float, ypos: float) -> None:
    global lastX, lastY, firstMouse

    if (firstMouse):

        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos # reversed since y-coordinates go from bottom to top

    lastX = xpos
    lastY = ypos

    camera.ProcessMouseMovement(xoffset, yoffset)

# glfw: whenever the mouse scroll wheel scrolls, this callback is called
# ----------------------------------------------------------------------
def scroll_callback(window: GLFWwindow, xoffset: float, yoffset: float) -> None:

    camera.ProcessMouseScroll(yoffset)

# glfw: whenever the window size changed (by OS or user resize) this callback function executes
# ---------------------------------------------------------------------------------------------
def framebuffer_size_callback(window: GLFWwindow, width: int, height: int) -> None:

    # make sure the viewport matches the new window dimensions note that width and 
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height)